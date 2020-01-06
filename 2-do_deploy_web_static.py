#!/usr/bin/python3
"""distributes an archive to your web servers,
using the function do_deploy"""


from fabric.api import *
from os import path

env.hosts = ['35.243.173.73', '34.74.64.12']


def do_deploy(archive_path):
    """Deploys the archive into the servers"""
    if not path.exists(archive_path):
        return False

    upload_file = put(archive_path, '/tmp/')
    if upload_file.failed:
        return False

    full_file = archive_path.split("/")[-1]
    my_file = full_file.split(".")[0]

    run("mkdir -p /data/web_static/releases/{}/".format(my_file))
    run("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/".
        format(my_file, my_file))

    run("rm /tmp/{}.tgz".format(my_file))

    run("mv /data/web_static/releases/{}/web_static/* "
        "/data/web_static/releases/{}/".format(my_file, my_file))
    run("rm -rf /data/web_static/releases/{}/web_static".
        format(my_file))
    run("rm -rf /data/web_static/current")
    run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
        format(my_file))
    print("New version deployed!")
    return True
