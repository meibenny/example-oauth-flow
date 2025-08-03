from flask import Flask, render_template
from flask_oidc import OpenIDConnect

app = Flask(__name__)
app.config["OIDC_CLIENT_SECRETS"] = "./client_secrets.json"
app.config["SECRET_KEY"] = "abcde12345"
oidc = OpenIDConnect(app)


@app.route("/")
def index():
    logged_in = oidc.user_loggedin
    return render_template("index.html", logged_in=logged_in)

@app.route("/protected")
@oidc.require_login
def protected():
    logged_in = oidc.user_loggedin
    return render_template("index.html", logged_in=logged_in)

@app.route("/token")
@oidc.accept_token()
def token():
    return "token route"
