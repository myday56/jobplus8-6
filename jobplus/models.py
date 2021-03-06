from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin,current_user
from werkzeug.security import generate_password_hash,check_password_hash

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    updated_time=db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

class User(Base,UserMixin):
    __tablename__ = 'user'

    ROLE_USER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(32),index=True,nullable=False)
    email = db.Column(db.String(64),unique=True,index=True,nullable=False)
    _password = db.Column('password',db.String(256),nullable=False)
    phone=db.Column(db.String(16))
    realname=db.Column(db.String(64))
    role = db.Column(db.SmallInteger,default=ROLE_USER)
    allow=db.Column(db.SmallInteger,default=1)
    job = db.Column(db.String(64))
    resume_url = db.Column(db.String(64))
    
    def __repr__(self):
        return '<User: {}'.format(self.username)

    @property
    def password(self):
        return self._password
    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)
    
    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY


class Job(Base):
    __tablename__ = 'job'
    id = db.Column(db.Integer,primary_key=True)
    jobname = db.Column(db.String(64),nullable=False)
    salary_min = db.Column(db.String(64))
    salary_max = db.Column(db.String(64))
    exprience = db.Column(db.String(64))
    degree = db.Column(db.String(64))
    location = db.Column(db.String(64))
    job_tag = db.Column(db.String(64))
    job_description = db.Column(db.String(256))
    job_requirement = db.Column(db.String(256))
    company_id = db.Column(db.Integer,db.ForeignKey('company.id',ondelete='CASCADE'))
    company = db.relationship('CompanyDetail',uselist=False,backref=db.backref('job'))
    online=db.Column(db.SmallInteger,default=1)

    @property 
    def current_user_is_applied(self):
        d = Delivery.query.filter_by(job_id=self.id, user_id=current_user.id).first()
        return (d is not None)
    

class CompanyDetail(Base):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    logo = db.Column(db.String(256), nullable=False)
    site = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(24), nullable=False)
    description = db.Column(db.String(100))
    about = db.Column(db.String(1024))
    tags = db.Column(db.String(128))
    stack = db.Column(db.String(128))
    team_introduction = db.Column(db.String(256))
    welfares = db.Column(db.String(256))
    field = db.Column(db.String(128))
    finance_stage = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    user = db.relationship('User', uselist=False, backref=db.backref('company', uselist=False))


    def __repr__(self):
        return '<Company: {}'.format(self.id)

    @property
    def url(self):
        return url_for('company.detail',company_id=self.id)


class Delivery(Base):
    __tablename__ = 'delivery'

    STATUS_WAITING = 1
    STATUS_REJECT = 2
    STATUS_ACCEPT = 3

    id = db.Column(db.Integer,primary_key=True)
    job_id = db.Column(db.Integer,db.ForeignKey('job.id',ondelete='SET NULL'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='SET NULL'))
    company_id = db.Column(db.Integer)
    status = db.Column(db.SmallInteger,default= STATUS_WAITING)
    response = db.Column(db.String(256))

    @property 
    def user(self):
        return User.query.get(self.user_id)

    @property 
    def job(self):
        return Job.query.get(self.job_id)