"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import User, db, connect_db, asc, desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
#db.create_all()


@app.route("/")
def display_users():
    return redirect("/users", code=302)
#def display_home():
#    """Show homepage."""
#
#    return render_template("index.html")


@app.route('/users')
def list_users():
    """Renders directory of employees and phone numbers  (from dept)"""
    users = User.query.order_by(asc(User.last_name)).order_by(User.first_name).all()
    return render_template('users.html', users=users)

@app.route('/users/<userid>')
def user_detail(userid):
    """Renders individual user detail page"""
    user = User.query.get(userid)
    print (f"inside user_detail, userid = {userid}")
    return render_template('user_detail.html', user=user)

@app.route("/user_action/<userid>", methods=["POST"])
def user_action(userid):
    user = User.query.get(userid)
    which_button = request.form['edit_delete']
    print(f"Inside user_action, userid={userid}, request={which_button}")
    if (which_button == 'Edit'):
        return render_template('user_edit_form.html', user=user)
    else: #must be delete
        User.query.filter_by(id=userid).delete()
        db.session.commit()
        return redirect("/users", code=302)                   
    #print(request.form)
    #print(request.form['edit_delete'])
    #return render_template('user_detail.html', user=user)

@app.route("/user_edit/<userid>", methods=["POST"])
def save_user_edit(userid):
    user = User.query.get(userid)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    db.session.add(user)
    db.session.commit() 
    #print (request.form)
    return render_template('user_detail.html', user=user)

@app.route("/new_user_form")
def edit_new_user():
    return render_template('new_user_form.html')

@app.route("/add_user", methods=["POST"])
def create_new_user():
    user = User()

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit() 
    return render_template('user_detail.html', user=user)

    