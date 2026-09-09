import asyncio
import json
import uuid
import websockets

from bookieco_market_reader import BookieCoMarketReader


BOOKIECO_WS_URL = "wss://agents.bookieco.com.cy/ws/"


class BookieCoLiveFeed:

    def __init__(self):

        self.reader = BookieCoMarketReader()
        self.connected = False


    # =====================================================
    # NORMAL LIVE CONNECTION
    # =====================================================

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
                "summary": self.reader.summary()
            }


        self.connected = False

        return {
            "success": True,
            "matches": list(
                self.reader.matches.values()
            ),
            "summary": self.reader.summary()
        }


    # =====================================================
    # REQUEST ONE SPECIFIC MATCH
    # =====================================================

    async def get_specific_match(
        self,
        match_id,
        listen_seconds=8
    ):

        # Start fresh
        self.reader = BookieCoMarketReader()

        try:

            async with websockets.connect(
                BOOKIECO_WS_URL,
                origin="https://agents.bookieco.com.cy",
                max_size=None
            ) as websocket:

                self.connected = True


                # -----------------------------------------
                # BOOKIECO MATCH SUBSCRIPTION
                # -----------------------------------------

                subscription = {

                    "subscribe": {

                        "internalId": str(
                            uuid.uuid4()
                        ),

                        "object": "match",

                        "ids": str(
                            match_id
                        ),

                        "marketfilter": "all"
                    }
                }


                await websocket.send(
                    json.dumps(
                        subscription
                    )
                )


                # -----------------------------------------
                # LISTEN FOR THE MATCH + MARKETS
                # -----------------------------------------

                try:

                    await asyncio.wait_for(
                        self._listen_for_match(
                            websocket,
                            int(match_id)
                        ),
                        timeout=listen_seconds
                    )

                except asyncio.TimeoutError:
                    pass


        except Exception as e:

            self.connected = False

            return {
                "success": False,
                "match_id": match_id,
                "error": str(e)
            }


        self.connected = False


        match = self.reader.get_match(
            int(match_id)
        )


        markets = self.reader.get_markets(
            int(match_id)
        )


        # -----------------------------------------
        # FIND KNOWN 1X2 MARKET
        # -----------------------------------------

        market_1x2 = (
            self.reader.get_1x2_market(
                int(match_id)
            )
        )


        return {

            "success": True,

            "match_id": int(
                match_id
            ),

            "match": match,

            "markets": markets,

            "markets_received": len(
                markets
            ),

            "market_1x2": market_1x2
        }


    # =====================================================
    # GENERAL LISTENER
    # =====================================================

    async def _listen(
        self,
        websocket
    ):

        while True:

            message = (
                await websocket.recv()
            )

            self.reader.process_message(
                message
            )


    # =====================================================
    # SPECIFIC MATCH LISTENER
    # =====================================================

    async def _listen_for_match(
        self,
        websocket,
        match_id
    ):

        while True:

            message = (
                await websocket.recv()
            )


            self.reader.process_message(
                message
            )


            # If we have the requested match AND markets,
            # keep collecting for a short moment.
            if (
                self.reader.get_match(
                    match_id
                )
                is not None
                and
                len(
                    self.reader.get_markets(
                        match_id
                    )
                ) > 0
            ):

                # Give BookieCo another 2 seconds
                # to send additional markets.
                try:

                    while True:

                        extra_message = (
                            await asyncio.wait_for(
                                websocket.recv(),
                                timeout=2
                            )
                        )

                        self.reader.process_message(
                            extra_message
                        )

                except asyncio.TimeoutError:

                    return


    # =====================================================
    # HELPERS
    # =====================================================

    def find_match(
        self,
        team_name
    ):

        return self.reader.find_match(
            team_name
        )


    def get_markets(
        self,
        match_id
    ):

        return self.reader.get_markets(
            match_id
        )


    def get_match_with_markets(
        self,
        match_id
    ):

        return (
            self.reader.get_match_with_markets(
                match_id
            )
        )
