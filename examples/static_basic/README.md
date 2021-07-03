# Example using Basic authentication
```sh
pip install -r requirements
pip install gunicorn
gunicorn --reload service:api 
```
and browse
```
http://raphaeljoie:Passw0rd@localhost:3000/users
```
or execute the following request
```
GET /users
Host: localhost:3000
Authorization: Basic cmFwaGFlbGpvaWU6UGFzc3cwcmQ= 
```
