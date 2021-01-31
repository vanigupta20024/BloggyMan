# BloggyMan

_**A Flask based application for blogging and implementing CRUD through UI by MySql.**_

This application has been made using python flask, MySql, Html, Bootstrap. Functionalities include:

- Writing a blog
- Editing/Updating a blog post
- Deleting a blog
- Session based user activity
- Password hashing (so not visible in database)
- Viewing blogs written by other bloggers

### To run the application:
* Create a database `flog`
* Create tables `blog` and `user`
* For `blog` table use command:
```
CREATE TABLE blog(blog_id int auto_increment, title varchar(100), author varchar(40), body varchar(1000), primary key(blog_id));
```
* For `user` table use command:
```
CREATE TABLE user(user_id int auto_increment, first_name varchar(20), last_name varchar(20), 
username varchar(20) unique, email varchar(30) unique, password varchar(100), primary key(user_id));
```
* Update `db.yaml` file, set `mysql_password` by replacing `*****` with your MySql client password.
* Run the app: `python app.py`.

### Screenshots:
Following are some screenshots of the application while running.

#### Home page:
![Home Page](https://github.com/vanigupta20024/BloggyMan/blob/main/images/capture1.PNG)

#### Login page:
![Login](https://github.com/vanigupta20024/BloggyMan/blob/main/images/capture2.PNG)

#### Write blog page:
![Write Blog](https://github.com/vanigupta20024/BloggyMan/blob/main/images/capture3.PNG)

#### Blog viewing page:
![Blog](https://github.com/vanigupta20024/BloggyMan/blob/main/images/capture4.PNG)

#### Hashed passwords in database:
![Hashed passwords](https://github.com/vanigupta20024/BloggyMan/blob/main/images/capture5.PNG)

### Todo:
- [x] Session handling
- [x] Can only write blog if authenticated/logged in
- [ ] Deployment on Heroku with database
- [x] Password hashing in the database
