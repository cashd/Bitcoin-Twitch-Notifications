import tornado.ioloop
import tornado.web
import settings

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		if self.get_secure_cookie("user") is not None:
			# Validate OAuth token with Twitch API
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
		except MissingArgumentError:
			# Redirect to login page with error message
			self.redirect("/")

	def post(self):
		# User is redirect from twitch to thi


# Used to host login page so user can get redirect to twich auth page
class LoginHandler(BaseHandler):
	# If user is not authenticated host login page
	# Else redirect to home page as user should be authenticated
	if get_current_user() is None:
		self.write("login")
	else:
		self.redirect("/")




		





def make_app():
	return tornado.web.Application(
    	handlers = [
		(r"/", MainHandler),
		(r"/auth/login/", AuthLoginHandler), 
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