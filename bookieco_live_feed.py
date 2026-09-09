import asyncio
import json
import random
import time
import urllib.request
import websockets

from bookieco_market_reader import BookieCoMarketReader


BOOKIECO_WS_URL = "wss://agents.bookieco.com.cy/ws/"
BOOKIECO_SEARCH_URL = "https://agents.bookieco.com.cy/api/sports/search"


class BookieCoLiveFeed:

    def __init__(self):

        self.reader = BookieCoMarketReader()
        self.connected = False


    # =====================================================
    # BOOKIECO INTERNAL ID
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
    # SEARCH BOOKIECO
    # =====================================================

    def search_match(
        self,
        query
    ):

        payload = {
            "headers": {},
            "requestArguments": {
                "query": str(query)
            }
        }


        body = json.dumps(
            payload
        ).encode(
            "utf-8"
        )


        request = urllib.request.Request(
            BOOKIECO_SEARCH_URL,
            data=body,
            method="POST"
        )


        request.add_header(
            "Content-Type",
            "application/json"
        )

        request.add_header(
            "Accept",
            "application/json"
        )

        request.add_header(
            "Origin",
            "https://agents.bookieco.com.cy"
        )

        request.add_header(
            "Referer",
            "https://agents.bookieco.com.cy/"
        )


        try:

            with urllib.request.urlopen(
                request,
                timeout=15
            ) as response:

                raw_data = (
                    response.read()
                    .decode("utf-8")
                )


            data = json.loads(
                raw_data
            )


            # =============================================
            # REAL BOOKIECO SEARCH RESPONSE STRUCTURE
            #
            # returnValue
            #   -> results
            #       -> matches
            # =============================================

            return_value = data.get(
                "returnValue",
                {}
            )


            if not isinstance(
                return_value,
                dict
            ):

                return_value = {}


            results_object = (
                return_value.get(
                    "results",
                    {}
                )
            )


            if not isinstance(
                results_object,
                dict
            ):

                results_object = {}


            raw_matches = (
                results_object.get(
                    "matches",
                    []
                )
            )


            if not isinstance(
                raw_matches,
                list
            ):

                raw_matches = []


            results = []


            for raw_match in raw_matches:

                if not isinstance(
                    raw_match,
                    dict
                ):

                    continue


                match_id = (
                    raw_match.get(
                        "id"
                    )
                )


                name = (
                    raw_match.get(
                        "name"
                    )
                )


                result = {

                    "match_id":
                        match_id,

                    "name":
                        name,

                    "code":
                        raw_match.get(
                            "code"
                        ),

                    "timestamp":
                        raw_match.get(
                            "ts"
                        ),

                    "status":
                        raw_match.get(
                            "status"
                        ),

                    "league_id":
                        raw_match.get(
                            "leagueId"
                        ),

                    "league_code":
                        raw_match.get(
                            "leagueCode"
                        ),

                    "league_name":
                        raw_match.get(
                            "leagueName"
                        ),

                    "category_name":
                        raw_match.get(
                            "categoryName"
                        ),

                    "sport_id":
                        raw_match.get(
                            "sportId"
                        ),

                    "sport_code":
                        raw_match.get(
                            "sportCode"
                        ),

                    "sport_name":
                        raw_match.get(
                            "sportName"
                        )
                }


                results.append(
                    result
                )


            return {

                "success": True,

                "query":
                    query,

                "matches_found":
                    len(results),

                "results":
                    results
            }


        except Exception as e:

            return {

                "success": False,

                "query":
                    query,

                "matches_found":
                    0,

                "results":
                    [],

                "error":
                    str(e)
            }


    # =====================================================
    # SEARCH FOR FOOTBALL MATCH ONLY
    # =====================================================

    def search_football_match(
        self,
        query
    ):

        result = self.search_match(
            query
        )


        if not result.get(
            "success"
        ):

            return result


        football_matches = []


        for match in result.get(
            "results",
            []
        ):

            if (
                match.get(
                    "sport_code"
                )
                == "soccer"
            ):

                football_matches.append(
                    match
                )


        result[
            "results"
        ] = football_matches


        result[
            "matches_found"
        ] = len(
            football_matches
        )


        return result


    # =====================================================
    # NORMAL LIVE FEED
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

                "error":
                    str(e),

                "summary":
                    self.reader.summary()
            }


        self.connected = False


        return {

            "success": True,

            "matches":
                list(
                    self.reader.matches.values()
                ),

            "summary":
                self.reader.summary()
        }


    # =====================================================
    # REQUEST SPECIFIC MATCH
    # =====================================================

    async def get_specific_match(
        self,
        match_id,
        listen_seconds=10
    ):

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

                "match_id":
                    match_id,

                "error":
                    str(e)
            }


        self.connected = False


        match = (
            self.reader.get_match(
                int(match_id)
            )
        )


        markets = (
            self.reader.get_markets(
                int(match_id)
            )
        )


        market_1x2 = (
            self.reader.get_1x2_market(
                int(match_id)
            )
        )


        return {

            "success": True,

            "match_id":
                int(match_id),

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
                and
                len(
                    self.reader.get_markets(
                        match_id
                    )
                ) > 0
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
    # HELPERS
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


    def get_markets(
        self,
        match_id
    ):

        return (
            self.reader.get_markets(
                match_id
            )
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
