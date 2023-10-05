#!/usr/bin/python3

"""
This module contains a function that generates a .tgz archive from
the contents of the web_static folder.

Functions:
    do_pack: Generates a .tgz archive.
"""

from fabric.api import local
from datetime import datetime


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
