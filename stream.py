from tda.auth import easy_client
from tda.client import Client
from tda.streaming import StreamClient

import asyncio
import json
import config

client = easy_client(
        api_key=config.API_KEY,
        redirect_uri=config.REDIRECT_URI,
        token_path=config.TOKEN_PATH)
stream_client = StreamClient(client, account_id=config.ACCOUNT_ID)

def order_book_handler(msg):
    print(json.dumps(msg, indent=4))

async def read_stream():
    await stream_client.login()
    await stream_client.quality_of_service(StreamClient.QOSLevel.DELAYED)
    await stream_client.nasdaq_book_subs(['GOOG'])

    stream_client.add_nasdaq_book_handler(order_book_handler)

    while True:
        await stream_client.handle_message()

asyncio.get_event_loop().run_until_complete(read_stream())