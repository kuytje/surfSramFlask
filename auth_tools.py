# helper function
# the code challenge is an encoded string that is used to verify the identity
# of the client the code verifier is a random string that is used to generate
# the code challenge
from flask import current_app as app, session
import requests
import base64
import hashlib
import json
import os
import re

def get_code_challenge():
    cv = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
    cv = re.sub('[^a-zA-Z0-9]+', '', cv)
    cc = hashlib.sha256(cv.encode('utf-8')).digest()
    cc = base64.urlsafe_b64encode(cc).decode('utf-8')
    cc = cc.replace('=', '')
    return cv, cc

code_verifier, code_challenge = get_code_challenge()

# request the initial authorization code from the SRAM server
def get_auth_url():
    return requests.get(
        url=app.config['authorization_endpoint'],
        params={
            "response_type": "code",
            "client_id": app.config['CLIENT_ID'],
            "scope": "openid profile email",
            "redirect_uri": app.config['REDIRECT_URI'],
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        },
        allow_redirects=False
    ).url


# request the access token from the SRAM server using the code from the previous step
def get_access_token(code, code_verifier):
    token_params = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': app.config['CLIENT_ID'],
        'client_secret': app.config['CLIENT_SECRET'],
        'redirect_uri': app.config['REDIRECT_URI'],
        'code_verifier': code_verifier,
    }
    result = requests.post(app.config['token_endpoint'], data=token_params)
    if (result.status_code != 200):
        print(result.content, token_params)
        return None
    return result.json()


# determine if the user is logged in
def is_logged_in():
    return 'access_token' in session


# get the userinfo from the SRAM server using the access token from the previously retrieved access token
def get_userinfo(access_token):
    if (is_logged_in() is False):
        return None
    result = requests.post(url=app.config['userinfo_endpoint'], data=access_token)
    if (result.status_code != 200):
        return None
    return result.json()


# get config from .well-known endpoint
def get_config(url):
    result = requests.get(url)
    if result.status_code == 200:
        return json.loads(result.content)
    return {}
