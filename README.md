# Pinocchio's Pizza & Subs

This Django-based pizza restaurant app featuring a cart with purchasing through Stripe. It features an admin interface to edit menu items and view pending orders. Users can add items to their cart and view their pending and past orders.

## Set-up

Set-up a virtual environment and activate it:

```bash
python3 -m venv env
source env/bin/activate
```

You should see (env) before your command prompt now. (You can type `deactivate` to exit the virtual environment any time.)

Install the requirements:

```bash
pip install -U pip
pip install -r requirements.txt
```

Create a Stripe account and obtain api keys [here](https://stripe.com/)

Set up your environment variables:

```bash
touch .env
echo DOMAIN="XXX" >> .env
echo STRIPE_SECRET_KEY="sk_test_XXX" >> .env
echo STRIPE_PUBLIC_KEY="pk_test_XXX" >> .env
```

## Usage

Make sure you are in the virtual environment (you should see (env) before your command prompt). If not `source /env/bin/activate` to enter it.

```bash
Usage: manage.py runserver
```

A sqlite database has been included with the repo. The admin interface can be accessed at `/admin` and the default admin username:password is `admin:Pinocchio`.

## Screenshots

![Pinocchio's Pizza & Subs Menu Page](https://i.imgur.com/eDEOi1T.png)

![Pinocchio's Pizza & Subs Cart Page](https://i.imgur.com/WZ0EM1P.png)

![Pinocchio's Pizza & Subs Orders Page](https://i.imgur.com/2d1GFTO.png)

## Credit

[HarvardX: CS50's Web Programming with Python and JavaScript](https://www.edx.org/course/cs50s-web-programming-with-python-and-javascript)

## License

Pinocchio's Pizza & Subs is licensed under the [MIT license](https://github.com/danrneal/pinocchios-pizza-and-subs/blob/master/LICENSE).
