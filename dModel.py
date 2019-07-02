from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ifvbkjtshpsxqj:4972b22ed367ed7346b0107d3c3e97db14fac1dde628cd6d7f08cf502c927ee1@ec2-50-16-197-244.compute-1.amazonaws.com:5432/d6tkud0mtknjov'
	
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class UserData(db.Model):
    __tablename__ = 'UserData'
	
    Id = db.Column(db.Integer, primary_key=True)
    KeyWord = db.Column(db.String(255))
    Description = db.Column(db.String(255))

    def __init__(self, KeyWord, Description):
        self.KeyWord = KeyWord
        self.Description = Description

    def __repr__(self):
        return "<UserData('%s', '%s')>" % (self.KeyWord, self.Description)


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)