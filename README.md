# Reservation test
Small Django project to test a simple reservation system. (Django 2.2, Python 3.7)

## How to test?
Create a virtual environment.
```
python -m venv venv-test
```
Activate the venv on Windows.
```
venv-test\Scripts\activate.bat
```
Activate the venv on Linux.
```
source venv-test/bin/activate
```
Clone the project
```
git clone https://github.com/Harold-Kalvin/Reservation-test.git
```
Move to the directory "Reservation-test" (cd Reservation-test) and install the dependencies.
```
pip install -r requirements.txt
```
Move to the directory "reservation_test" (cd reservation_test) and compile the translation files.
```
python manage.py compilemessages
```
Run the development server.
```
python manage.py runserver
```

## Test users
- admin (username), best_password (password)
- user_test_1 (username), best_password (password)
- user_test_2 (username), best_password (password)