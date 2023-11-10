import os

basedir = os.path.abspath(os.path.dirname(__file__))

oauth_config = {
    # Google OAuth 2.0 documentation:
    # https://developers.google.com/identity/protocols/oauth2/web-server#httprest
    'google': {
        'client_id': '550480126987-9ff8tnd74r1hen4bi2tubvqm19956cn3.apps.googleusercontent.com', # Pull keys from your key store. DO NOT hard code like here
        'client_secret': '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',  # Pull keys from your key store. DO NOT hard code like here
        'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
        'token_url': 'https://accounts.google.com/o/oauth2/token',
        'userinfo': {
            'url': 'https://www.googleapis.com/oauth2/v3/userinfo',
            'email': lambda json: json['email'],
        },
        'scopes': ['https://www.googleapis.com/auth/userinfo.email'],
    },

    # GitHub OAuth 2.0 documentation:
    # https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps
    'github': {
        'client_id': "6833f33e3b48d55b3409", # Pull keys from your key store. DO NOT hard code like here
        'client_secret': "014db34f56753443c842c7d07f730e154bf78770", # Pull keys from your key store. DO NOT hard code like here
        'authorize_url': 'https://github.com/login/oauth/authorize',
        'token_url': 'https://github.com/login/oauth/access_token',
        'userinfo': {
            'url': 'https://api.github.com/user/emails',
            'email': lambda json: json[0]['email'],
        },
        'scopes': ['user:email'],
    },
}

class Config(object):
    OAUTH2_PROVIDERS = oauth_config
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SECRET_KEY = "LOL"
    TESTING = False
    MONGO_URI = "mongodb://localhost:27017"
    MONGODB_SETTINGS = {
        "db": "flaskapp"
    }

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

class TestingConfig(Config):
    TESTING = True