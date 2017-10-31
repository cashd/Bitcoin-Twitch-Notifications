import tornado.ioloop
import tornado.web
import settings

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
		(r"/", MainHandler),
		(r"/auth/login/", AuthLoginHandler), 
		(r"/auth/logout", AuthLogoutHandler),
		]

		settings = {
			"template_path": settings.TEMPLATE_PATH,
			"static_path": settings.STATIC_PATH,
			"debug": settings.DEBUG,
			"cookie_secret": settings.COOKIE_SECRET,
			"login_url": "/auth/login/"
		}

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()