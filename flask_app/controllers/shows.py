from flask_app import app
from flask import render_template,redirect,request,session,flash, url_for
from flask_app.models.show import Show
from flask_app.models.like import Like
from flask_app.models.user import User

@app.route('/shows/<int:id>')
def display_show(id):
    if session['logged_in'] == True:
        show = Show.get_show_with_id(id)
        num_likes = Like.get_num_likes_of_show(id)
        poster_name = User.get_user_name_with_show_id(id)
        return render_template('show.html', show=show, num_likes=num_likes, poster_name=poster_name)
    return redirect(url_for('index'))

@app.route('/shows/new')
def new_show():
    if session['logged_in'] == True:
        return render_template('edit_show.html', title='Add New Show', form_function='add', show=Show.get_dummy_show())
    return redirect(url_for('index'))

@app.route('/shows/edit/<int:id>')
def edit_show(id):
    if session['logged_in'] == True:
        return render_template('edit_show.html', title='Edit ', form_function='update', show=Show.get_show_with_id(id))
    return redirect(url_for('index'))

@app.route('/shows/delete/<int:id>')
def delete_show(id):
    Like.delete_like_with_show_id(id)
    Show.delete_show(id)
    return redirect(url_for('dashboard'))

@app.route('/shows/add', methods=['POST'])
def add_show():
    print('/shows/add  form', request.form)
    
    if not Show.validate_show(request.form):
        return redirect(url_for('new_show'))
    
    # Call the save @classmethod
    show_id = Show.insert_show(request.form)
    print('inserted show:', show_id)
    return redirect(url_for("dashboard"))

@app.route('/shows/update', methods=['POST'])
def update_show():
    print('form', request.form)
    
    if not Show.validate_show(request.form):
        return redirect(url_for('edit_show', id=request.form['id']))
    
    # Call the update @classmethod
    Show.update_show(request.form)
    return redirect(url_for("dashboard"))
