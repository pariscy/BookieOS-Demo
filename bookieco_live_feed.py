import asyncio
import json
import random
import time
import websockets

from bookieco_market_reader import BookieCoMarketReader


BOOKIECO_WS_URL = "wss://agents.bookieco.com.cy/ws/"


class BookieCoLiveFeed:

    def __init__(self):

        self.reader = BookieCoMarketReader()
        self.connected = False


    # =====================================================
    # CREATE BOOKIECO-STYLE INTERNAL ID
    # Example:
    # 1788957133291-756
    # =====================================================

    def _create_internal_id(self):

        timestamp = int(
            time.time() * 1000
        )

        random_number = random.randint(
            100,
            999
        )

        return (
            str(timestamp)
            + "-"
            + str(random_number)
        )


    # =====================================================
    # NORMAL LIVE CONNECTION
    # =====================================================

    async def connect(
        self,
        listen_seconds=10
    ):

        try:

            async with websockets.connect(
                BOOKIECO_WS_URL,
                origin="https://agents.bookieco.com.cy",
                max_size=None
            ) as websocket:

                self.connected = True

                try:

                    await asyncio.wait_for(
                        self._listen(
                            websocket
                        ),
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
        listen_seconds=10
    ):

        # Start with clean data
        self.reader = (
            BookieCoMarketReader()
        )


        internal_id = (
            self._create_internal_id()
        )


        try:

            async with websockets.connect(
                BOOKIECO_WS_URL,
                origin="https://agents.bookieco.com.cy",
                max_size=None
            ) as websocket:

                self.connected = True


                # =========================================
                # EXACT BOOKIECO SUBSCRIPTION STRUCTURE
                # =========================================

                subscription = {

                    "subscribe": {

                        "internalId":
                            internal_id,

                        "object":
                            "match",

                        "ids":
                            str(match_id),

                        "marketfilter":
                            "all"
                    }
                }


                await websocket.send(
                    json.dumps(
                        subscription,
                        separators=(",", ":")
                    )
                )


                # =========================================
                # RECEIVE DATA
                # =========================================

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


                # =========================================
                # UNSUBSCRIBE CLEANLY
                # =========================================

                unsubscribe = {

                    "unsubscribe": {

                        "internalId":
                            internal_id,

                        "object":
                            "match",

                        "ids":
                            str(match_id),

                        "marketfilter":
                            "all"
                    }
                }


                try:

                    await websocket.send(
                        json.dumps(
                            unsubscribe,
                            separators=(",", ":")
                        )
                    )

                except Exception:

                    pass


        except Exception as e:

            self.connected = False

            return {
                "success": False,
                "match_id": match_id,
                "internal_id": internal_id,
                "error": str(e)
            }


        self.connected = False


        # =============================================
        # GET THE REQUESTED MATCH
        # =============================================

        match = (
            self.reader.get_match(
                int(match_id)
            )
        )


        # =============================================
        # GET ALL MARKETS RECEIVED
        # =============================================

        markets = (
            self.reader.get_markets(
                int(match_id)
            )
        )


        # =============================================
        # GET KNOWN 1X2 MARKET
        # marketTypeId 3
        # =============================================

        market_1x2 = (
            self.reader.get_1x2_market(
                int(match_id)
            )
        )


        return {

            "success": True,

            "match_id":
                int(match_id),

            "internal_id":
                internal_id,

            "match":
                match,

            "markets":
                markets,

            "markets_received":
                len(markets),

            "market_1x2":
                market_1x2
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

        found_match = False
        found_market = False


        while True:

            message = (
                await websocket.recv()
            )


            self.reader.process_message(
                message
            )


            if (
                self.reader.get_match(
                    match_id
                )
                is not None
            ):

                found_match = True


            if len(
                self.reader.get_markets(
                    match_id
                )
            ) > 0:

                found_market = True


            # Once we have both the match and at least one market,
            # keep listening briefly so BookieCo can send
            # the rest of the markets.
            if (
                found_match
                and found_market
            ):

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
    # FIND MATCH BY TEAM NAME
    # =====================================================

    def find_match(
        self,
        team_name
    ):

        return (
            self.reader.find_match(
                team_name
            )
        )


    # =====================================================
    # GET MARKETS
    # =====================================================

    def get_markets(
        self,
        match_id
    ):

        return (
            self.reader.get_markets(
                match_id
            )
        )


    # =====================================================
    # GET MATCH + MARKETS
    # =====================================================

    def get_match_with_markets(
        self,
        match_id
    ):

        return (
            self.reader.get_match_with_markets(
                match_id
            )
        )
