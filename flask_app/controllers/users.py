from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.post import Post
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# HTML Template to login or register

@app.route('/loginPage')
def loginPage():
    if 'user_id' in session:
        return redirect('/')
    return render_template('loginRegister.html')


#POST Method to create a User ex. Register

@app.route('/createUser', methods=['POST'])
def createUser():
    if not User.validate_user(request.form):
        flash('Somethings wrong ninja!', 'signUp')
        return redirect(request.referrer)
    
    if User.get_user_by_email(request.form):
        flash('My friend, this email already exists! What are you trying to do?!! Hack me?!', 'emailSignUp')
        return redirect(request.referrer)
    data = {
        'email': request.form['email'],
        'name': request.form['name'],
        'lastName': request.form['lastName'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    User.create_user(data)
    return redirect('/')


#POST method to log the user in

@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    if len(request.form['email'])<1:
        flash('Email is required to login', 'emailLogin')
        return redirect(request.referrer)
    if not User.get_user_by_email(data):
        flash('This email doesnt exist in this application', 'emailLogin')
        return redirect(request.referrer)

    user = User.get_user_by_email(data)

    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        # if we get False after checking the password
        flash("Invalid Password", 'passwordLogin')
        return redirect(request.referrer)
        
    session['user_id'] = user['id']
    return redirect('/')

# Route to display the main page 

@app.route('/')
def dashboard():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        user = User.get_user_by_id(data)
        allPosts = Post.getAllPosts()
        userLikedPosts = User.get_logged_user_liked_posts(data)
        return render_template('dashboard.html', loggedUser= user, allPosts = allPosts, userLikedPosts= userLikedPosts)
    return redirect('/logout')


#Route to display a specific user information

@app.route('/profile/<int:id>')
def profile(id):
    if 'user_id' in session:
        data = {
            'user_id': id
        }
        user = User.get_user_by_id(data)
        posts = User.get_all_user_info(data)
        return render_template('profile.html', posts= posts, user= user)
    return redirect('/logout')

#Route to log the user out -- Clean the session

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/loginPage')