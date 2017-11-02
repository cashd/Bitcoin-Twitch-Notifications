import tornado.ioloop
import tornado.web
import requests
import settings
import uuid
from random import randint
from models import User



class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        if self.get_secure_cookie('user_uuid') is not None:
            oauth =  self.get_secure_cookie('user_oauth')
            is_token_valid = requests.get("https://api.twitch.tv/helix", headers={'Authorization': 'Bearer {}'.format(oauth) }).json()['token']['valid']
            if is_token_valid:
                return User.get(User.uuid == self.get_secure_cookie('user_uuid'))
            else:
                return None




class MainHandler(BaseHandler):
    def get(self):
        self.write("Hello, world")




class AuthTwitchHandler(BaseHandler):
    def get(self):
        try:
            auth_code = self.get_argument("code")
        except tornado.web.MissingArgumentError:
            # Redirect to login page with error message
            self.redirect("/login/")
        payload = {
        "client_id":settings.TWITCH_CLIENT_ID,
        "client_secret": settings.TWITCH_SECRET,
        "code": auth_code,
        "grant_type": "authorization_code",
        "redirect_uri":settings.TWITCH_REDIRECT_URL
        }
        #Aync later
        r = requests.post("https://api.twitch.tv/kraken/oauth2/token", params=payload)
        # Check to see if request was not 404/403/etc.
        if r.status_code == requests.codes.ok:
            twitch_json = r.json()
            access_token = twitch_json["access_token"]
            refresh_token = twitch_json["refresh_token"]
            twitch_user = requests.get("https://api.twitch.tv/helix/users", headers={"Authorization": "Bearer {}".format(access_token)})
            twitch_user_data = twitch_user.json()['data']
            twitch_id = int(twitch_user_data['id'])
            query = User.select().where(User.twitch_id == twitch_id)
            try:
                user = User.get(User.twitch_id == twitch_id)
            except User.DoesNotExist:
                user = User.create(uuid=uuid.uuid4(), hash_id=randint(1111,9999), email=twitch_user_data['email'], twitch_id=twitch_id, twitch_username= twitch_user_data['display_name'])

            self.set_secure_cookie('user_uuid', user.uuid)
            self.set_secure_cookie('user_oauth', access_token)
            self.set_secure_cookie('user_refresh', refresh_token)

            self.redirect('/')
        else:
            # Redrect to login page with error message
            self.redirect("/")



class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect('/')

# Used to host login page so user can get redirect to twich auth page
class LoginHandler(BaseHandler):
    def get(self):
        if self.get_current_user() is None:
            self.write("login")
        else:
            self.redirect("/")

    def post(self):
        if self.get_current_user() is None:





def make_app():
    return tornado.web.Application(
        handlers = [
        (r'/', MainHandler),
        (r'/login/', LoginHandler),
        (r'/logout', LogoutHandler),
            (r'/twitch/auth/', )
        ], settings = {
            "template_path": settings.TEMPLATE_PATH,
            "static_path": settings.STATIC_PATH,
            "debug": settings.DEBUG,
            "cookie_secret": settings.COOKIE_SECRET,
            "login_url": settings.LOGIN_URL,
            "xsrf_cookies": settings.XSRF_COOKIES,
        }
        )

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()