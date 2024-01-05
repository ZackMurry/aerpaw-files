import argparse
from typing import Tuple
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class JSONStore:
    def __init__(self, file_store_name: str="datastore.json"):
        self._file_name = file_store_name
        try:
            self.load()
        except FileNotFoundError:
            self._int_vars = {}
            self._bool_vars = {}
            self._string_vars = {}

    def save(self):
        with open(self._file_name, 'w') as f:
            json.dump({
                "ints": self._int_vars,
                "bools": self._bool_vars,
                "strings": self._string_vars,
            }, f)

    def load(self):
        with open(self._file_name, 'r') as f:
            try:
                ds = json.load(f)
                self._int_vars = ds["ints"]
                self._bool_vars = ds["bools"]
                self._string_vars = ds["strings"]
            except Exception as e:
                # just clear everything
                print("unable to load datastore -- resetting all values")
                self.reset()

    def inc_int_var(self, var_name: str):
        if var_name not in self._int_vars:
            self._int_vars[var_name] = 1
            return
        self._int_vars[var_name] += 1
        self.save()

    def get_int_var(self, var_name: str) -> int:
        if var_name not in self._int_vars:
            return 0
        return self._int_vars[var_name]

    def set_bool_var(self, var_name: str):
        self._bool_vars[var_name] = True
        self.save()
    
    def get_bool_var(self, var_name: str) -> bool:
        if var_name not in self._bool_vars:
            return False
        return self._bool_vars[var_name]

    def set_string_var(self, var_name: str, value: str):
        self._string_vars[var_name] = str(value)
        self.save()
    
    def get_string_var(self, var_name: str) -> str:
        if var_name not in self._string_vars:
            return ""
        return self._string_vars[var_name]
    
    def reset(self):
        self._int_vars = {}
        self._bool_vars = {}
        self._string_vars = {}
        self.save()

global_store: JSONStore = None

class Handler(BaseHTTPRequestHandler):
    def _set_response_ok(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
    
    def _set_response_server_error(self):
        self.send_response(500)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def _set_response_user_error(self):
        self.send_response(400)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def _parse_path(self, path_str: str) -> Tuple[str, str]:
        # returns (endpoint_type, variable_name)
        path = str(path_str)
        # need to parse out query part of string, if present
        path = path.split("?")[0]
        path_parts = path.split("/")[1:]

        # handle special case for reset endpoint
        if (len(path_parts) == 1 and path_parts[0] == "reset"):
            return "reset", None

        if (len(path_parts) != 2) or (path_parts[0] not in ["bool", "int", "string"]):
            return None, None
        return path_parts[0], path_parts[1]

    def do_GET(self):
        global global_store
        
        # check to make sure path is valid format (described in readme)
        endpoint_type, var_name = self._parse_path(self.path)
        if var_name == None:
            self._set_response_user_error()
            return
        # get variable from store
        value = None
        if endpoint_type == "bool":
            value = global_store.get_bool_var(var_name)
        elif endpoint_type == "int":
            value = global_store.get_int_var(var_name)
        elif endpoint_type == "string":
            value = global_store.get_string_var(var_name)

        # reply
        self._set_response_ok()
        self.wfile.write(str(value).encode())

    def do_POST(self):
        global global_store

        # check to make sure path is valid format (described in readme)
        endpoint_type, var_name = self._parse_path(self.path)
        if endpoint_type == None:
            self._set_response_user_error()
            return

        if endpoint_type == "reset":
            global_store.reset()
            self._set_response_ok()
            return
        
        # set variable from store
        if endpoint_type == "bool":
            global_store.set_bool_var(var_name)
        elif endpoint_type == "int":
            global_store.inc_int_var(var_name)
        elif endpoint_type == "string":
            # get query string value
            q_split = str(self.path).split("?")
            if len(q_split) != 2:
                self._set_response_user_error()
                return
            query_str = q_split[1]
            qs = query_str.split("&")
            val_set = False
            for q in qs:
                kv = q.split("=")
                if len(kv) != 2:
                    self._set_response_user_error()
                    return
                if kv[0] == "val":
                    global_store.set_string_var(var_name, kv[1])
                    val_set = True
                    break
            if not val_set:
                self._set_response_user_error()
                return
        
        self._set_response_ok()

def run_http_server(port=12434):
    server_address = ('', port)
    httpd = HTTPServer(server_address, Handler)
    try:
        httpd.serve_forever()
    except Exception as e:
        pass
    httpd.server_close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--store_filename", default="datastore.json", required=False, help="file to write datastore to")
    args = parser.parse_args()

    datastore_file = args.store_filename
    global_store = JSONStore(datastore_file)

    run_http_server()