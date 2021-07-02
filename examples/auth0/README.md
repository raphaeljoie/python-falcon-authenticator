# Example using Auth0
Browse on [auth0.com](https://auth0.com/), create an Application, and fill the
client ID + oAuth domain in service.py. Then run
```sh
pip install -r requirements
pip install gunicorn
gunicorn --reload service:api 
```
