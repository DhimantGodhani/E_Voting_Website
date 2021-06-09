from application import app
from flask import render_template


@app.route("/")
def home():
    return render_template("index.html", home=True)


@app.route("/register")
def register():
    return render_template("register.html", register=True)


@app.route("/login")
def login():
    return render_template("login.html", login=True)

@app.route("/past_results")
def past_results():
    partyData = [{"year":"2017", "partyID":"1111", "partyName":"SOLC", "partyVotes":"400", "result":"Winner"},
{"year":"2018", "partyID":"2222", "partyName":"LGS", "partyVotes":"450", "result":"Winner"},
{"year":"2019", "partyID":"3333", "partyName":"SOPU", "partyVotes":"500", "result":"Winner"},
{"year":"2020", "partyID":"4444", "partyName":"SYFI", "partyVotes":"380", "result":"Winner"}]
    return render_template("past_results.html", login=True, partyData = partyData)

@app.route("/voteNow")
def voteNow():
    return render_template("voteNow.html", login=True)

@app.route("/futureEvents")
def futureEvents():
    return render_template("futureEvents.html", login=True)
