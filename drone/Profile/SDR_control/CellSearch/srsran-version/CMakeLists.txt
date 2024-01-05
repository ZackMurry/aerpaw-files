cmake_minimum_required(VERSION 3.10)

project(
  "cell_search"
  VERSION 0.1.0 
  LANGUAGES C CXX
)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/modules/")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wno-comment -Wno-write-strings -Wno-unused-result -Wformat -Wmissing-field-initializers -Wtype-limits -std=c99 -fno-strict-aliasing -D_GNU_SOURCE")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-switch -Wno-unused-variable -Wno-return-type -Wno-sign-compare -Wno-reorder -Wno-parentheses -fno-exceptions")


find_library(srsranphy srsran_phy)
message(STATUS "${srsranphy}")
if (NOT srsranphy)
  message(FATAL_ERROR "SRS RAN PHY not found")
else()
  message(STATUS "Looking for SRS RAN PHY - found")
#  add_definitions(-DSRSRAN_ENV)
endif()

add_definitions(-DSRSRAN_ENV)


find_package(UHD)
if(UHD_FOUND)
  include_directories(${UHD_INCLUDE_DIRS})
  link_directories(${UHD_LIBRARY_DIRS})
endif(UHD_FOUND)

find_package(FFTW3F REQUIRED)
if(FFTW3F_FOUND)
  include_directories(${FFTW3F_INCLUDE_DIRS})
  link_directories(${FFTW3F_LIBRARY_DIRS})
  if(BUILD_STATIC)
    set(FFT_LIBRARIES "${FFTW3F_STATIC_LIBRARIES}")
  else(BUILD_STATIC)
    set(FFT_LIBRARIES "${FFTW3F_LIBRARIES}")
  endif(BUILD_STATIC)
  message(STATUS "FFT_LIBRARIES: " ${FFT_LIBRARIES})
endif(FFTW3F_FOUND)

#################################################################
# Linking Libs after locating them
#################################################################

add_definitions(-DSRSRAN_ENV)

add_executable(${PROJECT_NAME} cell_search.c)
target_link_libraries(${PROJECT_NAME} srsran_phy srsran_common srsran_rf m pthread stdc++ ${FFTW3F_STATIC_LIBRARIES})

