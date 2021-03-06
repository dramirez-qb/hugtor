#!/bin/sh

tor > /tmp/torlogs 2>&1 &

echo "Waiting tor to launch on 9051..."

while ! nc -z localhost 9051; do   
  sleep 0.5 # wait for 1/2 of the second before check again
done

echo "tor launched"

exec "$@"
