/*
 * Copyright 2013-2019 Software Radio Systems Limited
 *
 * This file is part of srsLTE.
 *
 * srsLTE is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of
 * the License, or (at your option) any later version.
 *
 * srsLTE is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * A copy of the GNU Affero General Public License can be found in
 * the LICENSE file in the top-level directory of this distribution
 * and at http://www.gnu.org/licenses/.
 *
 */

#include <math.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <sys/time.h>
#include <unistd.h>
#include <time.h>
#include <unistd.h>

#include "srslte/srslte.h"

#include "srslte/common/crash_handler.h"
#include "srslte/phy/rf/rf_utils.h"

#ifndef DISABLE_RF
#include "srslte/phy/rf/rf.h"
#endif

#define MHZ 1000000
#define SAMP_FREQ 1920000
#define FLEN 9600
#define FLEN_PERIOD 0.005

#define MAX_EARFCN 1000

int band         = -1;
int earfcn_start = -1, earfcn_end = -1;

cell_search_cfg_t cell_detect_config = {.max_frames_pbch      = SRSLTE_DEFAULT_MAX_FRAMES_PBCH,
                                        .max_frames_pss       = SRSLTE_DEFAULT_MAX_FRAMES_PSS,
                                        .nof_valid_pss_frames = SRSLTE_DEFAULT_NOF_VALID_PSS_FRAMES,
                                        .init_agc             = 0,
                                        .force_tdd            = false};

struct cells {
  srslte_cell_t cell;
  float         freq;
  int           dl_earfcn;
  float         power;
};
struct cells results[1024];

float rf_gain = 70.0;
char* rf_args = "";

void usage(char* prog)
{
  printf("Usage: %s [agsendtvb] -b band\n", prog);
  printf("\t-a RF args [Default %s]\n", rf_args);
  printf("\t-g RF gain [Default %.2f dB]\n", rf_gain);
  printf("\t-s earfcn_start [Default All]\n");
  printf("\t-e earfcn_end [Default All]\n");
  printf("\t-n nof_frames_total [Default 100]\n");
  printf("\t-v [set srslte_verbose to debug, default none]\n");
}

void parse_args(int argc, char** argv)
{
  int opt;
  while ((opt = getopt(argc, argv, "agsendvb")) != -1) {
    switch (opt) {
      case 'a':
        rf_args = argv[optind];
        break;
      case 'b':
        band = (int)strtol(argv[optind], NULL, 10);
        break;
      case 's':
        earfcn_start = (int)strtol(argv[optind], NULL, 10);
        break;
      case 'e':
        earfcn_end = (int)strtol(argv[optind], NULL, 10);
        break;
      case 'n':
        cell_detect_config.max_frames_pss = (uint32_t)strtol(argv[optind], NULL, 10);
        break;
      case 'g':
        rf_gain = strtof(argv[optind], NULL);
        break;
      case 'v':
        srslte_verbose++;
        break;
      default:
        usage(argv[0]);
        exit(-1);
    }
  }
  if (band == -1) {
    usage(argv[0]);
    exit(-1);
  }
}

int srslte_rf_recv_wrapper(void* h, void* data, uint32_t nsamples, srslte_timestamp_t* t)
{
  DEBUG(" ----  Receive %d samples  ---- \n", nsamples);
  return srslte_rf_recv_with_time((srslte_rf_t*)h, data, nsamples, 1, NULL, NULL);
}

bool go_exit = false;

void sig_int_handler(int signo)
{
  printf("SIGINT received. Exiting...\n");
  if (signo == SIGINT) {
    go_exit = true;
  }
}

static SRSLTE_AGC_CALLBACK(srslte_rf_set_rx_gain_wrapper)
{
  srslte_rf_set_rx_gain((srslte_rf_t*)h, gain_db);
}

int srslte_rf_recv_wrapper_cs(void* h, cf_t* data[SRSLTE_MAX_PORTS], uint32_t nsamples, srslte_timestamp_t* t)
{
  DEBUG(" ----  Receive %d samples  ---- \n", nsamples);
  void* ptr[SRSLTE_MAX_CHANNELS] = {};
  for (int i = 0; i < SRSLTE_MAX_PORTS; i++) {
    ptr[i] = data[i];
  }
  return srslte_rf_recv_with_time_multi(h, ptr, nsamples, 1, NULL, NULL);
}

