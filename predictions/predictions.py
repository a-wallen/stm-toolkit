import sys, os

# Append the path to the /models folder for access to shared models
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

from prediction import prediction # prediction reports
from cosmos import Cosmos # database client wrapper

class Predictions():
    pass