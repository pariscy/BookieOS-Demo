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
            "first_message_type": None,
            "first_message_size": 0,
            "first_message_keys": [],
        }


    async def connect(self, listen_seconds=10):
        """
        Connect to the BookieCo WebSocket and listen
        for betting data for a short period.
        """

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
                "matches": [],
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


            # Save useful information about the FIRST message only
            if self.debug_info["messages_received"] == 1:

                try:
                    self.debug_info["first_message_size"] = len(message)
                except Exception:
                    self.debug_info["first_message_size"] = 0


            try:

                data = json.loads(message)

            except Exception:
                continue


            # Record structure of first valid JSON message
            if self.debug_info["first_message_type"] is None:

                self.debug_info["first_message_type"] = type(data).__name__

                if isinstance(data, dict):

                    self.debug_info["first_message_keys"] = list(
                        data.keys()
                    )[:30]

                elif isinstance(data, list):

                    self.debug_info["first_message_keys"] = [
                        f"LIST_LENGTH={len(data)}"
                    ]


            # ---------- NORMAL SINGLE OBJECT ----------
            if isinstance(data, dict):

                self.reader.process_message(data)


                # Sometimes data may be nested inside common container keys
                possible_containers = [
                    "data",
                    "items",
                    "matches",
                    "markets",
                    "result",
                    "results",
                    "payload"
                ]

                for key in possible_containers:

                    nested = data.get(key)

                    if isinstance(nested, list):

                        for item in nested:

                            if isinstance(item, dict):
                                self.reader.process_message(item)


                    elif isinstance(nested, dict):

                        self.reader.process_message(nested)


            # ---------- LIST OF OBJECTS ----------
            elif isinstance(data, list):

                for item in data:

                    if isinstance(item, dict):
                        self.reader.process_message(item)


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
