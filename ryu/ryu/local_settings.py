#ignore the following error when using ipython:
#/django/db/backends/sqlite3/base.py:50: RuntimeWarning:
#SQLite received a naive datetime (2012-11-02 11:20:15.156506) while time zone
#support is active.

import warnings
import exceptions
warnings.filterwarnings("ignore", category=exceptions.RuntimeWarning,
        module='django.db.backends.sqlite3.base', lineno=53)
