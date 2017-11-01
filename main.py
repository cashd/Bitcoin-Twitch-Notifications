import tornado.ioloop
import tornado.web
import requests
import settings
from models import User

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		if self.get_secure_cookie("user") is not None:
			#Validate OAuth token with Twitch API
			# Check if user id is the one associated with Twitch
		else:
			# Redirect to Login Page so user 
			#can obtain token by visiting custom auth url




class MainHandler(BaseHandler):
    def get(self):
        self.write("Hello, world")




class AuthTwitchHandler(BaseHandler):

	def get(self):
		try:
			auth_code = self.get_argument("code")
			state = self.get_argument()
		except:
			# Redirect to login page with error message
			self.redirect("/")
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
			expires_in = twitch_json["expires_in"]
			scope = twitch_json["scope"]
			twitch_user = requests.get("https://api.twitch.tv/helix/users", headers={"Authorization": "Bearer {}".format(access_token)})
			twitch_user_data = twitch_user.json()
			twitch_id = int(twitch_user_data["data"]["id"])
			query = User.select().where(User.twitch_id == twitch_id)
			if query.exist():
				user = User.get(User.twitch_id == twitch_id)
				self.set_secure_cookie("user_uid",user.uid)
				self.set_secure_cookie("user_oauth", access_token)
				self.set_secure_cookie("user_refresh", refresh_token)
				self.set_secure_cookie("tok_exp", expires_in)
			else:
				user = User.create(uid=)














		else:
			# Redrect to login page with error message
			self.redirect("/")



class AuthLogoutHandler(BaseHandler):
	def get(self):
		x =5

# Used to host login page so user can get redirect to twich auth page
class LoginHandler(BaseHandler):
	# If user is not authenticated host login page
	# Else redirect to home page as user should be authenticated
	def get(self):
		if self.get_current_user() is None:
			self.write("login")
		else:
			self.redirect("/")




		





def make_app():
	return tornado.web.Application(
    	handlers = [
		(r"/", MainHandler),
		(r"/auth/login/", AuthTwitchHandler),
		(r"/auth/logout", AuthLogoutHandler),
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