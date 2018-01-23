## Installation instructions

1. Install Python3, pip, venv:<br>
$ `sudo apt install python3 python3-pip python3-venv`<br>
2. Clone this repository:<br>
$ `mkdir project`<br>
$ `cd ./project`<br>
$ `git clone https://github.com/trolleksii/django-test.git`<br>
3. Create a new virtual environment with Python 3 interpreter:<br>
$ `virtualenv -p python3 ./venv`<br>
4. Activate it:<br>
$ `source ./venv/bin/activate`<br>
6. Install required packages from requirements.txt:<br>
$ `pip install -r ./django-test/requirements.txt`<br>
7. `cd` into ./django-test/howismyteam:<br>
$ `cd ./django-test/howismyteam/`<br>
8. Perform database migrations:<br>
$ `python manage.py migrate`<br>
9. Install Google Chrome browser and Selenium webdriver:<br>
To run functional tests you will need [Google Chrome](https://www.google.com/chrome/) and a [webdriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) for selenium:<br>
$ `curl https://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip --create-dirs -o ~/.local/bin`<br>
10. Run tests to make sure that everything is working as it should:<br>
$ `python manage.py test`<br>
11. Create a superuser:<br>
$ `python manage.py createsuperuser`<br>
12. Run the project:<br>
$ `python manage.pu runserver`<br>
