#!/usr/bin/env python3
# SPDX-License-Identifier: MIT

# Script to update the url and sha of the package
# example usage: ./update.py kdstatemachineeditor-qt5.rb v2.0.0

import argparse, os
import hashlib

# Returns the url of the tar.gz
def get_url(filename) -> str:
    try:
        with open(filename, 'r') as f:
            for line in f:
                if 'url' in line.lower():
                    url = line.split('"')[1]  # Extract URL between quotes
                    return url
    except Exception as e:
        print(f"Error reading file: {e}")
        exit(1)

    print("Could not find url in file")
    exit(1)

# Returns the sha256 of the .tar.gz file
def get_tarball_sha256(url):
    tar_filename = "/tmp/temp.tar.gz"
    os.system(f'curl -L -o {tar_filename} {url}')

    sha256_hash = hashlib.sha256()
    with open(tar_filename, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256_hash.update(chunk)

    os.remove(tar_filename)
    return sha256_hash.hexdigest()

def update(filename, new_tag):
    url = get_url(filename)

    # set the new url
    url = url.rsplit('/', 1)[0] + '/' + new_tag + '.tar.gz'
    sha = get_tarball_sha256(url)

    with open(filename, 'r') as f:
        content = f.read()

    content = content.replace(content.split('url "')[1].split('"')[0], url)
    content = content.replace(content.split('sha256 "')[1].split('"')[0], sha)

    with open(filename, 'w') as f:
        f.write(content)

parser = argparse.ArgumentParser()
parser.add_argument('filename', help="filename to diagnose")
parser.add_argument('tag', help="tag to diagnose for")
args = parser.parse_args()

script_dir = os.path.dirname(os.path.abspath(__file__))

full_path = os.path.abspath(args.filename)
if not full_path.startswith(script_dir) or not os.path.exists(args.filename):
    print("Error: File '%s' must be inside the script directory" % args.filename)
    exit(1)

update(args.filename, args.tag)
