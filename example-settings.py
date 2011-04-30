import os
from path import path

FILE_ROOT = path(os.environ['VIRTUAL_ENV']) / path('var/emporium')

if not FILE_ROOT.exists():
    FILE_ROOT.mkdir()
