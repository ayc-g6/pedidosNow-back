#!/bin/bash

cp .env.example .env
docker build .
docker-compose up -d