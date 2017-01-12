from flask import Flask
from flask_sqlalchemy import SQLAlchemy
##TODO: token based api for andriod andriod application!
app = Flask(__name__)
## change for your db!
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost/Birjandutbot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
db = SQLAlchemy(app)


class users(db.Model):
	__tablename__ = "users"
	username = db.Column('username',db.String(10))
	md5 = db.Column('md5',db.String(32))
	chat_id = db.Column('chat_id',db.String(8), primary_key=True)
	def __init__(self, username, md5,chat_id):
		self.username = username
		self.md5 = md5
		self.chat_id = chat_id

if __name__ == "__main__":
    app.run()