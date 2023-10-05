#!/usr/bin/python3
"""
This module contains functions that generate a .tgz archive from the contents
of the web_static folder and distribute it to web servers.

Functions:
    do_pack: Generates a .tgz archive.
    do_deploy: Distributes an archive to web servers.
    deploy: Creates and distributes an archive to web servers.
"""
from fabric.api import env, put, run, local, task, runs_once
from os.path import exists
from datetime import datetime

# List of hosts to deploy to
env.hosts = ['100.26.177.153', '54.87.239.21']
# Set the username
env.user = 'ubuntu'
# Set the path to the SSH private key file
env.key_filename = '/root/.ssh/id_rsa'


@runs_once
def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    The function creates a 'versions' directory if it doesn't exist,
    then creates a .tgz archive of the 'web_static'
    directory with a timestamped filename. The archive is stored in
    the 'versions' directory.

    Returns:
        str: The path to the created archive
        (e.g., 'versions/web_static_20220314133030.tgz') if the archive was
        created successfully, or None if an error occurred.
    """

    # Create the versions directory if it doesn't exist
    local("mkdir -p versions")

    # Create a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "versions/web_static_{}.tgz".format(timestamp)

    # Use the tar command to create a .tgz archive of the web_static directory
    result = local("tar -cvzf {} web_static".format(filename))

    # If the command was successful, return the name of the file.
    # Otherwise, return None.
    if result.succeeded:
        return filename
    else:
        return None


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


@task
def deploy():
    """
    Creates and distributes an archive to web servers.

    The function calls do_pack() function and stores the path of created
    archive.
    If no archive has been created, it returns False.
    Then it calls do_deploy(archive_path) function using new path of
    new archive.

    Returns:
         bool: True if all operations were successful, or False if no
         archive was created or an error occurred.
    """
    # Call do_pack() function and store path of created archive
    path = do_pack()

    # Return False if no archive has been created
    if path is None:
        return False

    # Call do_deploy(archive_path) function using new path of new archive
    return do_deploy(path)
