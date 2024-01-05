import requests
import time

DEFAULT_QUERY_DELAY = 1
DEFAULT_PORT = 12434
DEFAULT_HOST = "127.0.0.1"

def _build_request(var_type: str, var_name: str, port: int, host: str) -> str:
    if var_type not in ["string", "bool", "int"]:
        return None
    return f"http://{host}:{port}/{var_type}/{var_name}"

def reset_checkpoint_server(port: int=DEFAULT_PORT, host: str=DEFAULT_HOST):
    response = requests.post(f"http://{host}:{port}/reset")
    if response.status_code != 200:
        raise Exception("error when resetting checkpoint server")

def set_checkpoint(checkpoint_name: str, port: int=DEFAULT_PORT, host: str=DEFAULT_HOST):
    response = requests.post(_build_request("bool", checkpoint_name, port, host))
    if response.status_code != 200:
        raise Exception("error when posting to checkpoint server")

def check_checkpoint(checkpoint_name: str, port: int=DEFAULT_PORT, host: str=DEFAULT_HOST) -> bool:
    response = requests.get(_build_request("bool", checkpoint_name, port, host))
    if response.status_code != 200:
        raise Exception("error when getting from checkpoint server")
    response_content = response.content.decode()
    if response_content == "True":
        return True
    elif response_content == "False":
        return False
    raise Exception(f"malformed content in response from server: {response_content}")

def wait_for_checkpoint(checkpoint_name: str, query_delay: int=DEFAULT_QUERY_DELAY, port: int=DEFAULT_PORT, host: str=DEFAULT_HOST):
    # blocks until checkpoint is set
    while not check_checkpoint(checkpoint_name, port, host):
        time.sleep(query_delay)

def increment_counter(counter_name: str, port: int=DEFAULT_PORT, host: str=DEFAULT_HOST):
    response = requests.post(_build_request("int", counter_name, port, host))
    if response.status_code != 200:
        raise Exception("error when posting to checkpoint server")

def check_counter(counter_name: str, port: int=DEFAULT_PORT, host: str=DEFAULT_HOST) -> int:
    response = requests.get(_build_request("int", counter_name, port, host))
    if response.status_code != 200:
        raise Exception("error when getting from checkpoint server")
    response_content = response.content.decode()
    try:
        return int(response_content)
    except TypeError:
        raise Exception(f"malformed content in response from server: {response_content}")

def set_string(string_name: str, value: str, port: int=DEFAULT_PORT, host: str=DEFAULT_HOST):
    response = requests.post(_build_request("string", string_name, port, host) + f"?val={value}")
    if response.status_code != 200:
        raise Exception("error when posting to checkpoint server")

def check_string(string_name: str, port: int=DEFAULT_PORT, host: str=DEFAULT_HOST) -> int:
    response = requests.get(_build_request("string", string_name, port, host))
    if response.status_code != 200:
        raise Exception("error when getting from checkpoint server")
    response_content = response.content.decode()
    return response_content

# if __name__ == "__main__":
#     # just for testing
#     reset_checkpoint_server()
    
#     assert check_checkpoint("test_checkpoint") == False
#     set_checkpoint("test_checkpoint")
#     assert check_checkpoint("test_checkpoint") == True

#     assert check_counter("test_counter") == 0
#     increment_counter("test_counter")
#     increment_counter("test_counter")
#     increment_counter("test_counter")
#     assert check_counter("test_counter") == 3

#     assert check_string("test_string") == ""
#     set_string("test_string", "some_value")
#     assert check_string("test_string") == "some_value"
#     set_string("test_string", "another_value")
#     assert check_string("test_string") == "another_value"