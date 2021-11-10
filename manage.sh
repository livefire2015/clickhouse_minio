#!/bin/sh

argument=$1

if [ $argument = "up" ]; then
    echo "Creating infrastructure..."
    docker-compose up -d
    docker-compose -f superset/superset-service.yml up
elif [ $argument = "stop" ]; then
    echo "Stopping infrastructure..."
    docker-compose stop
elif [ $argument = "down" ]; then
    echo "Deleting infrastructure..."
    docker-compose down
elif [ $argument = "restart" ]; then
    echo "Restarting infrastructure..."
    docker-compose down
    docker-compose build
    docker-compose up -d
    docker-compose -f superset/superset-service.yml up
else
  echo "Unknown argumnet! Options: up, stop, down, restart"
fi