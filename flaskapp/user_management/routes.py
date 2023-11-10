from urllib.parse import urlencode
import secrets

import requests

from . import bp
from .models import User
from .service import get_user_by_email
from .forms import RegisterForm, LoginForm
from flaskapp.sqlite_database import db

from flask import request, flash, render_template, redirect, url_for, abort, current_app, session
from flask_login import login_user, logout_user, current_user


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = get_user_by_email(form.email.data)
            if user is None:
                flash("Invalid Username")
            else:
                if user.password_hash is None:
                    flash("please user Oauth to login")
                elif user.verify_hash(form.password.data):
                    login_user(user)
                    next = request.args.get("next")
                    return redirect(next or url_for("main.index"))
    return render_template("user/login.html", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User(email=form.email.data)
            user.generate_hash(form.password.data)
            db.session.add(user)
            db.session.commit()
            current_app.logger.info("User Registerd: %s", user.email)
            return redirect(url_for("user_management.login"))
    return render_template("user/register.html", form=form)


@bp.get("/logout")
def logout():
    logout_user()
    current_app.logger.info("User Logged Out")
    return redirect(url_for("user_management.login"))


@bp.get("/oauth_login/<provider>")
def oauth_login(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    # generate a random string for the state parameter
    session['oauth2_state'] = secrets.token_urlsafe(16)

    # create a query string with all the OAuth2 parameters
    qs = urlencode({
        'client_id': provider_data['client_id'],
        'redirect_uri': url_for('user_management.oauth_callback', provider=provider,
                                _external=True),
        'response_type': 'code',
        'scope': ' '.join(provider_data['scopes']),
        'state': session['oauth2_state'],
    })

    # redirect the user to the OAuth2 provider authorization URL
    return redirect(provider_data['authorize_url'] + '?' + qs)

@bp.route("/oauth_callback/<provider>")
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    # if there was an authentication error, flash the error messages and exit
    if 'error' in request.args:
        for k, v in request.args.items():
            if k.startswith('error'):
                flash(f'{k}: {v}')
        return redirect(url_for('index'))

    # make sure that the state parameter matches the one we created in the
    # authorization request
    if request.args['state'] != session.get('oauth2_state'):
        abort(401)

    # make sure that the authorization code is present
    if 'code' not in request.args:
        abort(401)

    # exchange the authorization code for an access token
    response = requests.post(provider_data['token_url'], data={
        'client_id': provider_data['client_id'],
        'client_secret': provider_data['client_secret'],
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('user_management.oauth_callback', provider=provider,
                                _external=True),
    }, headers={'Accept': 'application/json'})

    if response.status_code != 200:
        abort(401)
    oauth2_token = response.json().get('access_token')
    if not oauth2_token:
        abort(401)

    # use the access token to get the user's email address
    response = requests.get(provider_data['userinfo']['url'], headers={
        'Authorization': 'Bearer ' + oauth2_token,
        'Accept': 'application/json',
    })
    if response.status_code != 200:
        abort(401)
    email = provider_data['userinfo']['email'](response.json())

    # find or create the user in the database
    user = get_user_by_email(email)
    if user is None:
        user = User(email=email)
        db.session.add(user)
        db.session.commit()

    # log the user in
    login_user(user)

    current_app.logger.info("User Oauthed In: %s", user.email)
    return redirect(url_for('main.index'))


