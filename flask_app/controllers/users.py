from flask_app import app
from flask import render_template,redirect,request,session,flash, url_for
from flask_app.models.user import User
from flask_app.models.show import Show
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                            # which is made by invoking the function Bcrypt with our app as an argumen

@app.route('/')
def index():
    print('index session', session)
    return render_template("index.html")

@app.route('/users/register', methods=['POST'])
def register():
    print('form', request.form)
    
    if not User.validate_user(request.form):
        return redirect(url_for('index'))
    # validate the form here ...
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    # put the pw_hash into the data dictionary
    data = {}
    for key, value in request.form.items():
        data[key] = value
    
    data['password'] = pw_hash    
    print('data', data)  
    # Call the save @classmethod on User
    user_id = User.insert_user(data)
    # store user id into session
    session['user_id'] = user_id
    session['first_name'] = data['first_name']
    session['logged_in'] = True
    return redirect(url_for("dashboard"))
        
@app.route('/users/login', methods=['POST'])
def login():
    cur_user = User.get_user_with_email(request.form['email'])
    print('cur_user', cur_user)
    if not cur_user or not bcrypt.check_password_hash(cur_user.password, request.form['password']):
        flash("Invalid email/password combination")
        return redirect(url_for('index'))
    
    session['user_id'] = cur_user.id
    session['first_name'] = cur_user.first_name
    session['logged_in'] = True
    return redirect(url_for("dashboard"))

@app.route('/users/dashboard')
def dashboard():
    print('session', session)
    if session['logged_in'] == True:
        liked_shows = Show.get_liked_shows(session['user_id'])
        not_liked_shows = Show.get_not_liked_shows(session['user_id'])
        return render_template('dashboard.html', liked_shows=liked_shows, not_liked_shows=not_liked_shows)
    return redirect(url_for('index'))

@app.route('/users/logout')
def logout():
    session['logged_in'] = False;
    return redirect(url_for('index'))
