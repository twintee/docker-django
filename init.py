#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
from os.path import join, dirname, abspath, isfile, isdir
from dotenv import load_dotenv

dir_scr = abspath(dirname(__file__))
import helper as fn

os.chdir(dir_scr)
file_env = os.path.join(dir_scr, ".env")

def main():
    """
    initialize container
    """

    params = fn.getenv(file_env)

    # コンテナ削除
    # for line in fn.cmdlines(_cmd="docker-compose down -v"):
    #     sys.stdout.write(line)

    # ログリセット
    fn.rmdir(join(dir_scr, "log"))

    # ソースリセット
    fn.rmdir(join(dir_scr, "src"))

    dir_project = join(dir_scr, "src")

    if not isdir(dir_project):
        if params['GIT_REPO'] == "":
            # templateをコピー
            dir_template = join(dir_scr, "django", "project")
            fn.copydir(dir_template, dir_project, params)
        else:
            # gitからリポジトリクローン
            gituser = params['GIT_USER']
            if "gitlab" in params['GIT_REPO']:
                print("[info] clone from gitlab.")
                gituser = "oauth2"
            clone_url = params['GIT_REPO'].replace("://", f"://{gituser}:{params['GIT_TOKEN']}@")
            cmd = f"git clone"
            if params['GIT_BRANCH'] != "":
                cmd += f" -b {params['GIT_BRANCH']}"
            cmd += f" {clone_url} {dir_project}"
            for line in fn.cmdlines(_cmd=cmd):
                sys.stdout.write(line)
            # 内部でgitの更新できるようnetrc作成
            netrc_path = join(dir_scr, "django", ".netrc")
            if isfile(netrc_path):
                cmd = f"docker cp {netrc_path} node-app-django:/root"
                for line in fn.cmdlines(_cmd=cmd):
                    sys.stdout.write(line)

    if fn.input_yn("start https-portal container? (y/*) :"):
        # コンテナ作成
        for line in fn.cmdlines(_cmd=f"docker-compose up -d web"):
            sys.stdout.write(line)
    else:
        # コンテナ作成
        for line in fn.cmdlines(_cmd=f"docker-compose up -d"):
            sys.stdout.write(line)


if __name__ == "__main__":

    _input = input("initialize container. ok? (y/*) :").lower()
    if not _input in ["y", "yes"]:
        print("[info] initialize canceled.")
        sys.exit()

    print("[info] initialize start.")
    main()
    print("[info] initialize end.")
