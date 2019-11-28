  <h3 align="center">E-parking web application</h3>


## Table of Contents

- [Table of Contents](#table-of-contents)
- [About The Project](#about-the-project)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [admin](#admin)
  - [parking bookings related](#parking-bookings-related)
  - [User management related](#user-management-related)
- [Contact](#contact)



<!-- ABOUT THE PROJECT -->
## About The Project

![](https://i.ibb.co/mvK5m3H/cars-details.png)

System supporting the management of parking spaces and parkings named E-Parking. It is intended to use as a server application for multiple parkings databases. App communicate  with devices via REST API. 

Application consists of three main components:
* [Mobile application for parking customers](https://github.com/mateusz58/Google_MAPS.git)
* web application for parking managers and system administrators
* Server used for communication with the database

Most notable application features:
* adding and removing parkings from database
* booking a reservation for chosen parking for a limited period of time
* management of system users(only for system administrator)
* booking managment is restricted only for one parking per user
* system allows to set a personalized price for each parking
* it is possible to register more than one parking place at once for many cars on one parking
* 

Project relational table data structure:

![](https://i.ibb.co/6tgwTrS/realtional-Table.png)


### Built With
* [Django Framework](https://www.djangoproject.com/)
* [Django REST Framework](https://www.django-rest-framework.org/api-guide/renderers/)
* [MySql](https://www.mysql.com)
* [django background task](https://django-background-tasks.readthedocs.io/en/latest/)
* [django allauth](https://django-allauth.readthedocs.io/en/latest/)
* [django-admin-range-filter](https://github.com/silentsokolov/django-admin-rangefilter)
* [django admin totals](https://github.com/douwevandermeij/admin-totals.git)
* [django url filter](https://github.com/miki725/django-url-filter)

## Getting Started

### Prerequisites

* Make sure Python 3.6x and Pipenv are already installed. See here for help.

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
4. Load website at  http://127.0.0.1:8000

<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

## API Reference

### Admin panel url

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
- `api/v1/car_booking/logged/<int:pk>`<br>  display detailed  informations about booking based on id for logged user
  
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

## Contact

  - Email:  matp321@gmail.com

- Project Link: [https://github.com/mateusz58/Parking_Server.git](https://github.com/your_username/repo_name)

[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=flat-square
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=flat-square
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=flat-square
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=flat-square
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=flat-square
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
