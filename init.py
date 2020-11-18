#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
from os.path import join, dirname, abspath, isfile, isdir
from dotenv import load_dotenv

dir_scr = os.path.abspath(os.path.dirname(__file__))
import helper as fn

os.chdir(dir_scr)
file_env = os.path.join(dir_scr, ".env")

def main():
    """
    initialize container
    """

    params = fn.getenv(file_env)

    # コンテナ削除
    for line in fn.cmdlines(_cmd="docker-compose down -v"):
        sys.stdout.write(line)

    # ログリセット
    fn.rmdir(join(dir_scr, "log"))

    # ソースリセット
    fn.rmdir(join(dir_scr, "src"))

    # コンテナ作成
    for line in fn.cmdlines(_cmd=f"docker-compose up -d"):
        sys.stdout.write(line)

    docker_exec = "docker exec -it node-app-django"

    dir_app = join(dir_scr, "src", params['APP_NAME'])
    if not isdir(dir_app):
        if params['GIT_REPO'] == "":
            cmd = f"{docker_exec} django-admin startproject {params['APP_NAME']} ."
            for line in fn.cmdlines(_cmd=cmd):
                sys.stdout.write(line)
        else:
            # gitからリポジトリクローン
            gituser = params['GIT_USER']
            netrc_path = join(dir_scr, "django", ".netrc")
            if isfile(netrc_path):
                cmd = f"docker cp {netrc_path} node-app-django:/root"
                for line in fn.cmdlines(_cmd=cmd):
                    sys.stdout.write(line)
            if "gitlab" in params['GIT_REPO']:
                print("[info] clone from gitlab.")
                gituser = "oauth2"
            clone_url = params['GIT_REPO'].replace("://", f"://{gituser}:{params['GIT_TOKEN']}@")
            cmd = f"{docker_exec} git clone {clone_url} {params['APP_NAME']}"
            if params['GIT_BRANCH'] != "":
                cmd = f"{docker_exec} git clone -b {params['GIT_BRANCH']} {clone_url} {params['APP_NAME']}"
            for line in fn.cmdlines(_cmd=cmd):
                sys.stdout.write(line)

if __name__ == "__main__":

    _input = input("initialize container. ok? (y/*) :").lower()
    if not _input in ["y", "yes"]:
        print("[info] initialize canceled.")
        sys.exit()

    print("[info] initialize start.")
    main()
    print("[info] initialize end.")
