# RAGGI AI-Oracle

more text will be added soon...

# Installation

## Backend

create a virtual env

> python -m venv venv

install all packages

> pip install -r requirements.txt

run following command to run the dev server

> fastapi dev

## Frontend

navigate to **frontend/raggi** folder and following command to install all packages needed:

> npm install

then run following command to run the dev server:

> quasra dev

# Settings

## Environments

1. add an .env file inside **rag** folder that contains Setting for Langfuse:

   - SECRET_KEY
   - PUBLIC_KEY
   - LANGFUSE_HOST

2. add also an .env file in side **frontend/raggi** folder for the setting of the UI:

   - API="http://ip-adress-of-api:port"
