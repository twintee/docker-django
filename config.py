#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from os.path import join, dirname, abspath, isfile, isdir
import shutil
import argparse
from urllib.parse import urlparse

dir_scr = dirname(abspath(__file__))
# sys.path.append(join(dir_scr, ".."))
import helper as fn

dir_scr = dirname(abspath(__file__))

def main(_args):
    print("----- redis env setting start.")

    env_org = join(dir_scr, "_org", '.env')
    env_file = join(dir_scr, '.env')
    nconf_org = join(dir_scr, "_org", 'default.conf')
    nconf_dst = join(dir_scr, "nginx", 'default.conf')
    netrc_org = join(dir_scr, "_org", '.netrc')
    netrc_dst = join(dir_scr, "django", '.netrc')

    if _args.reset or not isfile(env_file):
        print("[info] init .env file.")
        shutil.copyfile(env_org, env_file)

    params = fn.getenv(env_file)

    fn.setparams(params, [
        'TZ',
        'APP_NAME',
        'APP_DOMAIN',
        'APP_PORT',
    ])

    if fn.input_yn("get app source from git? (y/*) :"):
        fn.setparams(params, [
            'GIT_USER',
            'GIT_TOKEN',
            'GIT_REPO',
            'GIT_BRANCH',
        ])
    if fn.input_yn("use mysql databases? (y/*) :"):
        fn.setparams(params, [
            'MYSQL_MASTER_HOST',
            'MYSQL_MASTER_PORT',
            'MYSQL_SLAVE_HOST',
            'MYSQL_SLAVE_PORT',
            'MYSQL_USER_PASSWORD',
        ])

    if fn.input_yn("use redis caches? (y/*) :"):
        fn.setparams(params, [
            'REDIS_MASTER_HOST',
            'REDIS_MASTER_PORT',
            'REDIS_MASTER_PASSWORD',
        ])

    fn.setenv(params, env_file)
    fn.update_file(params, nconf_org, "___", nconf_dst)

    # netrcファイル作成
    if params['GIT_REPO'] == "":
        dir_app = join(dir_scr, "src", "app")
        if not isdir(dir_app):
            fn.mkdir(dir_app, True)
            shutil.copytree(
                join(dir_scr, "django", "template"),
                join(dir_scr, "src"))
            # fn.update_file(params,
            #         join(dir_scr, "django", "settings.py"),
            #         "___",
            #         join(dir_scr, "src", "app", "settings.py"))
            # fn.update_file(params,
            #         join(dir_scr, "django", "db_router.py"),
            #         "___",
            #         join(dir_scr, "src", "app", "db_router.py"))
    else:
        # URLをパースする
        params['GIT_DOMAIN'] = urlparse(params['GIT_REPO']).netloc.replace("www.", "")
        fn.update_file(params, netrc_org, "___", netrc_dst)

    for k,v in params.items():
        print(f"{k}={v}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='set config files')
    parser.add_argument('--reset', '-r', help="reset files", action="store_true")
    args = parser.parse_args()

    main(args)