/** This function is simply a wrapper to the ue_cell_search module for rf devices
 * Return 1 if the MIB is decoded, 0 if not or -1 on error.
 */
int rf_mib_decoder(srslte_rf_t*       rf,
                   uint32_t           nof_rx_channels,
                   cell_search_cfg_t* config,
                   srslte_cell_t*     cell,
                   float*             cfo)
{
  int                  ret = SRSLTE_ERROR;
  srslte_ue_mib_sync_t ue_mib;
  uint8_t              bch_payload[SRSLTE_BCH_PAYLOAD_LEN] = {};

  if (srslte_ue_mib_sync_init_multi(&ue_mib, srslte_rf_recv_wrapper_cs, nof_rx_channels, (void*)rf)) {
    fprintf(stderr, "Error initiating srslte_ue_mib_sync\n");
    goto clean_exit;
  }

  if (srslte_ue_mib_sync_set_cell(&ue_mib, *cell)) {
    ERROR("Error initiating srslte_ue_mib_sync\n");
    goto clean_exit;
  }

  int srate = srslte_sampling_freq_hz(SRSLTE_UE_MIB_NOF_PRB);
  INFO("Setting sampling frequency %.2f MHz for PSS search\n", (float)srate / 1000000);
  srslte_rf_set_rx_srate(rf, (float)srate);

  INFO("Starting receiver...\n");
  srslte_rf_start_rx_stream(rf, false);

  // Copy CFO estimate if provided and disable CP estimation during find
  if (cfo) {
    ue_mib.ue_sync.cfo_current_value       = *cfo / 15000;
    ue_mib.ue_sync.cfo_is_copied           = true;
    ue_mib.ue_sync.cfo_correct_enable_find = true;
    srslte_sync_set_cfo_cp_enable(&ue_mib.ue_sync.sfind, false, 0);
  }

  /* Find and decode MIB */
  ret = srslte_ue_mib_sync_decode(&ue_mib, config->max_frames_pbch, bch_payload, &cell->nof_ports, NULL);
  if (ret < 0) {
    ERROR("Error decoding MIB\n");
    goto clean_exit;
  }
  if (ret == 1) {
    srslte_pbch_mib_unpack(bch_payload, cell, NULL);
  }

  // Save CFO
  if (cfo) {
    *cfo = srslte_ue_sync_get_cfo(&ue_mib.ue_sync);
  }

clean_exit:

  srslte_rf_stop_rx_stream(rf);
  srslte_ue_mib_sync_free(&ue_mib);

  return ret;
}

