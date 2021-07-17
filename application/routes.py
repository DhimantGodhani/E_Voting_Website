from application import app, db_connection
from flask import render_template, request, session, flash, redirect
from bson.json_util import dumps
import json

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
    partyD = db["election_year_2020"]
    partyD_cursor = partyD.find()
    partyD_cursor_list = list(partyD_cursor)
    partyD_json1 = dumps(partyD_cursor_list)
    partyD_json = json.loads(partyD_json1)
    return render_template("past_results.html", login=True, partyD_json=partyD_json)


@app.route("/voteNow")
def voteNow():
    candidates = db["election_year_2021"]
    candidates_cursor = candidates.find()
    candidates_cursor_list = list(candidates_cursor)
    candidates_json_1 = dumps(candidates_cursor_list)
    candidates_json = json.loads(candidates_json_1)
    return render_template("voteNow.html", login=True, candidates_json=candidates_json, isLoggedIn=True)


@app.route("/futureEvents")
def futureEvents():
    return render_template("futureEvents.html", login=True)


@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if 'email' in session:
        email = session['email']
        users_table = db["users"]
        email_found = users_table.find_one({"username": email})
        if email_found:

            if email_found['voted']:
                flash("You have already voted!")
                return redirect('/voteNow')

            candidates_table = db["election_year_2021"]
            candidate_name = request.args.get('candidate')
            candidate_found = candidates_table.find_one({"name": candidate_name})

            if candidate_found:
                # Update vote count of the candidate
                vote_count = int(candidate_found['vote']) + 1
                candidate_filter = {'name': candidate_name}
                candidate_new_value = {"$set": {'vote': vote_count}}
                candidates_table.update_one(candidate_filter, candidate_new_value)

                # Update voting status of the user
                user_filter = {'username': email}
                user_new_value = {"$set": {'voted': True}}
                users_table.update_one(user_filter, user_new_value)
                flash("Thank you for your vote")
            else:
                flash("Candidate: " + candidate_name + " not found")

            return redirect('/voteNow')
        else:
            msg = 'Unknown user'
    msg = 'You need to login before voting'
    return render_template('login.html', msg=msg)
