
# -*- coding: utf-8 -*-
from pprint import pprint
import traceback
from flask import current_app as app

import repository.database


@app.manager.option('-c',
                    '--command',
                    help='Name of the command')
def database(command):
    try:
        func = getattr(repository.database, command)()
    except Exception as e:
        print('ERROR: ' + str(e))
        traceback.print_tb(e.__traceback__)
        pprint(vars(e))