int main(int argc, char** argv)
{
  int                           n;
  srslte_rf_t                   rf;
  srslte_ue_cellsearch_t        cs;
  srslte_ue_cellsearch_result_t found_cells[3];
  int                           nof_freqs;
  srslte_earfcn_t               channels[MAX_EARFCN];
  uint32_t                      freq;
  uint32_t                      n_found_cells = 0;
  //time_t ltime;

  struct timeval curTime;
  int milli;
  char buffer[80];
  char currentTime[84] = "";


  srslte_debug_handle_crash(argc, argv);

  parse_args(argc, argv);

  printf("Opening RF device...\n");
  if (srslte_rf_open(&rf, rf_args)) {
    ERROR("Error opening rf\n");
    exit(-1);
  }
  if (!cell_detect_config.init_agc) {
    srslte_rf_set_rx_gain(&rf, rf_gain);
  } else {
    printf("Starting AGC thread...\n");
    if (srslte_rf_start_gain_thread(&rf, false)) {
      ERROR("Error opening rf\n");
      exit(-1);
    }
    srslte_rf_set_rx_gain(&rf, 50);
  }

  // Supress RF messages
  srslte_rf_suppress_stdout(&rf);

  nof_freqs = srslte_band_get_fd_band(band, channels, earfcn_start, earfcn_end, MAX_EARFCN);
  if (nof_freqs < 0) {
    ERROR("Error getting EARFCN list\n");
    exit(-1);
  }

  sigset_t sigset;
  sigemptyset(&sigset);
  sigaddset(&sigset, SIGINT);
  sigprocmask(SIG_UNBLOCK, &sigset, NULL);
  signal(SIGINT, sig_int_handler);

  if (srslte_ue_cellsearch_init(&cs, cell_detect_config.max_frames_pss, srslte_rf_recv_wrapper, (void*)&rf)) {
    ERROR("Error initiating UE cell detect\n");
    exit(-1);
  }

  if (cell_detect_config.max_frames_pss) {
    srslte_ue_cellsearch_set_nof_valid_frames(&cs, cell_detect_config.nof_valid_pss_frames);
  }
  if (cell_detect_config.init_agc) {
    srslte_rf_info_t* rf_info = srslte_rf_get_info(&rf);
    srslte_ue_sync_start_agc(&cs.ue_sync,
                             srslte_rf_set_rx_gain_wrapper,
                             rf_info->min_rx_gain,
                             rf_info->max_rx_gain,
                             cell_detect_config.init_agc);
  }


while(!go_exit) {
n_found_cells=0;
  for (freq=0;freq<nof_freqs && !go_exit;freq++) {

    /* set rf_freq */
    srslte_rf_set_rx_freq(&rf, 0, (double)channels[freq].fd * MHZ);
    INFO("Set rf_freq to %.3f MHz\n", (double) channels[freq].fd * MHZ/1000000);

    /*printf(
        "[%3d/%d]: EARFCN %d Freq. %.2f MHz looking for PSS.\n", freq, nof_freqs, channels[freq].id, channels[freq].fd);
    fflush(stdout);*/

    //printf("\n");
    fflush(stdout);
    if (SRSLTE_VERBOSE_ISINFO()) {
      printf("\n");
    }

    bzero(found_cells, 3*sizeof(srslte_ue_cellsearch_result_t));

    INFO("Setting sampling frequency %.2f MHz for PSS search\n", SRSLTE_CS_SAMP_FREQ/1000000);
    srslte_rf_set_rx_srate(&rf, SRSLTE_CS_SAMP_FREQ);
    INFO("Starting receiver...\n");
    srslte_rf_start_rx_stream(&rf, false);
    //ltime=time(NULL);

    gettimeofday(&curTime, NULL);
    milli = curTime.tv_usec / 1000;
    strftime (buffer, 80, "%Y-%m-%d %H:%M:%S", localtime (&curTime.tv_sec));
    sprintf (currentTime, "%s:%03d", buffer, milli);
 /*   printf("%s",asctime( localtime(&ltime) ) );*/

    n = srslte_ue_cellsearch_scan(&cs, found_cells, NULL);
    if (n < 0) {
      ERROR("Error searching cell\n");
      exit(-1);
    } else if (n > 0) {
      for (int i=0;i<3;i++) {
        if (found_cells[i].psr > 2.0) {
          srslte_cell_t cell;
          cell.id = found_cells[i].cell_id;
          cell.cp = found_cells[i].cp;
          int ret = rf_mib_decoder(&rf, 1, &cell_detect_config, &cell, NULL);
          if (ret < 0) {
            ERROR("Error decoding MIB\n");
            exit(-1);
          }
          if (ret == SRSLTE_UE_MIB_FOUND) {
            /* printf("Found CELL ID %d. %d PRB, %d ports\n", cell.id, cell.nof_prb, cell.nof_ports);*/
            if (cell.nof_ports > 0) {
              results[n_found_cells].cell      = cell;
              results[n_found_cells].freq = channels[freq].fd;
              results[n_found_cells].dl_earfcn = channels[freq].id;
              results[n_found_cells].power = found_cells[i].peak;
              printf("Found CELL MHz, %.1f,  EARFCN, %d, PHYID, %d, PRB, %d,  ports, %d, PSS power dBm, %.1f,  PSR, %.1f \n",
               results[n_found_cells].freq,
               results[n_found_cells].dl_earfcn,
               results[n_found_cells].cell.id,
               results[n_found_cells].cell.nof_prb,
               results[n_found_cells].cell.nof_ports,
               10*log10(results[n_found_cells].power),
               found_cells[i].psr);
               //asctime( localtime(&ltime)));
               //currentTime);
              n_found_cells++;
            }
          }
        }
      }
    }
  }


 } /* while loop*/
  printf("\nBye\n");

  srslte_ue_cellsearch_free(&cs);
  srslte_rf_close(&rf);
  exit(0);
}
