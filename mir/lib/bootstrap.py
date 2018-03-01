#!/usr/bin/env python
"""
Application bootsrap functions
"""

import bcrypt


# -----------------------------------
# Application Bootstrap
# -----------------------------------

def create_admin(app, token_generator):
    with app.app_context():
        sub_resource = app.data.driver.db['accounts']
        admin = sub_resource.find_one({'username': app.config['DEFAULT_ADMIN_USER']})
        if not admin:
            default_admin_account = {
                'username': app.config['DEFAULT_ADMIN_USER'],
                'password': bcrypt.hashpw(app.config['DEFAULT_ADMIN_PW'].encode('utf-8'), bcrypt.gensalt()),
                'roles': 'superuser',
                'owner': app.config['DEFAULT_ADMIN_USER'],
                'token': token_generator(app.config['SECRET_KEY'], app.config['DEFAULT_ADMIN_USER'])
            }
            app.data.insert('accounts', default_admin_account)
