import sys, os
# Append the path to the /models folder for access to shared models
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models'))


from graph import Graph

import logging
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    symbol = req.params.get('symbol')
    if not symbol:
        return func.HttpResponse(
             "Pass a symbol in the query string or in the request body for a valid response.",
             status_code=400
        )

    if symbol:
        directory: str = os.path.abspath(os.path.dirname(__file__))
        try:
            f = open(os.path.join(directory, f"{symbol}.html"))
        except (IOError, ValueError, EOFError) as e:
            g = Graph()
            figure = g.graph(symbol, directory)
        except:
            print("Unknown Error")
        finally:
            f = open(os.path.join(directory, f"{symbol}.html"))
            data = f.read()
        return func.HttpResponse(
            status_code=200,
            headers={'content-type':'text/html'},
            charset="utf-16",
            body=data
        )
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

# if __name__ == "__main__":
#     symbol: str = "TSLA"
#     directory: str = os.path.abspath(os.path.dirname(__file__))
#     try:
#         f = open(os.path.join(directory, f"{symbol}.html"))
#     except (IOError, ValueError, EOFError) as e:
#         g = Graph()
#         figure = g.graph(symbol, directory)
#     except:
#         print("Unknown Error")
#     finally:
#         f = open(os.path.join(directory, f"{symbol}.html"))
#         data = f.read()
#         print(data)

