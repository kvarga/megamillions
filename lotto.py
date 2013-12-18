# omg pythonz!
from __future__ import print_function
import requests
import re
import os
import csv
from datetime import datetime
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///test.db')
db = SQLAlchemy(app)

class LottoPicks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(150))
    date = db.Column(db.Date)
    ball_1 = db.Column(db.Integer)
    ball_2 = db.Column(db.Integer)
    ball_3 = db.Column(db.Integer)
    ball_4 = db.Column(db.Integer)
    ball_5 = db.Column(db.Integer)
    mega_ball = db.Column(db.Integer)


def import_from_csv(user_id, filename):
    csv_file = csv.DictReader(open(filename, 'rb'), delimiter=',', quotechar='"')
    for line in csv_file:
        new_pick = LottoPicks()
        new_pick.user_id = user_id
        new_pick.ball_1 = line['num1']
        new_pick.ball_2 = line['num2']
        new_pick.ball_3 = line['num3']
        new_pick.ball_4 = line['num4']
        new_pick.ball_5 = line['num5']
        new_pick.mega_ball = line['megaball']
        new_pick.date = datetime.strptime(line['Date'], '%m/%d/%y').date()
        db.session.add(new_pick)
        db.session.commit()
        # {'num4': '43', 'num5': '61', 'num1': '2', 'num2': '17',
        #  'num3': '29', 'Date': '12/17/13', 'megaball': '15'}


def define_tables():
    db.create_all()

def get_megamillion_numbers():
    r = requests.get('http://www.megamillions.com/winning-numbers')
    data = r.text

    # get date of lotto
    regex = re.compile("article class=\"[^\"]*winning-numbers\">.*h1>*(.*)</h1", re.IGNORECASE | re.MULTILINE | re.DOTALL)
    r = regex.search(data)
    if len(r.groups()) != 1:
        print('Boo!')
        return
    # (u'Winning Numbers 12/13/2013',)
    megamillion_date = r.groups()[0][16:]
    megamillion_date = datetime.strptime(megamillion_date, '%m/%d/%Y').date()

    # get whiteballs
    regex = re.compile("<div class=\"winning-numbers-white-ball\">\s*(\S*)\s*</div>", re.IGNORECASE | re.MULTILINE | re.DOTALL)
    r = regex.findall(data)
    if len(r) != 5:
        print('Boo2!')
        return

    megamillion_balls = [int(ball) for ball in r]

    # get megaball
    regex = re.compile("<div class=\"winning-numbers-mega-ball\">\s*(\S*)\s*</div>", re.IGNORECASE | re.MULTILINE | re.DOTALL)
    r = regex.findall(data)
    if len(r) != 1:
        print('Boo3!')
        return

    megamillion_megaball = int(r[0])

    # get prizes (bowwow)
    prizes = {}
    regex = re.compile("<tr class=\"winning-numbers-prize-row[^\"]*\">\s*<td>\s*([^<]*)\s*</td>\s*<td>\s*([^<]*)\s*</td>\s*<td>\s*([^<]*)", re.IGNORECASE | re.MULTILINE | re.DOTALL)
    r = regex.findall(data)
    for money_line in r:
        matches = money_line[0].split('+')
        white_balls = int(matches[0].strip(' '))
        mega_balls = int(matches[1].strip(' '))
        amount = money_line[2]
        prizes[(white_balls, mega_balls)] = amount

    #(u'5 + 0', u'9', u'$1,000,000')
    return (megamillion_date, megamillion_balls, megamillion_megaball, prizes)

def find_winners():
    results = get_megamillion_numbers()
    win_date = results[0]
    win_balls = set(results[1])
    win_megaball = results[2]
    win_prizes = results[3]
    print('%s Megamillion Results: %s MEGA(%s)' % (win_date, ' '.join([str(ball) for ball in win_balls]), win_megaball))

    #lotto_picks = LottoPicks.query.filter_by(date=results[0]).all()
    lotto_picks = LottoPicks.query.filter_by().all()
    for pick in lotto_picks:
        megaball_match = False
        pick_balls = set([pick.ball_1, pick.ball_2, pick.ball_3, pick.ball_4, pick.ball_5])
        combined = pick_balls & win_balls

        if pick.mega_ball == win_megaball:
            megaball_match = True

        prize_won = None
        prize_query = (len(combined), 1 if megaball_match else 0)
        if prize_query in win_prizes:
            prize_won = win_prizes[prize_query]
        if len(combined) >= 3 or megaball_match:
            print('MEGABALL!' if megaball_match else None, '%s white balls' % len(combined), '-', prize_won)

