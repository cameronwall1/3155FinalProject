from flask import Flask, render_template, url_for, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_required, login_user, logout_user, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
import csv
import re

# Tried adding the flask login, didnt work. If you see errors, start by removing that first and then going from there



db = SQLAlchemy()
DB_NAME = "database.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisismysecretkey!'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)

lineCount = 0
csv_file = open("rotten_tomatoes_movies.csv", 'r')
csv_reader = csv.reader(csv_file, delimiter=',')
lines = []

line = ''
for row in csv_file:
    lines.append(line)
    line = row
    #print("Line " + str(lineCount) + " found!")
    lineCount += 1
lines.pop(0)

csv_file.close()


class Movie (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    movietitle = db.Column (db.String(75))
    moviedescription = db.Column(db.String(250))
    movierating = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, movietitle, moviedescription, movierating, user_id):
        self.movietitle = movietitle
        self.moviedescription = moviedescription
        self.movierating = movierating
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

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_first_request
def create_tables():
    db.create_all()
    # db.drop_all()



# arg@ row: A raw line from the csv file
def getMovieTitleFromRow(row):
    columns = re.split(',', row)
    title = columns[1]
    return title

# arg@ row: A raw line from the csv file
def getMovieDescFromRow(row):
    columns = re.split(',"', row)
    desc = columns[1]
    desc = '"' + desc
    return desc

# arg@ row: A raw line from the csv file
def getTomatoMovieRatingFromRow(row):
    columns = re.split(',', row)
    rating = columns[len(columns) - 1 - 7]
    return rating

# arg@ row: A raw line from the csv file
def getAudienceMovieRatingFromRow(row):
    columns = re.split(',', row)
    rating = columns[len(columns) - 1 - 4]
    return rating

# arg@ lines: An array that contains raw lines from the csv file
# arg@ targetTitle: the relative title that the program should look for
def getMovieDescFromTitle(lines, targetTitle):
    desc = None
    currentTitle = ''

    for row in range(len(lines)):
        row += 1
        currentTitle = getMovieTitleFromRow(lines[row].lower())

        if (currentTitle.find((targetTitle.lower()))):
            desc = getMovieDescFromRow(lines[row])
            break
    
    return desc

# arg@ lines: An array that contains raw lines from the csv file
# arg@ targetTitle: the relative title that the program should look for
def getMovieTitleFromTitle(lines, targetTitle):
    title = None
    currentTitle = ''

    for row in range(len(lines)):
        row += 1
        currentTitle = getMovieTitleFromRow(lines[row].lower())

        if (currentTitle.find((targetTitle.lower()))):
            title = getMovieTitleFromRow(lines[row])
            break
    
    return title

# arg@ lines: An array that contains raw lines from the csv file
# arg@ targetTitle: the relative title that the program should look for
def getMovieTitlesFromTitle(lines, targetTitle):
    titles = None
    currentTitle = ''

    for row in range(len(lines)):
        row += 1
        currentTitle = getMovieTitleFromRow(lines[row].lower())

        if (currentTitle.find((targetTitle.lower()))):
            titles.append(getMovieTitleFromRow(lines[row]))
    
    return titles

# arg@ lines: An array that contains raw lines from the csv file
# arg@ targetTitle: the relative title that the program should look for
def getAudRatingFromTitle(lines, targetTitle):
    rating = None
    currentTitle = ''

    for row in range(len(lines)):
        row += 1
        currentTitle = getMovieTitleFromRow(lines[row].lower())

        if (currentTitle.find((targetTitle.lower()))):
            rating = getAudienceMovieRatingFromRow(lines[row])
            break
    
    return rating

# arg@ lines: An array that contains raw lines from the csv file
# arg@ targetTitle: the relative title that the program should look for
def getTomRatingFromTitle(lines, targetTitle):
    rating = None
    currentTitle = ''

    for row in range(len(lines)):
        row += 1
        currentTitle = getMovieTitleFromRow(lines[row]).lower()

        if (currentTitle.find((targetTitle.lower()))):
            rating = getTomatoMovieRatingFromRow(lines[row])
            break
    
    return rating

