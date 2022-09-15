#!/bin/bash

mkdir data
cd data
echo ".save ./chat.db" | sqlite3 -batch

