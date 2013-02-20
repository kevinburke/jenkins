#!/usr/bin/env python

import argparse
import ConfigParser
import json
import os
import re
import subprocess
import sys
import webbrowser

from clint.textui import colored
import requests

def _get_remote_url(remote_name):
    """ Retrieve the remote URL from a remote name like 'upstream' """
    cmd = "git config --get remote.{}.url".format(remote_name)
    try:
        remote_url = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError:
        a = colored.red(
            "Couldn't find a remote named {}\n".format(remote_name))
        sys.stderr.write(str(a))
        sys.exit(1)
    return remote_url


def _parse_git_remote_url(url):
    """Parse Git remote URL's into a SRE_Match object

    Matches user@<hostname>:<web_user>/<user_repo>
    or      git://<hostname>/<web_user>/<user_repo>
    """
    ssh_regex = re.compile(r"""
                           ^(
                                (?P<git_user>\S+)@   # match user@ ssh url's
                                |
                                git://               # match git read-only url's
                           )
                           (?P<host>[^/:]+) # hostname
                           [:/]             # separator
                           (?P<user>[^/]+)
                           /
                           (?P<repo_name>.+?)
                           \.git$
                           """, re.X)
    return ssh_regex.match(url)


def _get_jenkins_host():
    config = ConfigParser.ConfigParser({'port': '80'})
    try:
        config.readfp(open(os.path.expanduser("~") + '/.jenkinsrc'))
    except IOError:
        print colored.red("""Error: Config file .sshboxrc not found.

Add your Jenkins URL configuration to a .jenkinsrc file like so:

[jenkins]
host = https://jenkins.mydomain.com
port = 80""")
        sys.exit(2)
    host = config.get('jenkins', 'host')
    port = config.get('jenkins', 'port')
    return host, port


def _get_git_branch():
    # If no branch provided, default to the current branch
    cmd = "git rev-parse --abbrev-ref HEAD"
    try:
        return subprocess.check_output(cmd, shell=True).strip('\n')
    except subprocess.CalledProcessError:
        sys.stderr.write(str(
            colored.red("An error occurred trying to get the "
                        "current git branch, command was {}".format(cmd))))
        sys.exit(1)


def _build_url(host, port, user, repo_name, branch):
    port_part = "" if port == "80" else ":" + port
    return host + port_part + "/job/{}.{}.{}".format(user, repo_name, branch)


def _get_latest_build_url(api_response, default=None):
    try:
        return api_response['lastBuild']['url'] + 'console'
    except KeyError:
        return default


def main():
    parser = argparse.ArgumentParser(description=
                                     "Open current build of a Jenkins job")
    parser.add_argument('remote_name', type=str, default='origin', nargs='?',
                        help="Name of the remote to open")
    parser.add_argument('-b', '--branch', type=str, default=None,
                        help="Git branch to open (defaults to current branch)")
    parser.add_argument('-j', '--job', action='store_true',
                        help="Open the job homepage, not the current build")
    args = parser.parse_args()

    remote_url = _get_remote_url(args.remote_name)
    match = _parse_git_remote_url(remote_url)
    host, port = _get_jenkins_host()
    branch = args.branch or _get_git_branch()
    base_url = _build_url(host, port, match.group('user'), match.group('repo_name'),
                     branch)

    r = requests.get(base_url + '/api/json')
    url = base_url if args.job else _get_latest_build_url(json.loads(r.content))
    webbrowser.open_new_tab(url)


if __name__ == "__main__":
    main()

