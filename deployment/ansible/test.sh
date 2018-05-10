#!/usr/bin/env bash

uptime
echo "hello"

# run by
# ansible all -i hosts -m script -a shell.sh -u ubuntu --key-file=<key-file>
