from flask import Blueprint, session, redirect, request, render_template
from auth_tools import is_logged_in, get_userinfo, get_access_token, get_auth_url, code_verifier

# Blueprint Configuration
# Here the static folder and the templates folder are annotated
app_blueprint = Blueprint(
    "app", __name__, template_folder="templates", static_folder="static"
)

# the home route displays the user information if the user is logged in
# else it shows that the user is not logged in
@app_blueprint.route('/')
def home():
    """
    Render the public homepage.

    Displays a public-facing page showing whether the user is currently logged in or not.

    Returns
    -------
    Response
        Rendered HTML template of the public home page.
    """
    logged_in =  is_logged_in()

    return render_template('public.html', logged_in=logged_in)


# the private page is only displayed if the user is logged in
# else it shows that the user is not logged in
@app_blueprint.route('/private')
def private():
    """
    Render the private page for authenticated users.

    If the user is logged in, displays user-specific information retrieved from the SRAM server.
    If the user is not logged in, redirects to the public home page.

    Returns
    -------
    Response
        Rendered HTML template (private or public page).
    """
    if not is_logged_in():
        return render_template('public.html')

    access_token = session['access_token']
    userinfo = get_userinfo(access_token)
    return render_template('private.html', userinfo=userinfo)


@app_blueprint.route('/login')
def login():
    """
    Redirect the user to the SRAM authorization endpoint to initiate login.

    Returns
    -------
    Response
        A redirect response to the SRAM login page.
    """
    return redirect(get_auth_url())


# the authorization callback route is called by the SRAM server after the user
# has logged in
@app_blueprint.route('/authorized/')
def oidc_callback():
    """
    Handle the OIDC authorization callback from the SRAM server.

    Extracts the authorization code from the request, exchanges it for an access token,
    stores the token in the session, and redirects the user to the home page.

    Returns
    -------
    Response
        Redirects to the home page on success or displays an error message on failure.
    """
    code = request.args.get('code')
    access_token = get_access_token(code, code_verifier)
    if access_token is None:
        return "Error while getting access token"
    session['access_token'] = access_token
    return redirect('/')


# the logout route clears the session and redirects the user to the home page
@app_blueprint.route('/logout')
def logout():
    """
    Log the user out by clearing the session and redirecting to the home page.

    Returns
    -------
    Response
        Redirect response to the home page.
    """
    session.pop('access_token', None)
    return redirect('/')
