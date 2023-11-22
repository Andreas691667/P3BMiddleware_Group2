# P3BMiddleware_Group2

This project implements the classic game of Pong as a distributed system. 
The game is implemented using the client-server architecture, where the server is responsible for the game logic and the clients are responsible for the user interface.

To run the game, open a terminal and run the following command:
```bash
python3 server.py
```
This will start the server and wait for two clients to connect.
Then, open another terminal and run the following command:
```bash
python3 client.py q a
```
This will start the client and connect it to the server. This client moves up on 'q' and down on 'a'.
In a third terminal, run the following command:
```bash
python3 client.py o l
```
This will start the second client and connect it to the server. This client moves up on 'o' and down on 'l'.