"""
#app/run.py
Provides entry point for app
"""
import os
from .api import create_app
from .api.manage import tables 

APP = create_app(config=os.getenv("CONFIG"))


tables("create")


if __name__ == ('__main__'):
	APP.run()



