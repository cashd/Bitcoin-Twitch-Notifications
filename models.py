from peewee import *

db = SqliteDatabase('database.db')

class User(Model):
	# uid = 
	email = CharField()
	twitch_id = CharField()
	twitch_username = CharField()
	btc_address = CharField()
	twitch_profile_picture = CharField()
	profile_bio = CharField()


	class Meta:
		database = db



class Transaction(Model):
	user = ForeignKeyField(User, related_name="transactions")
	rec_wallet_address = CharField()
	display_name = CharField()
	display_msg = CharField()
	#amount = IntegerField()
	currency_type = CharField()

	class Meta:
		database = db



	