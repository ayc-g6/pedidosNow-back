#!/bin/bash
# IMPORTANT: before running this script ensure to run heroku login!!!!

set -e

# heroku login

APP_NAME=pedidosnow-back

heroku apps:create $APP_NAME
heroku addons:create heroku-postgresql:hobby-dev --app $APP_NAME