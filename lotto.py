# omg pythonz!
import requests
import re
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///test.db')
db = SQLAlchemy(app)

class LottoPicks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(150))
    ball_1 = db.Column(db.Integer)
    ball_2 = db.Column(db.Integer)
    ball_3 = db.Column(db.Integer)
    ball_4 = db.Column(db.Integer)
    ball_5 = db.Column(db.Integer)
    mega_ball = db.Column(db.Integer)


def define_tables():
    db.create_all()

def get_megamillion_numbers():
    r = requests.get('http://www.megamillions.com/winning-numbers')
    data = r.text

    # get date of lotto
    regex = re.compile("article class=\"[^\"]*winning-numbers\">.*h1>*(.*)</h1", re.IGNORECASE | re.MULTILINE | re.DOTALL)
    r = regex.search(data)
    if len(r.groups()) != 1:
        print 'Boo!'
        return
    # (u'Winning Numbers 12/13/2013',)
    megamillion_date = r.groups()[0][16:]
    print 'Date of drawing %s' % megamillion_date

    # get whiteballs
    regex = re.compile("<div class=\"winning-numbers-white-ball\">\s*(\S*)\s*</div>", re.IGNORECASE | re.MULTILINE | re.DOTALL)
    r = regex.findall(data)
    if len(r) != 5:
        print 'Boo2!'
        return

    megamillion_balls = [int(ball) for ball in r]
    print 'Balls %s' % megamillion_balls

    # get megaball
    regex = re.compile("<div class=\"winning-numbers-mega-ball\">\s*(\S*)\s*</div>", re.IGNORECASE | re.MULTILINE | re.DOTALL)
    r = regex.findall(data)
    if len(r) != 1:
        print 'Boo3!'
        return

    megamillion_megaball = int(r[0])
    print 'Mega-Balls %s' % megamillion_megaball

