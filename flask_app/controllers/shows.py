from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.show import Show
from flask_app.models.user import User


@app.route('/new/show')
def new_show():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('new_tv_show.html')

@app.route('/create/show', methods=['POST'])
def create_show():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Show.validate_show(request.form):
        return redirect('/new/show')
    data = {
        "title": request.form["title"],
        "network": request.form["network"],
        "release_date": request.form["release_date"],
        "description": request.form["description"],
        "user_id": session["user_id"]
    }
    Show.save(data)
    return redirect('/dashboard')

@app.route('/edit/show/<int:id>')
def edit_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    return render_template("edit_tv_show.html",edit=Show.get_one(data))

@app.route('/update/show/<int:id>', methods=['POST'])
def update_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Show.validate_show(request.form):
        return redirect(f'/edit/show/{id}')
    data = {
        "id": id,
        "title": request.form["title"],
        "network": request.form["network"],
        "release_date": request.form["release_date"],
        "description": request.form["description"],
    }
    Show.update(data)
    return redirect('/dashboard')

@app.route('/show/<int:id>')
def view_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    return render_template("show_tv_show.html",show=Show.get_one(data),user=User.get_poster_of_show(data))

@app.route('/destroy/show/<int:id>')
def destroy_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Show.destroy(data)
    return redirect('/dashboard')