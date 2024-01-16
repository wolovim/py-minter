# py-minter

User interface for a generic soulbound token creator.

## Tech stack

- Back-end: solidity, flask
- Front-end: next.js

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

## Captains log

- new env, pip install eth-ape
- `ape init`
- basic solidity contract
- solidity + OZ ape config
- fix v5 errors from contract wizard
- write SBT 721 and 1155 tokens
- build script that injects ABI and bytecode into webapp and server
- UI to deploy and mint tokens
- server with database to store deployments and token mints
