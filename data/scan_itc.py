#! /usr/bin/env python

import fnmatch
import os

# Find all .itc files
matches = []
for root, dirnames, filenames in os.walk('./'):
  for filename in fnmatch.filter(filenames, '*.itc'):
      matches.append(os.path.join(root, filename))

for match in matches:
    with open(match, 'r') as itcfile:
        ninj = int(itcfile.readlines()[1].split()[1])

        if ninj == 10:
            print match
