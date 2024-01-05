# checkpoints

AERPAW provides a set of tools that can be used to establish "checkpoints" for scripts.
These can be used to block execution on a node until a process on a different node completes.

The general structure is that a checkpoint server runs on one predetermined node.

* When a script wants to declare that it has reached a checkpoint, it will send a message to set a variable in the server.
* When a script wants to see if a checkpoint has been set, it retrieves the variable from a server.

By default, these variables have three types:

* `boolean` -> either true or false, set once
* `int` -> increments every time it is "set". starts at zero
* `string` -> holds arbitrary data

The server can be used to store arbitrary data using the string type, however there are no assertions made about performance.

## API

Examples of how to interface with the server can be seen in the provided bash or python scripts.

The API is designed to use HTTP POST and GET requests as follows:

* HTTP POST `http://server/bool/variable` -> sets boolean flag "variable" to true
* HTTP POST `http://server/int/variable` -> increments integer "variable" by 1
* HTTP POST `http://server/string/variable?val=set-value` -> sets value of string "variable" to val (in this case, "set-value")

* HTTP GET `http://server/bool/variable`
* HTTP GET `http://server/int/variable`
* HTTP GET `http://server/string/variable`

On GET reply, the server sends the data back as a raw value

CRITICALLY there is a way to reset all variables in the server by POSTing to:

* HTTP POST `http://server/reset` -> resets all variables to default values

By default, the server is launched on experiment startup, but values will be persistent.
The default E-VM launch scripts make a call to the above endpoint.
