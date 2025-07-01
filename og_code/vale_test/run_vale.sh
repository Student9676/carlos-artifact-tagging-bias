#!/bin/sh

touch tmp/vale_input.txt
touch tmp/vale_output.json

vale_command=$(vale --output JSON tmp/vale_input.txt)

echo ${vale_command} >| 'tmp/vale_output.json'
