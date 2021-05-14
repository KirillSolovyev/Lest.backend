# Lest backed API. Django Advanced course project

# Lest - online retail app

Lest helps grossery shops to provider best customer experience. It allows to buy everything customers need on their own through smartphone and app.

- Customers scan goods' bar code and all info about it appears in the app. Then they can pay for goods in the app and leave store.

- With Lest grossery stores will offer omni channel shopping.

## This repository is backend API

- In the app a user can get info about product by barcode. Add it to cart and pay for it.

- Authentication is via JWT and one time password. The app uses custom user model (phone number as a username)

## Getting Started

```shell
For correct work you need to create virtual environment with python 3.6.2
```

```shell
pip install -r requirements.txt
```

```shell
python manage.py makemigrations
python manage.py migrate
```

```shell
python manage.py runserver
```