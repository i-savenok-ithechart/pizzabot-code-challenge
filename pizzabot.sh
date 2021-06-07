#!/bin/sh

echo "Searching for docker image..."
if [[ "$(sudo docker images -q pizzabot-router-8493f4a6-07cd-42ae-ab9f-f0dbb06f23df)" == "" ]]; then
  echo "Image does not exists, building..."
  sudo docker build . -t pizzabot-router-8493f4a6-07cd-42ae-ab9f-f0dbb06f23df
fi
  echo "Running \"python pizzabot.py $1\":"

  sudo docker run --rm pizzabot-router-8493f4a6-07cd-42ae-ab9f-f0dbb06f23df "$1"
