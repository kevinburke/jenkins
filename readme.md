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
