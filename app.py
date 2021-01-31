from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from flask_ckeditor import CKEditor
from werkzeug.security import generate_password_hash, check_password_hash
import yaml
import os

app = Flask(__name__)
Bootstrap(app)
CKEditor(app)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

app.config['SECRET_KEY'] = os.urandom(24)

@app.route("/")
def index():
	cur = mysql.connection.cursor()
	result = cur.execute("SELECT * FROM blog")
	if result > 0:
		blogs = cur.fetchall()
		cur.close()
		return render_template("index.html", blogs = blogs)
	cur.close()
	return render_template("index.html", blogs = None)

@app.route("/blogs/<int:id>/")
def blogs(id):
	cur = mysql.connection.cursor()
	result = cur.execute("SELECT * FROM blog WHERE blog_id = {}".format(id))
	if result > 0:
		blog = cur.fetchone()
		return render_template("blogs.html", blog = blog)
	return "Blog not found!"

@app.route("/register/", methods = ['GET', 'POST'])
def register():
	if request.method == "POST":
		userdetails = request.form
		if userdetails['password'] != userdetails['confirm_password']:
			flash("Passwords do not match!", "danger")
			return render_template("register.html")
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO user(first_name,last_name,username,email,password) values(%s,%s,%s,%s,%s)", (userdetails['first_name'],userdetails['last_name'],\
			userdetails['username'],userdetails['email'],generate_password_hash(userdetails['password'])))
		mysql.connection.commit()
		cur.close()
		flash("Registration successful! Please login.", "success")
		return redirect("/login")
	return render_template("register.html")

@app.route("/login/", methods = ["GET", "POST"])
def login():
	if request.method == "POST":
		userdetails = request.form
		username = userdetails['username']
		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * FROM user WHERE username = %s",[username])
		if result > 0:
			user = cur.fetchone()
			if check_password_hash(user['password'], userdetails['password']):
				session['login'] = True
				session['firstname'] = user['first_name']
				session['lastname'] = user['last_name']
				flash("Welcome " + session['firstname'] + " ! You have been successfully logged in.", "success")
				return redirect("/")
			else:
				cur.close()
				flash("Passwords do not match.", "danger")
				return render_template("login.html")
		else:
			cur.close()
			flash("User not found.","danger")
			return render_template("login.html")
	return render_template("login.html")

@app.route("/write-blog/", methods = ["GET", "POST"])
def write_blog():
	if session.get('firstname') is not None:
		if request.method == "POST":
			blogpost = request.form
			title = blogpost['title']
			body = blogpost['body']
			author = session['firstname'] + " " + session['lastname']
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO blog(title, body, author) VALUES(%s,%s,%s)",(title,body,author))
			mysql.connection.commit()
			cur.close()
			flash("Successfully posted new blog!","success")
			return redirect("/")
		return render_template("write-blog.html")
	else:
		flash("First login please!", "danger")
		return redirect("/login/")

@app.route("/my-blogs/")
def my_blogs():
	if session.get('firstname') is not None:
		author = session['firstname'] + " " + session['lastname']
		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * FROM blog WHERE author = %s",[author])
		if result > 0:
			my_blogs = cur.fetchall()
			return render_template("my-blogs.html", my_blogs = my_blogs)
		else:
			return render_template("my-blogs.html", my_blogs = None)
	else:
		flash("First login please!", "danger")
		return redirect("/login/")

@app.route("/edit-blog/<int:id>/", methods = ["GET", "POST"])
def edit_blog(id):
	if request.method == "POST":
		cur = mysql.connection.cursor()
		title = request.form['title']
		body = request.form['body']
		cur.execute("UPDATE blog SET title = %s, body = %s where blog_id = %s", (title, body, id))
		mysql.connection.commit()
		cur.close()
		flash("Blog updated successfully.", "success")
		return redirect("/blogs/{}".format(id))
	cur = mysql.connection.cursor()
	result = cur.execute("SELECT * FROM blog WHERE blog_id = {}".format(id))
	if result > 0:
		blog = cur.fetchone()
		blog_form = {}
		blog_form['title'] = blog['title']
		blog_form['body'] = blog['body']
		return render_template("edit-blog.html", blog_form=blog_form)

@app.route("/delete-blog/<int:id>", methods = ["GET", "POST"])
def delete_blog(id):
	cur = mysql.connection.cursor()
	cur.execute("DELETE FROM blog WHERE blog_id = {}".format(id))
	mysql.connection.commit()
	flash("Your blog has been deleted." , "success")
	return redirect("/")

@app.route("/logout/")
def logout():
	session.clear()
	flash("You have been logged out!", "info")
	return redirect("/")

if __name__ == '__main__':
	app.run(debug = True)