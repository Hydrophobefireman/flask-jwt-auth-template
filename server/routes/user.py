from server.api_handlers import user
from server.app_init import app
from server.util import ParsedRequest, api_response


# user registration route
# POST request
@app.post("/accounts/register/", strict_slashes=False)
@app.post("/register", strict_slashes=False)
@api_response
def register():
    return user.register(ParsedRequest())


@app.post("/accounts/login", strict_slashes=False)
@api_response
def login():
    return user.login(ParsedRequest())


# refresh the JWT Token
# GET request
@app.get("/accounts/token/refresh/", strict_slashes=False)
@api_response
def refesh_token():
    return user.re_authenticate(ParsedRequest())


# ===========================================================================
#                                  Users


@app.get("/accounts/<user>/", strict_slashes=False)
@api_response
def view_user(username):
    return user.get_user_details(ParsedRequest(), username)


@app.patch("/accounts/<user>/", strict_slashes=False)
@api_response
def edit_user(username):
    return user.edit(ParsedRequest(), username)
