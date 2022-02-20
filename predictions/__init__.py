import sys, os
# Append the path to the /models folder for access to shared models
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

import logging
import azure.functions as func
from cosmos import Cosmos
from sentiment import Sentiment
from delta import Delta

def main(documents: func.DocumentList) -> str:

    if documents:
        logging.info('Document id: %s', documents[0]['id'])

    # Access database
    instance = Cosmos()

    # Read sentiment data
    sentiments = instance.read(Sentiment) # filter_injection

    # TODO: Create predictions
