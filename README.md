# Realms Royale Server

This repo is part of the Realms Royale hackathon project.

Code is for the trusted server for storing the data of coordinates and unit id. It provides the following features:

- Storing the data of a player joining a royale lobby, returning player id to the client
- Storing a composed random seed, and private key when 3 players have joined. Setting the session parameters for the game
- Return the unit id when a there is a player encounter
- Calculating the movable coordinates in the game and returning them to the client
- Provide the public key to be stored on Starknet, verifying the private key on the server
