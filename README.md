# py-minter

Contracts and UI for a soulbound token creator

*WIP: working towards a hackathon starter kit and tutorial content*

## Tech stack

- Back-end: Ape, Solidity, Flask
- Front-end: Vite

## Setup

- install deps
- install foundry/anvil
- run anvil
- ape compile
- ape test
- ape run build --token 721
- ape run build --token 1155
- flask db init
- flask db migrate -m "init"
- flask db upgrade
- python server.py
- cd webapp && npm i
- npm run dev
- deploy contracts and mint tokens at localhost:5173

## Captains log

- new env, pip install eth-ape
- `ape init`
- basic solidity contract
- solidity + OZ ape config
- v5 OZ contract wizard starting point
- write SBT 721 and 1155 contracts
- write tests for sbt functionality
- build script that injects ABI and bytecode into webapp and server
- UI to deploy and mint tokens
- server with database to store deployments and token mints
