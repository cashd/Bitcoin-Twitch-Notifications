from peewee import *

db = SqliteDatabase('database.db')

class User(Model):
	uid = 
	email = CharField()
	twitch_id = CharField()
	btc_address = CharField()

	class Meta:
		database = db



class Transaction(Model):
	user = ForeignKeyField(User, related_name="transactions")
	