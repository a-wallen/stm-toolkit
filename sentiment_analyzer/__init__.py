import sys
# Append the path to the /models folder for access to shared models
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

# https://www.nltk.org/howto/sentiment.html
import logging

import azure.functions as func


def main(documents: func.DocumentList) -> str:
    if documents:
        logging.info('Document id: %s', documents[0]['id'])
