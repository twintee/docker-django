#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
from os.path import join, dirname, abspath, isfile, isdir
from dotenv import load_dotenv
import argparse

dir_scr = os.path.abspath(os.path.dirname(__file__))
sys.path.append(abspath(join(dir_scr, "..")))
import helper as fn

os.chdir(dir_scr)
file_env = os.path.join(dir_scr, ".env")

def main(_args):
    """
    initialize container
    """
    dk_cmd = "docker exec -it node-app-django"
    # コンテナ作成
    for line in fn.cmdlines(_cmd=f"{dk_cmd} python3 manage.py {_args.cmd}"):
        sys.stdout.write(line)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='set env params')
    parser.add_argument('cmd', help="execute manage.py args.")
    args = parser.parse_args()

    print("[info] initialize start.")
    main(args)
    print("[info] initialize end.")
