#!/usr/bin/python
from __future__ import with_statement
import MySQLdb 
import os
from flask import Flask, request, session, g, redirect, url_for, \
		abort, render_template, flash

from werkzeug import secure_filename
from contextlib import closing

from CONFIG	import CONFIG

DEBUG = True
SECRET_KEY = 'development key'
UPLOAD_FOLDER = 'static/photo'
ALLOWED_EXTENSIONS = set(['jpg','png','jpeg'])

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def connect_db():
	con = MySQLdb.connect(
			host=CONFIG.HOST,
			user=CONFIG.USER,
			passwd=CONFIG.PASSWD,
			db=CONFIG.DB)
	return con.cursor()

@app.before_request
def before_request():
	g.db = connect_db()

@app.after_request
def after_request(response):
	g.db.close()
	return response

@app.route('/')
def show_entries():
	cur = g.db.execute('select id, photo_path, description, name from User where userid = %s order by id' % session['userid'])
	entries = [dict(userid=row[0], photo_path=row[1], description=row[2], name=row[3]) for row in g.db.fetchall()] 
	return render_template('show_entries.html', entries=entries)

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		sql = "select id from LoginUser where username='%s' and passwd='%s'" % (request.form['username'], request.form['password'])
		cur = g.db.execute(sql)
		print cur
		if cur == 0:
			error = "Invalid username or Invalid password"
		else:
			session['userid'] = g.db.fetchall()[0][0]
			flash("You were logged in")
			return redirect(url_for('show_entries'))
	return render_template('login.html', error = error)

@app.route('/logout')
def logout():
	session.pop('userid', None)
	flash('You were logged out')
	return redirect(url_for('login'))

def allowed_file(filename):
	return '.' in filename and \
			filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/showadd')
def show_add_entry():
	return render_template('add.html') 

@app.route('/add', methods=["GET", "POST"])
def add_entry():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			description = request.form['description']
			name = request.form['name']
			gender = request.form['gender']
			sql = "insert into User(userid,photo_path,\
					description,name,gender)values(%s,'photo/%s','%s','%s',%s)" \
					% (session['userid'],filename, description, name, gender)
			g.db.execute(sql)
		return redirect(url_for('show_entries'))
	return redirect(url_for('show_add_entry'))

@app.route('/editrelation')
def edit_relationship():
	cur = g.db.execute('select id,name from User where userid = %s' % session['userid'])
	members = g.db.fetchall()
	cur = g.db.execute('select id,name from User where gender = 0 and userid = %s' % session['userid'])
	men = g.db.fetchall()
	cur = g.db.execute('select id,name from User where gender = 1 and userid = %s' % session['userid'])
	women = g.db.fetchall()
	return render_template('relationship.html', members = members, men = men, women = women)

@app.route('/addrelationship', methods=["GET", "POST"])
def add_relationship():
	if request.method == 'POST':
		memberid = request.form['member']
		fatherid = request.form['father']
		motherid = request.form['mother']
		sql = "insert into Relationship(userid, fatherid, motherid)values( \
				%s, %s, %s)" % (memberid, fatherid, motherid)
		g.db.execute(sql)
		return redirect(url_for('show_entries'))
	return redirect(url_for('edit_relationship'))

@app.route('/showrelationship', methods=["GET", "POST"])
def show_relationship():
	userid = request.form["userid"]
	cur = g.db.execute("select name,photo_path,id from User where id = %s" % userid)
	li = []
	li1 = []
	li1.append(g.db.fetchall())
	g.db.execute("select fatherid, motherid from Relationship where userid = %s" % userid)
	recursion_parents(li, g.db.fetchall())
	li.append(li1)

	g.db.execute("select userid from Relationship where fatherid=%s or motherid=%s" % (userid,userid))
	recursion_children(li, g.db.fetchall())

	return render_template('show_relationship.html', relationships=li)

@app.route('/displayinfo/<userid>')
def display_userinfo(userid):
	cur = g.db.execute("select name, photo_path, description from User where id = %s" % userid)
	return render_template('user_info.html', usersinfo=g.db.fetchall())

def recursion_parents(lis, parents):
	li = []
	if parents == []:
		return
	_parents =[] 
	for parent in parents:
		for parentid in parent:
			g.db.execute("select name, photo_path, id from User where id = %s" \
				% parentid)
			li.append(g.db.fetchall())
			g.db.execute("select fatherid, motherid from Relationship where userid=%s" % parentid)
			_parents.append(g.db.fetchall())
	parents = [parent for sub_parents in _parents for parent in sub_parents]
	recursion_parents(lis, parents)
	lis.append(li)
	return lis

def recursion_children(lis, children):
	li = []
	if children == []:
		return
	_children = []
	for child in children:
		for childid in child:
			g.db.execute("select name, photo_path, id from User where id = %s" \
					% childid)
			li.append(g.db.fetchall())
			g.db.execute("select userid from Relationship where fatherid=%s or motherid=%s" % (childid,childid))
			_children.append(g.db.fetchall())
	lis.append(li)
	children = [child for sub_children in _children for child in sub_children]
	recursion_children(lis, children)
	return lis

#test
@app.route('/show/<username>')
def show(username):
	return username

if __name__ == '__main__':
	app.run()
