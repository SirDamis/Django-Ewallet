# WaPay

WaPay is an online wallet that allows you to send and receive you receive payments reliably and instantly. 

WaPay is built using Python's Django framework.

## SetUp

Clone the project and navigate into the project directory.
```bash
git clone https://github.com/SirDamis/Django-Ewallet.git
cd Django-Ewallet
```

Activate the virtual environment  
```bash
pip install --user pipenv
pipenv shell
```


Install the dependencies.

```bash
pip install -r requirements.txt
```

## Run the application
Migrate the database using the command

```bash
python manage.py makemigrations

python manage.py migrate
```
Create your copy of the env file 
```
cp .env.example .env 
``` 

Start the server using the command
```bash
python manage.py runserver
```
Starting development server at http://127.0.0.1:8000/
## Run the test suites
Run the test cases using the pytest command
```bash
pytest
```
## Functionalities
* User Management
  * Registration
  * Login/Logout
  * Change Password
* Transaction Management
  * Fund wallet using your card
  * Withdraw from wallet to your account
  * Send and Receive Money from Wallet
  * View Transaction History



## Live URL
This project is hosted on heroku. Click this [link](https://github.com) to access the website


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)