#!/usr/bin/env python3
import sys
import os
import base64
import json
import dotenv
import jsonpickle
from prediction import Prediction
from sentiment import Sentiment
from typing import Dict, List, TypeVar, Generic
from azure.cosmos import CosmosClient

T = TypeVar('T')

class Cosmos():
    def __init__(self):
        self._internalClient = self._cosmosCreateInstance()
        database_name = 'sentiments'
        self._database = self._internalClient.get_database_client(database_name)
        self.report_container_name = "reports"
        self.article_container_name = "articles"
        self.sentiment_container_name = "sentiments"
        # container_name = 'Items'
        # self._container = self._database.get_container_client(container_name)

    def _cosmosCreateInstance(self) -> CosmosClient:
        """[PRIVATE] Return new instance of cosmosDB - reading api credentials from environment

        Returns:
            CosmosClient: An instance of CosmosDB Api Client
        """
        dotenv.load_dotenv()
        encrypted_creds: str = os.environ["COSMOS_CREDS"]
        decoded: bytes = base64.b64decode(encrypted_creds)
        json_dict = json.loads(decoded)
        return CosmosClient(
            json_dict["url"],
            json_dict["primary_key"],
        )

    def write(
        self,
        items: List[T],
    ) -> None:
        """Write items of the generic type T in the database
        this function will handle contain resolution based on
        the type of T and return the result 

        Args:
            items (List[Generic[T]]): The list of items to be written.

        Unit Tests:
        """
        pass

    def read(
        self,
        injection: str,
        item_type: Generic[T],
        skip: int,
        limit: int,
    ) -> List[T]:
        """Read items of Generic type [T] from the database

        Args:
            injection (str): injected SQL query
            type (Generic[T]): type of item to read

            Pagination
            skip (int): start at "skip" entries from the beginning
            limit (int): return "limit" number of results from the database 

        Returns:
            List[Generic[T]]: A list of desired items
        
        Unit Tests:
        """
        print(item_type)
        pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()