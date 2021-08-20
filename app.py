from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail
from models import Feedback, db

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    POSTGRES = {
        'user': 'postgres',
        'pw': 'a2dejlnor9054',
        'db': 'mvpdb',
        'host': 'localhost',
        'port': '5432',
    }
    app.config['DEBUG'] = True
else :
    POSTGRES = {
        'user': 'yssnhbufmhvkze',
        'pw': '8fef3ac8f13467f5123dfa014bcafabc29d5d4113df3c775135277865fb850d8',
        'db': 'd24dr5l6kfgcbh',
        'host': 'ec2-34-194-14-176.compute-1.amazonaws.com',
        'port': '5432',
    }
    app.config['DEBUG'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        service = request.form['service']
        rating = request.form['rating']
        comments = request.form['comments']
        # print(customer, dealer, rating, comments)
        if customer == '' or service == '' or rating == '' or comments == '':
            return render_template('index.html', message='Please fill in all fields')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, service, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, service, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message='You are alreasy registered')



if __name__ == '__main__':
    app.run()
