from domdit import db, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

db.metadata.clear()


class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rank = db.Column(db.Integer, autoincrement=True)
    name = db.Column(db.String(200), unique=False, nullable=False)
    languages = db.Column(db.String(200), unique=False, nullable=False)
    short_description = db.Column(db.String(200), unique=False, nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(200), unique=False, nullable=False)
    git = db.Column(db.String(200), unique=False, nullable=False)
    folder = db.Column(db.String(200), unique=True, nullable=False)


class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rank = db.Column(db.Integer, autoincrement=True)
    portfolio_id = db.Column(db.Integer)
    name = db.Column(db.String(200), unique=False, nullable=False)
    site_name = db.Column(db.String(200), unique=False, nullable=False)
    url = db.Column(db.String(200), unique=False, nullable=False)
    text = db.Column(db.Text)
    folder = db.Column(db.String(200), unique=True, nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return "User('{self.email}')"
