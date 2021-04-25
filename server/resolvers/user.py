from server.resolvers.base_resolver import BaseResolver
from server.api_handlers import user
from server.util import ParsedRequest


class UserResolver(BaseResolver):
    def get(self, username):
        return user.get_user_details(ParsedRequest(), username)

    def patch(self, username):
        return user.edit(ParsedRequest(), username)


class LoginResolver(BaseResolver):
    def post(self):
        return user.login(ParsedRequest())


class RegisterResolver(BaseResolver):
    def post(self):
        return user.register(ParsedRequest())


class AuthenticationResolver(BaseResolver):
    def get(self):
        return user.re_authenticate(ParsedRequest())
