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
    """
    Generate a code verifier and corresponding code challenge for PKCE (Proof Key for Code Exchange).

    This function creates a secure random code verifier and derives a code challenge from it using SHA-256
    hashing and base64 URL-safe encoding, following the PKCE specification for OAuth 2.0.

    Returns
    -------
    tuple of str
        A tuple containing:
        - code_verifier (str): A high-entropy cryptographic random string.
        - code_challenge (str): A base64-encoded SHA-256 hash of the code verifier.

    Examples
    --------
    >>> code_verifier, code_challenge = get_code_challenge()
    >>> print(code_verifier)
    xYz123abc...
    >>> print(code_challenge)
    ABcdEfGhIj...
    """
    cv = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
    cv = re.sub('[^a-zA-Z0-9]+', '', cv)
    cc = hashlib.sha256(cv.encode('utf-8')).digest()
    cc = base64.urlsafe_b64encode(cc).decode('utf-8')
    cc = cc.replace('=', '')
    return cv, cc

code_verifier, code_challenge = get_code_challenge()


def get_auth_url():
    """
    Construct the authorization URL for initiating the OAuth 2.0 Authorization Code Flow with PKCE.

    This function builds a URL to the OAuth 2.0 authorization endpoint with the necessary
    parameters including response type, client ID, scopes, redirect URI, and PKCE code challenge.

    Returns
    -------
    str
        The full URL to which the user should be redirected to begin the authentication process.

    Raises
    ------
    KeyError
        If required configuration keys (e.g., CLIENT_ID, REDIRECT_URI) are missing from app config.

    Examples
    --------
    >>> auth_url = get_auth_url()
    >>> print(auth_url)
    https://sram.surf.nl/oidc/authorize?response_type=code&client_id=...
    """
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


def get_access_token(code, code_verifier):
    """
    Exchange an authorization code for an access token using the OAuth 2.0 Authorization Code Flow with PKCE.

    This function sends a POST request to the SRAM token endpoint, providing the authorization code and
    code verifier to retrieve an access token and related information.

    Parameters
    ----------
    code : str
        The authorization code received from the authorization server after user login.
    code_verifier : str
        The original code verifier used to generate the code challenge in the authorization request.

    Returns
    -------
    dict or None
        A dictionary containing the access token and other relevant OAuth fields (e.g., id_token, refresh_token),
        or None if the request fails.

    Examples
    --------
    >>> token_response = get_access_token("abc123", "verifierXYZ")
    >>> if token_response:
    ...     print(token_response["access_token"])
    """
    token_params = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': app.config['CLIENT_ID'],
        'client_secret': app.config['CLIENT_SECRET'],
        'redirect_uri': app.config['REDIRECT_URI'],
        'code_verifier': code_verifier,
    }
    result = requests.post(app.config['token_endpoint'], data=token_params)
    if result.status_code != 200:
        print(result.content, token_params)
        return None
    return result.json()


# determine if the user is logged in
def is_logged_in():
    """
    Returns if the user is logged in

    :return:
    boolean
    """
    return 'access_token' in session


# get the userinfo from the SRAM server using the access token from the previously retrieved access token
def get_userinfo(access_token):
    """
    Retrieve user information based on the user ID.

    Parameters
    ----------
    user_id : str
        The unique identifier of the user.

    Returns
    -------
    dict
        A dictionary containing user details such as name, email, and roles.


    Examples
    --------
    >>> user = get_user_info("12345")
    >>> print(user["email"])
    johndoe@example.com
    """
    if (is_logged_in() is False):
        return None
    result = requests.post(url=app.config['userinfo_endpoint'], data=access_token)
    if (result.status_code != 200):
        return None
    return result.json()


# get config from .well-known endpoint
def get_config(url):
    """
    Retrieve OAuth 2.0/OIDC configuration from a `.well-known` endpoint.

    This function sends a GET request to the provided discovery URL (typically ending in
    `.well-known/openid-configuration`) and returns the parsed configuration as a dictionary.

    Parameters
    ----------
    url : str
        The full URL to the OpenID Connect discovery document.

    Returns
    -------
    dict
        A dictionary containing configuration details such as authorization and token endpoints,
        or an empty dictionary if the request fails.

    Examples
    --------
    >>> config = get_config("https://sram.surf.nl/.well-known/openid-configuration")
    >>> print(config.get("authorization_endpoint"))
    https://sram.surf.nl/oidc/authorize
    """
    result = requests.get(url)
    if result.status_code == 200:
        return json.loads(result.content)
    return {}
