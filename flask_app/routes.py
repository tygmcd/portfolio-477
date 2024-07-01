# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request, session, url_for, copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from .utils.database.database  import database
from .utils.chat.ChatUtil import ChatUtil
from werkzeug.datastructures  import ImmutableMultiDict
from pprint import pprint
import json
import random
import functools
from . import socketio
db = database()
chatUtil = ChatUtil()


#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function

def getUser():
	return db.reversibleEncrypt('decrypt', session['email']) if 'email' in session else 'Unknown'

def getRole():
	if 'email' in session:
		email = db.reversibleEncrypt('decrypt', session['email'])
		query = f"SELECT role FROM users WHERE users.email='{email}'"
		role_db = db.query(query)
		return role_db[0]['role']
	
def getAccounts():
	query = "SELECT email, role FROM users"
	return db.query(query)
		

@app.route('/login')
def login():
	return render_template('login.html', user=getUser())

@app.route('/logout')
def logout():
	session.pop('email', default=None)
	return redirect('/')

@app.route('/processlogin', methods = ["POST","GET"])
def processlogin():
	# Extract credentials into a dict
	form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))

	# Get email and encrypted password, authenticate them
	user_email = form_fields['email']
	encrypted_pw = db.onewayEncrypt(form_fields['password'])
	auth_result = db.authenticate(user_email, encrypted_pw)

	# if authentication sucesssful, set session email
	if auth_result["success"] == 1:
		session['email'] = db.reversibleEncrypt('encrypt', form_fields['email']) 
		
	return json.dumps(auth_result)


#######################################################################################
# CHATROOM RELATED
#######################################################################################
@app.route('/chat')
@login_required
def chat():
	print(chatUtil.users_online)
	return render_template('chat.html', user=getUser(), online=len(chatUtil.users_online))

@socketio.on('joined', namespace='/chat')
def joined(message):
	join_room('main')
	# adds to online count when a user joins (extra thing I added for fun)
	chatUtil.user_join(getUser())
	if getRole() == 'owner':
		style = chatUtil.owner_style
	else:
		style = chatUtil.guest_style
	
	emit('status', {'msg': getUser() + ' has entered the room.', 'online': len(chatUtil.users_online), 'style': style}, room='main')

@socketio.on('message-sent', namespace='/chat')
def sent(message):
	if getRole() == 'owner':
		style = chatUtil.owner_style
	else:
		style = chatUtil.guest_style
		
	emit('message-received', {'msg': getUser() + " said: " + message['msg'], 'style': style}, room='main')

@socketio.on('leave-room', namespace='/chat')
def leave(message):
	# subtracts from online count when a user joins (extra thing I added for fun)
	chatUtil.user_leave(getUser())
	if getRole() == 'owner':
		style = chatUtil.owner_style
	else:
		style = chatUtil.guest_style

	emit('status', {'msg': getUser() + ' has left the room.', 'online': len(chatUtil.users_online),  'style': style}, room='main')
	leave_room('main')
	

#######################################################################################
# OTHER
#######################################################################################
@app.route('/')
def root():
	return redirect('/home')

@app.route('/home')
def home():
	x = random.choice(['I am one of the guys who raises/lowers the field goal nets at Detroit Lions home games!',
					'I like to collect vinyl records!',
					'I am a big Michigan State sports fan!'])
	return render_template('home.html', user=getUser(), fun_fact = x)

@app.route('/projects')
def projects():
	return render_template("projects.html",  user=getUser())

@app.route('/projects/piano')
def piano():
	return render_template("piano.html",  user=getUser())

@app.route('/resume')
def resume():
	resume_data = db.getResumeData()
	return render_template('resume.html', resume_data = resume_data,  user=getUser())


@app.route('/processfeedback', methods = ['POST'])
def processfeedback():
	feedback = request.form
	fb_name = feedback['name']
	fb_email = feedback['email']
	fb_comment = feedback['comment']
	db.insertRows('feedback', ['name', 'email', 'comment'], [[fb_name, fb_email, fb_comment]])
	data = db.query("SELECT * FROM feedback")

	return render_template('processfeedback.html', data = data, user=getUser())

@app.route('/admin')
@login_required
def admin():
	if getRole() == 'owner':
		return render_template('admin.html', user=getUser(), accounts=getAccounts())
	return redirect(url_for("home"))

@app.route('/cleartable', methods = ['POST'])
def cleartable():
	data = request.form.to_dict()
	if 'feedback' in data and data['feedback'] == 'on':
		db.query('DELETE FROM feedback;')
		message = "Table cleared successfully"
	return render_template('admin.html', message=message, user=getUser())

@app.route('/manageaccounts', methods = ['POST'])
def manage_accounts():
	data = request.form.to_dict()
	for email in data:
		if data[email] == 'on' and email != getUser():
			db.query(f"DELETE FROM users WHERE email='{email}';")
	
	return render_template('admin.html', user=getUser(), accounts=getAccounts())

@app.route('/createaccount', methods = ['POST'])
def create_account():
	data = request.form.to_dict()
	res = db.createUser(data['email'], data['password'], 'guest')
	return render_template('admin.html', user=getUser(), accounts=getAccounts(), status=res['success'])

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r
