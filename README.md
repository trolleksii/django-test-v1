# How is My Team?
A simple Django application to allow daily checkins and monitoring of your teams happiness.

## Installation instructions

1. Install Python3, pip, venv:
`sudo apt install python3 python3-pip python3-venv`
2. Clone this repository:
```
mkdir project
cd ./project
git clone https://github.com/trolleksii/django-test.git
```
3. Create a new virtual environment with Python 3 interpreter:
 `virtualenv -p python3 ./venv`
4. Activate it:
 `source ./venv/bin/activate`
6. Install required packages from requirements.txt:
 `pip install -r ./django-test/requirements.txt`
7. `cd` into ./django-test/howismyteam:
 `cd ./django-test/howismyteam/`
8. Perform database migrations:
 `python manage.py migrate`
9. Install Google Chrome browser and Selenium webdriver:
To run functional tests you will need [Google Chrome](https://www.google.com/chrome/) and a [webdriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) for selenium:
`curl https://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip --create-dirs -o ~/.local/bin`
10. Run tests to make sure that everything is working as it should:
 `python manage.py test`


## Usage instructions

1. Create a superuser:
 `python manage.py createsuperuser`
2. Run the project:
 `python manage.py runserver`
3. Visit [project's webpage](http://localhost:8000) and login as a superuser.
4. Navigate to the admin page and add some **PollProfiles**(**User** field is mandatory, **Team** is optional, **happines** should be empty on creation or user will not be able to participate in the poll on that day) for users of the project
5. Relog as one of added users and participate in the poll
6. Check poll results

Users with **PollProfile** that have a team will see stats for their team only. All others will see stats for all users without a team. 
Users without **PollProfile** can't participate in the poll but still can see poll results for users without a team.
By design the user with **PollProfile** which hadn't participated in the poll that day, will not see the poll results.
