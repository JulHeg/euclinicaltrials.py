__version__ = "1.0.0"

# This package only works for Python 3.8 and above
import sys
if sys.version_info < (3, 8):
    raise ImportError("euclinicaltrials.py requires Python 3.8 or above")

#from .lib import *
from .Trial import *
from .Document import *
