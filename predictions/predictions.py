import sys, os

# Append the path to the /models folder for access to shared models
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models'))

from prediction import Prediction # prediction reports
from cosmos import Cosmos # database client wrapper

class Predictions():

    def __init__(self):
        pass

    def __del__(self):
        pass