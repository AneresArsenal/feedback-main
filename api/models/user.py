import bcrypt
from sqlalchemy import Column, LargeBinary, String
from sqlalchemy_api_handler import ApiHandler

from models.mixins import HasExternalThumbUrlMixin, \
                          HasQualificationMixin, \
                          HasScienceFeedbackMixin, \
                          HasThumbMixin, \
                          NeedsValidationMixin
from models.role import Role
from utils.db import db


class User(ApiHandler,
           db.Model,
           HasExternalThumbUrlMixin,
           HasQualificationMixin,
           HasScienceFeedbackMixin,
           HasThumbMixin,
           NeedsValidationMixin):

    clearTextPassword = None

    email = Column(String(120), nullable=False, unique=True)

    firstName = Column(String(30))

    lastName = Column(String(30))

    password = Column(LargeBinary(60), nullable=False)

    def check_password(self, passwordToCheck):
        return bcrypt.hashpw(passwordToCheck.encode('utf-8'), self.password) == self.password

    def errors(self):
        errors = super(User, self).errors()
        if self.clearTextPassword:
            errors.check_min_length('password', self.clearTextPassword, 8)
            self.clearTextPassword = None
        if self.email:
            errors.check_email('email', self.email)
        if self.id is None\
           and User.query.filter_by(email=self.email).count() > 0:
            errors.add_error('email', 'Un compte lié à cet email existe déjà')
        return errors

    def get_id(self):
        return str(self.id)

    def has_rights(self, roleType):
        return Role.query\
                   .filter((Role.userId == self.id) &
                           (Role.type == roleType))\
                   .first() is not None

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def modify(self, dct):
        user_dict = dict({}, **dct)

        password = None
        if dct.__contains__('password') and dct['password']:
            password = dct['password']
            del user_dict['password']

        super(User, self).modify(user_dict)

        if password:
            self.set_password(password)

        return self

    def set_password(self, newpass):
        self.clearTextPassword = newpass
        self.password = bcrypt.hashpw(newpass.encode('utf-8'),
                                      bcrypt.gensalt())
