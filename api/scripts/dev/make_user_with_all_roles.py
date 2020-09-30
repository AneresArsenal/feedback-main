from sqlalchemy_api_handler import ApiHandler

from models.role import Role, RoleType
from models.user import User


email = os.environ['USER_EMAIL']


user = User.create_or_modify({
    '__SEARCH_BY__': 'email',
    'email': os.environ['USER_EMAIL']
})

roles = []
for role_type in RoleType:
    roles.append(Role.create_or_modify({
        'type': role_type,
        'user': user
    }))

ApiHandler.save(*roles)
