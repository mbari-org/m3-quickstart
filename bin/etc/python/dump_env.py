#! /usr/bin/env python

import os
import pprint
import shlex
import subprocess
import sys

env_file = sys.argv[1]
print(f"Reading env file: {env_file}")
cmd = f"env -i bash -c 'source {env_file}'"
command = shlex.split(cmd)
proc = subprocess.Popen(command, stdout = subprocess.PIPE)
for line in proc.stdout:
  (key, _, value) = line.partition("=")
  print(f"{key} = {value}")
  os.environ[key] = value
proc.communicate()

pprint.pprint(dict(os.environ))