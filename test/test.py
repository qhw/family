from flask import Flask,url_for, render_template, session, redirect, escape, request, flash
app = Flask(__name__)

@app.route('/user/<username>')
def hello_world(username):
	return 'hello world' + username

@app.route('/')
def index():
	flash('hello world')
	if 'username' in session:
		return 'Loggede in as %s' % escape(session['username'])
	return 'You are not logged in'

@app.route('/login', methods=['POST', 'GET'])
def login():
	error = None
	if request.method == 'POST':
		session['username'] = request.form['username']
		return redirect(url_for('index'))
	return '''
		<form action="" method="post">
			<p><input type=text name=username>
			<p><input type=submit value=Login>
		</form>'''

@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('index'))

app.secret_key = 'A0Zr98j/3j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/user/<username>')
def profile(username):pass

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html', name=name)

with app.test_request_context():
	print url_for('index')
	print url_for('login')
	print url_for('login',next='/')
	print url_for('profile', username='John Doe')

if __name__ == '__main__':
	app.run()
