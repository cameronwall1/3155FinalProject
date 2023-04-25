from flask import Flask, render_template, url_for, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash



db = SQLAlchemy()
DB_NAME = "database.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)

class Movie (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column (db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, id, data, user_id):
        self.id = id
        self.data = data
        self.user_id = user_id

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column (db.String(150), unique=True)
    password = db.Column (db.String(150))
    firstname = db.Column (db.String (150))
    movies = db.relationship('Movie')

    def __init__(self, email, password, firstname):
        self.email = email
        self.password = password
        self.firstname = firstname
        # self.movies = movies

@app.before_first_request
def create_tables():
    db.create_all()




@app.route('/', methods = ['GET', 'POST'])
def index ():
    return render_template("index.html")

@app.route('/login', methods = ['GET', 'POST'])
def login ():
    # if request.method == 'POST':
    #     email = request.form.get('users-email')
    #     password = request.form.get('users-password')
        
    #     user = User.query.filter_by(email = email).first()
    #     if user:
    #         if check_password_hash(user.password, password):
    #             return render_template('movies.html', content = "True")

    return render_template('login.html')

@app.route('/movies', methods = ['GET', 'POST'])
def movies ():
    return render_template('movies.html')

@app.route('/reviewers', methods = ['GET', 'POST'])
def revieweres ():
    return render_template('reviewers.html')

@app.route('/login/signup/createaccount', methods = ['GET', 'POST'])
def singupuser ():

    validinformation = False

    if request.method == 'POST':
        email = request.form.get("users-email")
        firstname = request.form.get('users-name')
        password = request.form.get('users-password')

        if len(str(email)) < 4:
            pass
        elif len(str(firstname)) < 2:
            pass
        elif len(str(password)) < 4:
            pass
        else:
            print("Information was valid, proceed!")
            validinformation = True
            new_user = User(email=email, password = generate_password_hash(password, method = 'sha256'), firstname=firstname)
            db.session.add(new_user)
            db.session.commit()
            # return render_template('signup.html', usersemail = email, usersfirstname = firstname, userspassword = password, booleanValue = validinformation)
            return render_template('movies.html')
        
    return render_template('signup.html',boolean = validinformation)

@app.get('/login/signup/signin')
def singinuser ():
    return render_template('signin.html')

@app.route ('/loginuser', methods = ['GET','POST'])
def loginuser ():
    print ("This is the method we're using")
    if request.method == 'POST':
        email = request.form.get('users-email')
        password = request.form.get('users-password')
        
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                return render_template('movies.html', content = "Just decided to change this content to see if it works")
            else:
                print ("the passwords did not match")

    return render_template('login.html')




if __name__ == "__main__":
    app.run(debug=True)

