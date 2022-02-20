#!/usr/bin/env python3
import os
import base64
import json
import dotenv
from alpaca_news import AlpacaNews
from alpaca_ticker import AlpacaTicker
from prediction import Prediction
from sentiment import Sentiment
from typing import Any, Dict, List, TypeVar
from azure.cosmos import CosmosClient
from delta import Delta

T = TypeVar('T')

class Cosmos():
    """Cosmos DB wrapper"""

    def __init__(self):
        self._internalClient = self._cosmosCreateInstance()
        database_name = 'sentiments'
        self._database = self._internalClient.get_database_client(database_name)
        self.prediction_container_name = "predictions"
        self.article_container_name = "articles"
        self.sentiment_container_name = "sentiments"
        self.ticker_container_name = "tickers"
        self.delta_name = "deltas"
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

    def write(self, items: List[any]) -> None:
        """Write items of the generic type T in the database
        this function will handle contain resolution based on
        the type of T and return the result 

        Args:
            items (List[Generic[T]]): The list of items to be written.

        Unit Tests:
        """
        container = self._getContainer(item_type=type(items[0]))
        client = self._database.get_container_client(container)
        for item in items:
            client.upsert_item(item.__dict__)

    def read(
        self,
        item_type: type,
        filter_injection: str=None,
        skip: int=None,
        limit: int=None,
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
        
        # Get container details to read data from
        container = self._getContainer(item_type)
        container_client = self._database.get_container_client(container)

        whereClause = ""
        if filter_injection:
            whereClause = f"WHERE {filter_injection}"
        
        offset = ""
        if offset:
            offset = f"OFFSET {skip}"

        range = ""
        if limit:
            range = f"LIMIT {limit}"

        results: Any = container_client.query_items(
            f"""
            SELECT * FROM {container}
            {whereClause}
            {offset}
            {range}
            """,
            enable_cross_partition_query=True 
        )

        converted = []
        for result in results:
            result = {res: result[res] for res in result if not res.startswith("_")}
            c = item_type(**result)
            converted.append(c)

        return converted

    def _getContainer(self, item_type: any) -> str:
        """Get container name from passed type

        Args:
            item_type (Generic[T]): type of the item that you want to do

        Raises:
            Exception: Exception if type name does not resolve to a container

        Returns:
            str: container name

        Unit Test:
            >>> c = Cosmos()
            >>> actual = c.getContainer(AlpacaNews)
            >>> expected = c.article_container_name
            >>> actual == expected
            True
            >>> actual = c.getContainer(Prediction)
            >>> expected = c.prediction_container_name
            >>> actual == expected
            True
            >>> actual = c.getContainer(Sentiment)
            >>> expected = c.sentiment_container_name
            >>> actual == expected
            True
        """
        if item_type == AlpacaNews:
            container: str = self.article_container_name
        elif item_type == Prediction:
            container: str = self.prediction_container_name
        elif item_type == Sentiment:
            container: str = self.sentiment_container_name
        elif item_type == AlpacaTicker:
            container: str = self.ticker_container_name
        elif item_type == Delta:
            container: str = self.delta_name
        else:   
            raise Exception(f"Cannot read {item_type} from database")
        return container


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    wrapper = CosmosClient()
