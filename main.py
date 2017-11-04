import tornado.ioloop
import tornado.web
import requests
from settings import *
from uuid import uuid4
from random import randint
from models import User



class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_cookie = self.get_secure_cookie('user_uuid')
        self.write(str(user_cookie))
        if user_cookie:
            oauth =  self.get_secure_cookie('user_oauth').decode('ascii')
            self.write(str(oauth))
            is_token_valid = requests.get("https://api.twitch.tv/kraken/", headers={'Authorization': 'OAuth {}'.format(oauth)}, params={"client_id": TWITCH_CLIENT_ID})
            self.write(is_token_valid.text)
        #     if is_token_valid:
        #         return self.get_secure_cookie('user_uuid')
        #     else:
        #         return None



class MainHandler(BaseHandler):
    def get(self):
        self.get_current_user()




class AuthTwitchHandler(BaseHandler):
    def get(self):
        try:
            auth_code = self.get_argument("code")
        except tornado.web.MissingArgumentError:
            # Redirect to login page with error message
            self.redirect("/")
        payload = {
        "client_id":TWITCH_CLIENT_ID,
        "client_secret": TWITCH_SECRET,
        "code": auth_code,
        "grant_type": "authorization_code",
        "redirect_uri":TWITCH_REDIRECT_URL
        }
        #Aync later
        r = requests.post("https://api.twitch.tv/kraken/oauth2/token", params=payload)
        if r.status_code == requests.codes.ok:
            twitch_json = r.json()
            access_token = twitch_json["access_token"]
            refresh_token = twitch_json["refresh_token"]
            twitch_user = requests.get("https://api.twitch.tv/helix/users", headers={"Authorization": "Bearer {}".format(access_token)})
            twitch_user_data = twitch_user.json()['data'][0]
            twitch_id = twitch_user_data['id']
            try:
                user = User.get(User.twitch_id == twitch_id)
            except User.DoesNotExist:
                user = User.create(uuid=uuid4(), hash_id=randint(1111,9999), email=twitch_user_data['email'], twitch_id=twitch_id, twitch_username= twitch_user_data['display_name'])
            self.set_secure_cookie('user_uuid', user.uuid)
            self.set_secure_cookie('user_oauth', access_token)
            self.set_secure_cookie('user_refresh', refresh_token)
            self.write("Successfully made User")
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



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/login/', LoginHandler),
            (r'/logout', LogoutHandler),
            (r'/twitch/auth/', AuthTwitchHandler)
        ]
        settings = {
            "template_path":TEMPLATE_PATH,
            "static_path":STATIC_PATH,
            "debug":DEBUG,
            "cookie_secret": '0TiDeqFE7CP4RettuEtmt1iOiSkeXB3V',
            "login_url": "/auth/login/"
        }
        tornado.web.Application.__init__(self, handlers, **settings)
if __name__ == "__main__":
    app = Application()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()