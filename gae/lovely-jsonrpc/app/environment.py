import sys
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# include all zips in the package directory
LIB_DIR = os.path.join(PROJECT_DIR, 'packages')
if os.path.exists(LIB_DIR):
    _paths = []
    for name in os.listdir(LIB_DIR):
        p = os.path.join(LIB_DIR, name)
        _paths.append(p)
    sys.path = _paths + sys.path
