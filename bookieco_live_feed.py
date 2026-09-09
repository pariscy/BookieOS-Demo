import asyncio
import json
import websockets

from bookieco_market_reader import BookieCoMarketReader


BOOKIECO_WS_URL = "wss://agents.bookieco.com.cy/ws/"


class BookieCoLiveFeed:

    def __init__(self):
        self.reader = BookieCoMarketReader()
        self.connected = False


    async def connect(self, listen_seconds=10):
        """
        Connect to the BookieCo WebSocket and listen
        for betting data for a short period.
        """

        try:
            async with websockets.connect(
                BOOKIECO_WS_URL,
                origin="https://agents.bookieco.com.cy"
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
                "summary": self.reader.summary()
            }

        self.connected = False

        return {
            "success": True,
            "matches": list(self.reader.matches.values()),
            "summary": self.reader.summary()
        }


    async def _listen(self, websocket):

        while True:

            message = await websocket.recv()

            try:
                data = json.loads(message)
            except Exception:
                continue

            self.reader.process_message(data)


    def find_match(self, team_name):

        return self.reader.find_match(team_name)


    def get_markets(self, match_id):

        return self.reader.get_markets(match_id)


    def get_match_with_markets(self, match_id):

        return self.reader.get_match_with_markets(match_id)
