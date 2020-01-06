#!/usr/bin/python3
"""Fabric script (based on the file 2-do_deploy_web_static.py) that creates
and distributes an archive to your web servers, using the function deploy:"""


from fabric.api import *
from datetime import datetime
from os import path

env.hosts = ['35.243.173.73', '34.74.64.12']


def do_pack():
    """packs files into .tgz file"""
    tgz_file = 'versions/web_static_{}.tgz'\
        .format(datetime.strftime(datetime.now(), "%Y%m%d%I%M%S"))
    local("mkdir -p versions")
    new_file = local("tar -cvzf {} web_static".format(tgz_file))

    if new_file.succeeded:
        return tgz_file
    return None


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


def deploy():
    """Create and distribute an archive to a web server."""
    archive = do_pack()
    if not archive:
        return False
    return do_deploy(archive)
