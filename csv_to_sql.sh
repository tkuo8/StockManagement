#!/bin/bash

symbols=$(cat output.txt)

TABLE_NAME="stocks"

sql=$(echo $symbols | awk -F',' '{for(i=1; i<=NF; i++) print "INSERT INTO '"$TABLE_NAME"' (symbol, purchase_price, quantity) VALUES (\047"$i"\047, 0, 0);"}' | head -n 10)

#echo $sql
echo $sql | sqlite3 ./backend/instance/stockManagement.sqlite
