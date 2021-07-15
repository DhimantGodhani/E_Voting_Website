from application import app, db_connection
from flask import render_template, request, session

connection_db = db_connection.db_connection()
db = connection_db.connect_to_mongodb()


@app.route("/")
def home():
    if "email" in session:
        return render_template("index.html", home=True, isLoggedIn=True)
    return render_template("index.html", home=True)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'name' in request.form and 'username' in request.form and 'password' in request.form and 'age' in request.form and 'gender' in request.form:
        username = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get("name")
        age = int(request.form.get("age"))
        gender = request.form.get("gender")
        usersTable = db["users"]
        new_user = {"name": name, "username": username, "password": password, "age": age, "gender": gender,
                    "voted": False}
        try:
            usersTable.insert_one(new_user)
        except Exception as e:
            print("An exception occurred ::", e)
        return render_template("login.html", msg="User successfully created!!!", register=True)
    else:
        if request.method != 'GET':
            return render_template("register.html", msg="Please enter user details carefully!!!", register=True)
    return render_template("register.html", register=True)


@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html", home=True)


@app.route("/login", methods=['GET', 'POST'])
def login():
    msg = 'Please login to your account'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form.get("username")
        password = request.form.get("password")
        usersTable = db["users"]
        username_found = usersTable.find_one({"username": username})
        if username_found:
            username_val = username_found['username']
            password_val = username_found['password']
            if password == password_val:
                session["email"] = username_val
                return render_template("index.html", home=True, isLoggedIn=True)
            else:
                if "email" in session:
                    return render_template("index.html", home=True, isLoggedIn=True)
                msg = 'Wrong password'
                return render_template('login.html', msg=msg)
        else:
            msg = 'Username not found'
            return render_template('login.html', msg=msg)

    return render_template("login.html", login=True)


@app.route("/past_results")
def past_results():
    partyData = [{"year": "2017", "partyID": "1111", "partyName": "SOLC", "partyVotes": "400", "result": "Winner"},
                 {"year": "2018", "partyID": "2222", "partyName": "LGS", "partyVotes": "450", "result": "Winner"},
                 {"year": "2019", "partyID": "3333", "partyName": "SOPU", "partyVotes": "500", "result": "Winner"},
                 {"year": "2020", "partyID": "4444", "partyName": "SYFI", "partyVotes": "380", "result": "Winner"}]
    return render_template("past_results.html", login=True, partyData=partyData)


@app.route("/voteNow")
def voteNow():
    return render_template("voteNow.html", login=True)


@app.route("/futureEvents")
def futureEvents():
    return render_template("futureEvents.html", login=True)
