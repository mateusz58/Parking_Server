

![js-standard-style](https://img.shields.io/badge/code%20style-Google_Style-brightgreen.svg?style=flat)
![js-standard-style](https://img.shields.io/badge/build-passing-green)
![js-standard-style](https://img.shields.io/badge/release-v1.0.0-blue)
![js-standard-style](https://img.shields.io/badge/license-MIT-green)


<img src="https://i.ibb.co/C8W65x9/Screenshot-6.png" width = 200 align="right" />

# E-Parking space and parkings online manager
## Table of Contents

- [E-Parking space and parkings online manager](#e-parking-space-and-parkings-online-manager)
  - [Table of Contents](#table-of-contents)
  - [About The Project](#about-the-project)
    - [Built With](#built-with)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [API Reference](#api-reference)
    - [Admin panel](#admin-panel)
    - [Parking bookings related](#parking-bookings-related)
    - [User management related](#user-management-related)
  - [License](#license)
  - [Contact](#contact)

<!-- ABOUT THE PROJECT -->
## About The Project

![](https://i.ibb.co/mvK5m3H/cars-details.png)

System supporting the management of parking spaces and parkings named E-Parking. It is intended to use as a server/client application for multiple parkings bookings. App communicate with devices via REST API. Three types of users implemented in system are:
* MobileAppUser — these group of users can log in only to mobile application where it is possible to search whole set of parkings added to database and reserve parking place for a limited period on a choses parking. Database resources for this user limit to bookings which user added to database by registering parking place.
* ParkingManager — these group of users can log in only to web application. Database resources regarding bookings are restricted only to those which concern one parking which is ascribed to user.
* Admin — these group of users can log in only to web application. They have full control of database resources which means that they can perfrom all CRUD operations on each database record.

Application consists of three main components:

* [Mobile application for parking customers](https://github.com/mateusz58/Google_MAPS.git)
* web application for parking managers and system administrators
* Backend server used for communication with the database

Most notable application features:
* adding and removing parkings from database
* booking a reservation for chosen to park for a limited period
* management of system users(only for system administrator)
* booking management is restricted only for one parking per user
* system allows to set a personalized price for each parking
* it is possible to register more than one parking place at once for many cars on one parking for each car registration number is identificator

### Built With
* [Django Framework](https://www.djangoproject.com/)
* [Django REST Framework](https://www.django-rest-framework.org/api-guide/renderers/)
* [MySql](https://www.mysql.com)
* [django background task](https://django-background-tasks.readthedocs.io/en/latest/)
* [django allauth](https://django-allauth.readthedocs.io/en/latest/)
* [django-admin-range-filter](https://github.com/silentsokolov/django-admin-rangefilter)
* [django admin totals](https://github.com/douwevandermeij/admin-totals.git)
* [django url filter](https://github.com/miki725/django-url-filter)

### Prerequisites

* [Python 3.6x](https://www.python.org/downloads/release/python-360/)
* [Pip](https://pypi.org/project/pip/)
* [pipenv](https://github.com/pypa/pipenv)
* [Django](https://www.djangoproject.com/)
### Installation

1. Clone the repo and configure the virtualenv:
```sh
$ git clone https://github.com/wsvincent/djangox.git
$ cd djangox
$ pipenv install
$ pipenv shell
```
2. Set up initial migration for users and bookings
```sh
(djangox) $ python manage.py makemigrations users
(djangox) $ python manage.py migrate
(djangox) $ python manage.py makemigrations pages
(djangox) $ python manage.py migrate
```
3. Create a superuser
```sh
(djangox) $ python manage.py createsuperuser
```
4. Load website at http://127.0.0.1:8000

<!-- USAGE EXAMPLES -->

## API Reference

### Admin panel

  - `admin/*` administration panel for managing parkings

### Parking bookings related

- `api/v1/parking`<br> display/add/delete/modify all parkings stored in database
- `api/v1/parking/search$`<br> display parkings based on given parameter
- `api/v1/parking/<int:pk>`<br> display/delete/modify parking based on id
- `api/v1/booking/logged`<br> diplay all bookings of single user
- `api/v1/booking/logged/<int:pk>`<br> diplay/delete/modify all bookings of single user
- `api/v1/booking/`<br> display all bookings
- `api/v1/car_booking/logged/`<br> display all detailed bookings of user
- `api/v1/car_booking`<br> display all bookings in detail
- `api/v1/car_booking/logged/<int:pk>`<br> display detailed informations about booking based on id for logged user
  
  ### User management related

- `api/v1/registration_custom/` <br>
  add user to database
- `accounts-rest/registration/account-confirm-email/(?P<key>.+)/$` <br>
 activation link to activate user
- `api-token-auth/` log user to to system and return token for authorization
- `api/users` display/delete all users
- `api/rest-auth/logout/` log out user from system 
- `api/users/<int:pk>` search/delete/modify user based on id
- `api/users/search$` search user based on email

## License

[MIT](https://tldrlegal.com/license/mit-license)

## Contact

  - Email:  matp321@gmail.com

- Project Link: [https://github.com/mateusz58/Parking_Server.git](https://github.com/your_username/repo_name)

