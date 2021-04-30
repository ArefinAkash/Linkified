from dotenv import dotenv_values
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from flask import Flask, render_template, redirect, url_for, request
from os import environ
from sys import argv
from tinydb import TinyDB, Query
from urllib.parse import urlparse
from hashids import Hashids
from datetime import datetime
db = TinyDB("db.json")


env_config = dotenv_values(".env")

app = Flask(__name__)

app.secret_key = b"random bytes representing flask secret key"
app.config["TEMPLATES_AUTO_RELOAD"] = True
try:
    app.config["DISCORD_CLIENT_ID"] = environ["PYDISAUR_CLIENT_ID"]
    app.config["DISCORD_CLIENT_SECRET"] = environ["PYDISAUR_CLIENT_SECRET"]
    root = environ["PYDISAUR_ROOT_URL"]
except:
    app.config["DISCORD_CLIENT_ID"] = env_config["CLIENT_ID"]
    app.config["DISCORD_CLIENT_SECRET"] = env_config["CLIENT_SECRET"]
    root = env_config["ROOT_URL"]
app.config["DISCORD_REDIRECT_URI"] = root + "/callback"
discord = DiscordOAuth2Session(app)


def genid():
    hashids = Hashids(salt = "lorem ipsum dolor sit amet", alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
    return hashids.encode(int(datetime.today().timestamp()))
  

@app.route("/static/<path:path>/")
def static_dir(path):
    return send_from_directory("static", path)


@app.route('/')
def home():
    return render_template("home.html")

@app.route("/login/")
def login():
    return discord.create_session()


@app.route("/callback/")
def callback():
    discord.callback()
    return redirect(url_for("dashboard"))


@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))

@app.route("/logout/")
def logout():
    discord.revoke()
    return redirect(url_for("home"), code=302)


@app.route("/dashboard/")
@requires_authorization
def dashboard():
    return render_template("dashboard.html", user=discord.fetch_user())

def is_http_or_https(url):
    return urlparse(url).scheme in {'http', 'https'}

@app.route("/api/shorten/", methods=['POST'])
@requires_authorization
def api_shorten():
    r = request.form
    user = discord.fetch_user()
    d = {}
    d["id"] = genid()
    d["shortened_url"] = root + "/" + d["id"]
    urlf = r["url"]
    if not is_http_or_https(urlf):
        urlf = "http://" + urlf
    d["original_url"] = urlf
    d["creator_id"] = user.id
    db.insert(d)
    return redirect(root + "/dashboard/success?url=" + d["shortened_url"], code=302)


@app.route("/dashboard/success/")
def shorten_success():
    return render_template("shorten_success.html")


@app.route("/dashboard/urls/")
@requires_authorization
def urls():
    r = Query()
    user = discord.fetch_user()
    return render_template("urls.html", l=db.search(r.creator_id == user.id))


@app.route("/api/deleteShorten/")
@app.errorhandler(401)
@requires_authorization
def api_deleteShorten():
    user = discord.fetch_user()
    r = Query()
    if user.id != db.get(r.id == request.args["id"])["creator_id"]:
        return 401
    else:
        p = db.get(r.id == request.args["id"])
        id = p.doc_id
        db.remove(doc_ids=[id])
        return redirect(root + "/dashboard/urls", code=302)


@app.route('/<id>/')
def shorten_manager(id):
    r = Query()
    return redirect(db.get(r.id == id)["original_url"], code=302)


if __name__ == "__main__":
    try:
        p = int(argv[1])
    except:
        p = 5000
    try:
        environ["OAUTHLIB_INSECURE_TRANSPORT"] = argv[2]
    except:
        environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
    app.run(port=p)