@app.route('/', methods = ['GET', 'POST'])
def index ():
    return render_template("login.html", user1 = current_user)

@app.route('/login', methods = ['GET', 'POST'])
def login ():
    print("This is the method that we are using!")
    return render_template('login.html', user1 = current_user, allusers = User.query.all())

@app.route('/movies', methods = ['GET', 'POST'])
@login_required
def movies ():
    return render_template('movies.html', user1 = current_user, values = Movie.query.all(), allusers = User.query.all())

@app.route('/reviewers', methods = ['GET', 'POST'])
@login_required
def revieweres ():
    return render_template('reviewers.html', user1 = current_user)

@app.route('/login/signup/createaccount', methods = ['GET', 'POST'])
def singupuser ():

    validinformation = False

    if request.method == 'POST':
        email = request.form.get("users-email")
        firstname = request.form.get('users-name')
        password = request.form.get('users-password')

        print(Movie)

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
            login_user(new_user, remember = True)
            # return render_template('signup.html', usersemail = email, usersfirstname = firstname, userspassword = password, booleanValue = validinformation)
            return render_template('movies.html', content = 'This is just where we ran this shit from', user1 = current_user, values = Movie.query.all())
        
    return render_template('signup.html',boolean = validinformation, user1 = current_user)

@app.post('/addmovies')
def addMovieRating ():
    if request.method == 'POST':
        movietitle1 = request.form.get("moviename")
        moviedescription1 = request.form.get("description")
        movierating1 = request.form.get("rating")
        usersid = current_user


        if (len(movietitle1) < 2 or len(moviedescription1) < 5):
            pass
        else:
            newmovie = Movie(movietitle = movietitle1, moviedescription = moviedescription1, movierating = movierating1, user_id = usersid.id)
            db.session.add(newmovie)
            db.session.commit()
            return render_template('movies.html' , user1 = current_user, values = Movie.query.all(), allusers = User.query.all())

@app.get('/login/signup/signin')
def singinuser ():
    return render_template('signin.html', user1 = current_user, allusers = User.query.all())

@app.route ('/loginuser', methods = ['GET','POST'])
def loginuser ():
    print ("This is the method we're using")
    if request.method == 'POST':
        email = request.form.get('users-email')
        password = request.form.get('users-password')
        
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember = True)
                return render_template('movies.html', content = "True", user1 = current_user,values = Movie.query.all(), allusers = User.query.all())
            else:
                print ("the passwords did not match")

    return render_template('signin.html', content = "The passwords did not match. Please try again!", user1 = current_user)

@app.route ('/logout', methods = ['GET','POST'])
@login_required
def logout ():
    logout_user()
    # return redirect(url_for('login.html'))
    return render_template('login.html', user1 = current_user)


@app.route('/delete/<int:id>')
def deletemovie (id):
    movie_to_delete = Movie.query.get_or_404(id)
    print("This is the delete method")
    db.session.delete(movie_to_delete)
    db.session.commit()
    if (len(Movie.query.all()) == 0):
        return render_template('movies.html', user1 = current_user)
    
    return render_template('movies.html', user1 = current_user, values = Movie.query.all(), allusers = User.query.all())

@app.route('/movies/search', methods = ['POST','GET'])
def search_movies():
    moviename = request.form.get('searchfunction').lower()
    tempvalues = Movie.query.all() 
    finalmovie = ''
    print (moviename)

    for i in tempvalues:
        if i.movietitle.lower() == moviename.lower():
            finalmovie = i.movietitle.lower()

    if finalmovie == '':
        tomatoTitles = getMovieTitlesFromTitle(lines, moviename)
        if tomatoTitles != None:
            finalmovie.append(tomatoTitles)

    return render_template('movies.html', search_active=True, values = Movie.query.all(), name = moviename, finalmovie = finalmovie, user1 = current_user, allusers = User.query.all())

if __name__ == "__main__":
    app.run(debug=True)

# 1429 Nia Rd. Charlotte,NC 28215
# Users: cam@gmail.com 1234567
# Users: jordan@gmail.com  
# Users: calliewall@gmail.com
