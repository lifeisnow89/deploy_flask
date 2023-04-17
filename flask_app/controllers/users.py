from flask import Flask, flash, render_template,redirect,request,session
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.wine_model import Wine
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('login_reg.html')


@app.route('/create', methods=['POST'])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash,

    }
    id = User.save(data)
    session['user_id'] = id
    return redirect("/main")

@app.route('/login',methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    user = User.get_by_email(data)
    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    return redirect('/main')


#end login controllers

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/main')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    all_wines = Wine.get_all()
    print("Gregory printing all wines")
    print(all_wines)
    return render_template('main.html', all_wines = all_wines)

@app.route('/new')
def new():
    return render_template('new.html')

@app.route('/view_wine_page/<int:wines_id>')
def view_wine(wines_id):
    if 'user_id' not in session:
        return redirect('/')
    print(Wine.get_wine_w_user(wines_id))
    return render_template("view_wine_page.html", wine = Wine.get_wine_w_user(wines_id))

@app.route('/delete/<int:wines_id>')
def delete(wines_id):
    Wine.delete({"wines_id":wines_id})
    if 'user_id' not in session:
        return redirect('/')
    return redirect('/main')

@app.route('/new_wine', methods=['POST'])
def save():
    if not Wine.validate_wine(request.form):
        return redirect('/new')
    if 'user_id' not in session:
        return redirect('/')
    print(request.form)
    Wine.save(request.form)
    return redirect('/main')

#edit controllers

@app.route('/edit/<int:wine_id>', methods=['POST'])
def update(wine_id):
    if not Wine.validate_wine(request.form):
        return redirect('/edit')
    if 'user_id' not in session:
        return redirect('/main')
    print(request.form, "*" * 50)
    Wine.update(request.form)
    return redirect('/main')


@app.route('/edit/<int:wine_id>')
def edit(wine_id):
    if 'user_id' not in session:
        return redirect('/')
    wine = Wine.get_one_w_user(wine_id)
    print("I'm printing wine name for testing")
    print(wine.wine_name)
    return render_template('edit.html', wine_in_html = wine)


@app.route('/my_wine_page/')
def view_my_wine():
    if 'user_id' not in session:
        return redirect('/')
    user_id = session['user_id']
    wines = Wine.get_wine_w_user(user_id)
    print('This is me printing more wine')
    print(wines)
    return render_template("my_wine_page.html", wines = wines)

