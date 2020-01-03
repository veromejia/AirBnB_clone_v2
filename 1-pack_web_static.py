#!/usr/bin/python3
""" Generates a .tgz archive from the contents of the web_static folder"""

from fabric.api import *
from datetime import datetime


def do_pack():
    """packs files into .tgz file"""
    tgz_file = 'versions/web_static_{}.tgz'\
        .format(datetime.strftime(datetime.now(), "%Y%m%d%I%M%S"))
    local("mkdir -p versions")
    new_file = local("tar -cvzf {} web_static".format(tgz_file))

    if new_file.succeeded:
        return tgz_file
    return None
