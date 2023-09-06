# CallApp
Web application based on CRM and a Dialer using Django and MySQL

## Functionalities

- Log in
    - via username & password 
    - remind user
- Create an ccount
- Log out
- Profile activation via email
- Reset password
- Remind a username
- Resend an activation code




## Installing

### Clone the project

```bash
git clone https://github.com/danielostos21/CallApp.git
cd CallApp
```

### Install dependencies & activate virtualenv

#### Create a virtualenv 

```bash
python venv env
```

### Activate virtual enviroment 

Linux
```bash
source env/bin/activate
```
Windows
```bash
env/Scripts/activate
```



#### Install django

```bash
pip install django

```


### Apply migrations

```bash
python callapp/manage.py migrate
```

### Collect static files (only on a production server)

```bash
python callapp/manage.py collectstatic
```

### Running

#### A development server

Just run this command:

```bash
python callapp/manage.py runserver
```