import sys
import os
import requests

with open("A:\ctw\l.txt", "a") as f: f.write(f"{sys.argv}\n")

try: domain, target, val, apikey = sys.argv[1:]
except Exception as e: input(f"{e}\nTry again!"); exit()

# TODO: setup your DNS provider (apache libcloud etc)
requestsHeaders = {"User-Agent": "pydns", "domain": domain, "target": target, "value": val, "apikey": apikey}
r = requests.post("https://ns.aodd.xyz/manage/create", headers=requestsHeaders)
if r.status_code == 200: pass
else: print("ERROR")

# TODO: add/append the txt record
