from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail
from models import Feedback, db
from flask_migrate import Migrate
from flask_script import Manager

db = SQLAlchemy()
migrate = Migrate()

def create_app():

    app = Flask(__name__)

    ENV = 'production'

    if ENV == 'development':
        POSTGRES = {
            'user': 'postgres',
            'pw': 'a2dejlnor9054',
            'db': 'mvpdb',
            'host': 'localhost',
            'port': '5432',
        }
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
        %(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    else :
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yssnhbufmhvkze:8fef3ac8f13467f5123dfa014bcafabc29d5d4113df3c775135277865fb850d8@ec2-34-194-14-176.compute-1.amazonaws.com:5432/d24dr5l6kfgcbh'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)
    return app

app = create_app()


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
