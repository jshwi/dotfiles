"""
pyfunctions.env
===============
"""
import datetime
import pathlib

HOME = str(pathlib.Path.home())
DATE = datetime.date.today().strftime("%Y/%m/%d")
TIME = datetime.datetime.now().strftime("%H:%M:%S")
