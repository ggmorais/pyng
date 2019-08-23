import os

while True:
    host = os.system('ping.exe -n 1 google.com | FIND "TTL="')
