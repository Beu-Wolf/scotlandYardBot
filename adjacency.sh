#!/bin/bash

if [ $# -ne 1 ]
  then
    echo "Usage: $0 <vertex>"
    exit
fi
cat listAdjacent.txt | grep "^${1} : "
