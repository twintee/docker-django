#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import argparse
from os.path import join, dirname, abspath, isfile, isdir

dir_scr = abspath(dirname(__file__))
import helper as fn

os.chdir(dir_scr)
file_env = os.path.join(dir_scr, ".env")

def main(_args):
    """
    initialize container
    """

    params = fn.getenv(file_env)

    # コンテナ削除
    if not _args.debug:
        for line in fn.cmdlines(_cmd="docker-compose down -v"):
            sys.stdout.write(line)

    # ログリセット
    fn.rmdir(join(dir_scr, "log"))

    # ソースリセット
    fn.rmdir(join(dir_scr, "src"))

    dir_project = join(dir_scr, "src")

    if not isdir(dir_project):
        if params['GIT_REPO'] == "":
            # templateをコピー
            dir_template = join(dir_scr, "django", "project")
            params['APP_NAME_PASCAL'] = str(params['APP_NAME']).capitalize()
            fn.copydir(dir_template, dir_project, params)
            fn.rmdir(join(dir_project, "app"), True)
            fn.copydir(join(dir_template, "app"), join(dir_project, params['APP_NAME']), params)
            fn.rmdir(join(dir_project, "templates", "app"), True)
            fn.copydir(join(dir_template, "templates", "app"), join(dir_project, "templates", params['APP_NAME']), params)

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

    # コンテナ作成
    if not _args.debug:
        if fn.input_yn("start https-portal container? (y/*) :"):
            for line in fn.cmdlines(_cmd=f"docker-compose up -d"):
                sys.stdout.write(line)
        else:
            for line in fn.cmdlines(_cmd=f"docker-compose up -d web"):
                sys.stdout.write(line)


    # django前処理
    if params['GIT_REPO'] == "":
        docker_cmd = "docker exec -it node-app-django"
        for line in fn.cmdlines(_cmd=f"{docker_cmd} python3 ./manage.py makemigrations"):
            sys.stdout.write(line)
        for line in fn.cmdlines(_cmd=f"{docker_cmd} python3 ./manage.py migrate"):
            sys.stdout.write(line)
        for line in fn.cmdlines(_cmd=f"{docker_cmd} python3 ./manage.py createsuperuser"):
            sys.stdout.write(line)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='set config files')
    parser.add_argument('--debug', '-d', help="reset files", action="store_true")
    args = parser.parse_args()

    _input = input("initialize container. ok? (y/*) :").lower()
    if not _input in ["y", "yes"]:
        print("[info] initialize canceled.")
        sys.exit()

    print("[info] initialize start.")
    main(args)
    print("[info] initialize end.")
