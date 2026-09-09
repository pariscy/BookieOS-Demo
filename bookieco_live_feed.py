import asyncio
import http.cookiejar
import json
import random
import time
import urllib.request
import websockets

from bookieco_market_reader import BookieCoMarketReader


BOOKIECO_BASE_URL = "https://agents.bookieco.com.cy"
BOOKIECO_SESSION_URL = BOOKIECO_BASE_URL + "/api/site/session"
BOOKIECO_SEARCH_URL = BOOKIECO_BASE_URL + "/api/sports/search"
BOOKIECO_WS_URL = "wss://agents.bookieco.com.cy/ws/"


class BookieCoLiveFeed:

    def __init__(self):

        self.reader = BookieCoMarketReader()
        self.connected = False

        self.cookie_jar = (
            http.cookiejar.CookieJar()
        )

        self.http_opener = (
            urllib.request.build_opener(
                urllib.request.HTTPCookieProcessor(
                    self.cookie_jar
                )
            )
        )


    # =====================================================
    # CREATE BOOKIECO INTERNAL ID
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
    # COMMON HTTP HEADERS
    # =====================================================

    def _add_common_headers(
        self,
        request
    ):

        request.add_header(
            "Accept",
            "application/json, text/plain, */*"
        )

        request.add_header(
            "Content-Type",
            "application/json"
        )

        request.add_header(
            "Origin",
            BOOKIECO_BASE_URL
        )

        request.add_header(
            "Referer",
            BOOKIECO_BASE_URL + "/"
        )

        request.add_header(
            "User-Agent",
            "Mozilla/5.0"
        )


    # =====================================================
    # CREATE PUBLIC BOOKIECO SESSION
    # =====================================================

    def create_session(self):

        payload = {

            "headers": {},

            "requestArguments": {}
        }


        body = json.dumps(
            payload
        ).encode(
            "utf-8"
        )


        request = urllib.request.Request(
            BOOKIECO_SESSION_URL,
            data=body,
            method="POST"
        )


        self._add_common_headers(
            request
        )


        try:

            with self.http_opener.open(
                request,
                timeout=15
            ) as response:

                raw_data = (
                    response.read()
                    .decode(
                        "utf-8"
                    )
                )


            data = json.loads(
                raw_data
            )


            return {

                "success": True,

                "data": data,

                "cookies": [
                    cookie.name
                    for cookie
                    in self.cookie_jar
                ]
            }


        except Exception as e:

            return {

                "success": False,

                "error":
                    str(e)
            }


    # =====================================================
    # SEARCH BOOKIECO MATCHES
    # =====================================================

    def search_match(
        self,
        query
    ):

        # ---------------------------------------------
        # STEP 1:
        # Create BookieCo public session
        # ---------------------------------------------

        session_result = (
            self.create_session()
        )


        if not session_result.get(
            "success"
        ):

            return {

                "success": False,

                "stage":
                    "session",

                "error":
                    session_result.get(
                        "error",
                        "Session creation failed"
                    ),

                "results":
                    []
            }


        # ---------------------------------------------
        # STEP 2:
        # Search using SAME cookie-aware opener
        # ---------------------------------------------

        payload = {

            "headers": {},

            "requestArguments": {

                "query":
                    str(query)
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


        self._add_common_headers(
            request
        )


        try:

            with self.http_opener.open(
                request,
                timeout=15
            ) as response:

                raw_data = (
                    response.read()
                    .decode(
                        "utf-8"
                    )
                )


            data = json.loads(
                raw_data
            )


            # =========================================
            # REAL BOOKIECO SEARCH STRUCTURE
            #
            # returnValue
            #   -> results
            #       -> matches
            # =========================================

            return_value = (
                data.get(
                    "returnValue",
                    {}
                )
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


                result = {

                    "match_id":
                        raw_match.get(
                            "id"
                        ),

                    "name":
                        raw_match.get(
                            "name"
                        ),

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

                    "score":
                        raw_match.get(
                            "score"
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

                    "category_id":
                        raw_match.get(
                            "categoryId"
                        ),

                    "category_code":
                        raw_match.get(
                            "categoryCode"
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

                "stage":
                    "search",

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
    # SEARCH FOOTBALL ONLY
    # =====================================================

    def search_football_match(
        self,
        query
    ):

        result = (
            self.search_match(
                query
            )
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


        result["results"] = (
            football_matches
        )


        result["matches_found"] = (
            len(
                football_matches
            )
        )


        return result


    # =====================================================
    # BUILD COOKIE HEADER FOR WEBSOCKET
    # =====================================================

    def _get_cookie_header(self):

        parts = []


        for cookie in self.cookie_jar:

            parts.append(
                cookie.name
                + "="
                + cookie.value
            )


        return "; ".join(
            parts
        )


    # =====================================================
    # GENERAL LIVE CONNECTION
    # =====================================================

    async def connect(
        self,
        listen_seconds=10
    ):

        # Create public BookieCo session first
        session_result = (
            self.create_session()
        )


        if not session_result.get(
            "success"
        ):

            return {

                "success": False,

                "stage":
                    "session",

                "error":
                    session_result.get(
                        "error"
                    ),

                "summary":
                    self.reader.summary()
            }


        cookie_header = (
            self._get_cookie_header()
        )


        headers = {}


        if cookie_header:

            headers["Cookie"] = (
                cookie_header
            )


        try:

            async with websockets.connect(
                BOOKIECO_WS_URL,
                origin=BOOKIECO_BASE_URL,
                additional_headers=headers,
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

                "stage":
                    "websocket",

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
    # REQUEST SPECIFIC MATCH + MARKETS
    # =====================================================

    async def get_specific_match(
        self,
        match_id,
        listen_seconds=10
    ):

        self.reader = (
            BookieCoMarketReader()
        )


        # ---------------------------------------------
        # STEP 1:
        # Create BookieCo public session
        # ---------------------------------------------

        session_result = (
            self.create_session()
        )


        if not session_result.get(
            "success"
        ):

            return {

                "success": False,

                "stage":
                    "session",

                "match_id":
                    match_id,

                "error":
                    session_result.get(
                        "error"
                    )
            }


        # ---------------------------------------------
        # STEP 2:
        # Use same cookies in WebSocket
        # ---------------------------------------------

        cookie_header = (
            self._get_cookie_header()
        )


        headers = {}


        if cookie_header:

            headers["Cookie"] = (
                cookie_header
            )


        internal_id = (
            self._create_internal_id()
        )


        try:

            async with websockets.connect(
                BOOKIECO_WS_URL,
                origin=BOOKIECO_BASE_URL,
                additional_headers=headers,
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

                "stage":
                    "websocket",

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
