# Open Jenkins urls

### Getting started

1. Clone this repo

        git clone git@github.com:kevinburke/jenkins.git

2. Install it

        cd jenkins
        python setup.py develop

3. Configure your Jenkins URL location

        echo "[jenkins]" >> ~/.jenkinsrc
        echo "host = http://jenkins.mydomain.com" >> ~/.jenkinsrc
        echo "port = 7777" >> ~/.jenkinsrc

4. View unit tests after you push code

        cd /path/to/project
        jenkins

Will open up the latest test run in your browser.

### Usage

    $ jenkins -h
    usage: jenkins [-h] [-b BRANCH] [-j] [remote_name]

    Open current build of a Jenkins job

    positional arguments:
      remote_name           Name of the remote to open

    optional arguments:
      -h, --help            show this help message and exit
      -b BRANCH, --branch BRANCH
                            Git branch to open (defaults to current branch)
      -j, --job             Open the job homepage, not the current build
