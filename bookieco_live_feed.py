import asyncio
import json
import websockets

from bookieco_market_reader import BookieCoMarketReader


BOOKIECO_WS_URL = "wss://agents.bookieco.com.cy/ws/"


class BookieCoLiveFeed:

    def __init__(self):
        self.reader = BookieCoMarketReader()
        self.connected = False

        self.debug_info = {
            "messages_received": 0,
            "message_types": {},
            "subscription_keys": [],
            "subscription_value_type": None,
            "subscription_sample_keys": [],
            "objects_found": 0,
            "object_types_found": {}
        }


    async def connect(self, listen_seconds=10):

        try:

            async with websockets.connect(
                BOOKIECO_WS_URL,
                origin="https://agents.bookieco.com.cy",
                max_size=None
            ) as websocket:

                self.connected = True

                try:

                    await asyncio.wait_for(
                        self._listen(websocket),
                        timeout=listen_seconds
                    )

                except asyncio.TimeoutError:
                    pass


        except Exception as e:

            self.connected = False

            return {
                "success": False,
                "error": str(e),
                "summary": self.reader.summary(),
                "debug": self.debug_info
            }


        self.connected = False

        return {
            "success": True,
            "matches": list(
                self.reader.matches.values()
            ),
            "summary": self.reader.summary(),
            "debug": self.debug_info
        }


    async def _listen(self, websocket):

        while True:

            message = await websocket.recv()

            self.debug_info["messages_received"] += 1


            try:
                data = json.loads(message)

            except Exception:
                continue


            data_type = type(data).__name__

            self.debug_info["message_types"][data_type] = (
                self.debug_info["message_types"].get(
                    data_type,
                    0
                ) + 1
            )


            # Inspect subscription wrapper
            if isinstance(data, dict) and "subscription" in data:

                subscription = data.get("subscription")

                self.debug_info["subscription_value_type"] = (
                    type(subscription).__name__
                )


                if isinstance(subscription, dict):

                    if not self.debug_info["subscription_keys"]:

                        self.debug_info["subscription_keys"] = list(
                            subscription.keys()
                        )[:30]


                elif isinstance(subscription, list):

                    if not self.debug_info["subscription_keys"]:

                        self.debug_info["subscription_keys"] = [
                            "LIST_LENGTH=" + str(len(subscription))
                        ]


                    if subscription:

                        first_item = subscription[0]

                        if isinstance(first_item, dict):

                            if not self.debug_info[
                                "subscription_sample_keys"
                            ]:

                                self.debug_info[
                                    "subscription_sample_keys"
                                ] = list(
                                    first_item.keys()
                                )[:30]


            # Recursively search this message for
            # BookieCo match and market objects.
            self._scan_for_objects(data)


    def _scan_for_objects(self, value):

        # ---------- DICTIONARY ----------
        if isinstance(value, dict):

            object_type = value.get("object")


            if object_type:

                object_type_string = str(object_type)

                self.debug_info[
                    "object_types_found"
                ][object_type_string] = (
                    self.debug_info[
                        "object_types_found"
                    ].get(
                        object_type_string,
                        0
                    ) + 1
                )


            # If this looks like a BookieCo match or market,
            # send it to our market reader.
            if object_type in ["match", "market"]:

                result = self.reader.process_message(
                    value
                )

                if result is not None:

                    self.debug_info[
                        "objects_found"
                    ] += 1


            # Search everything nested inside this dictionary.
            for nested_value in value.values():

                self._scan_for_objects(
                    nested_value
                )


        # ---------- LIST ----------
        elif isinstance(value, list):

            for item in value:

                self._scan_for_objects(
                    item
                )


    def find_match(self, team_name):

        return self.reader.find_match(
            team_name
        )


    def get_markets(self, match_id):

        return self.reader.get_markets(
            match_id
        )


    def get_match_with_markets(
        self,
        match_id
    ):

        return self.reader.get_match_with_markets(
            match_id
        )
