activate_this = "/var/www/flask/pyclock/PythonTimeClock_Flask_API/env_pyclock_api/bin/activate_this.py"
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
sys.path.insert(0, "/var/www/flask/pyclock/PythonTimeClock_Flask_API/")

from api import connex_app

application = connex_app
