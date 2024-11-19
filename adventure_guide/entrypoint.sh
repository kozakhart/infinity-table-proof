#!/bin/bash

GREY='\x1b[90m'
RESET='\x1b[0m'

PORT=${PORT:-8080}

uvicorn main:app --host 0.0.0.0 --port $PORT
