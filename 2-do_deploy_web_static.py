#!/usr/bin/python3

"""
This module contains a function that distributes an archive to web servers.

Functions:
    do_deploy: Distributes an archive to web servers.
"""

from fabric.api import env, put, run
from os.path import exists

# List of hosts to deploy to
env.hosts = ['100.26.177.153', '54.87.239.21']


def do_deploy(archive_path):
    """
    Distributes an archive to web servers.

    The function checks if the archive file exists and if it does,
    it uploads the file to /tmp/ on the web servers,
    uncompresses it to /data/web_static/releases/, deletes the archive
    from /tmp/, deletes any existing symbolic
    link at /data/web_static/current, and creates a new symbolic link
    at /data/web_static/current that points to
    the new version of your code.

    Args:
        archive_path (str): The path to the archive file.

    Returns:
        bool: True if all operations were successful, or False if the archive
        file doesn't exist or an error occurred.
    """

    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Uncompress the archive to the folder /data/web_static/releases/
        # on the web server
        filename = archive_path.split("/")[-1]
        name = filename.split(".")[0]

        releases_path = "/data/web_static/releases"

        run("mkdir -p {}/{}/".format(releases_path, name))
        run("tar -xzf /tmp/{} -C {}/{}/".format(filename, releases_path, name))

        # Move files from 'web_static' subdirectory to parent directory
        run("mv {}/{}/web_static/* {}/{}/".format(releases_path,
                                                  name,
                                                  releases_path,
                                                  name))

        # Remove 'web_static' subdirectory
        run("rm -rf {}/{}/web_static".format(releases_path, name))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(filename))

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current on the web
        # server, linked to the new version of the code
        run("ln -s {}/{}/ /data/web_static/current".format(releases_path,
                                                           name))

        return True
    except Exception:
        return False
