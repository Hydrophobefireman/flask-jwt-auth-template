from server.resolvers.user import (
    AuthenticationResolver,
    LoginResolver,
    RegisterResolver,
    UserResolver,
)

from server.app_init import app
from server.util import POST_REQUEST, api_response, crud


user_resolver = UserResolver()
register_resolver = RegisterResolver()
login_resolver = LoginResolver()
authentication_resolver = AuthenticationResolver()
# user registration route
# POST request
@app.route("/accounts/register/", **crud("post"))
@app.route("/register", **crud("post"))
@api_response
def register():
    return register_resolver.resolve_for()


@app.route("/accounts/login", **POST_REQUEST)
@api_response
def login():
    return login_resolver.resolve_for()


# refresh the JWT Token
# GET request
@app.route("/accounts/token/refresh/", strict_slashes=False)
@api_response
def refesh_token():
    return authentication_resolver.resolve_for()


# ===========================================================================
#                                  Users


@app.route("/accounts/<user>/", **crud("patch", "get"))
@api_response
def edit_user(user):
    return user_resolver.resolve_for(user)
