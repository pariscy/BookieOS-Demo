import json


class BookieCoMarketReader:

    def __init__(self):
        self.matches = {}
        self.markets = {}


    def process_message(self, raw_message):
        """
        Reads BookieCo WebSocket data.

        It supports:
        - a single object
        - {"messages": [...]}
        - lists of objects
        - nested match / market objects
        """

        try:
            if isinstance(raw_message, str):
                data = json.loads(raw_message)
            else:
                data = raw_message

        except Exception:
            return None


        self._scan(data)

        return True


    def _scan(self, value):

        if isinstance(value, dict):

            object_type = value.get("object")


            # ---------- MATCH ----------
            if object_type == "match":

                match_id = value.get("id")

                if match_id is not None:

                    match = {
                        "match_id": match_id,
                        "uuid": value.get("uuid"),
                        "tournament_id": value.get("tournamentId"),
                        "competitors": value.get("competitors", []),
                        "start_time": value.get("startTs"),
                        "number_of_markets": value.get("nrMarkets"),
                        "market_types": value.get("marketTypes", []),
                        "is_live": value.get("isLive"),
                        "is_suspended": value.get("isSuspended"),
                    }

                    self.matches[match_id] = match


            # ---------- MARKET ----------
            elif object_type == "market":

                market_id = value.get("id")
                match_id = value.get("matchId")

                if market_id is not None and match_id is not None:

                    selections = []

                    for selection in value.get("selections", []):

                        selections.append({
                            "selection_id": selection.get("id"),
                            "outcome": selection.get("outcome"),
                            "odds": selection.get("odds"),
                            "probability": selection.get("probability"),
                        })


                    market = {
                        "market_id": market_id,
                        "match_id": match_id,
                        "market_type_id": value.get("marketTypeId"),
                        "special": value.get("special"),
                        "is_suspended": value.get("isSuspended"),
                        "max_payout": value.get("maxPayout"),
                        "selections": selections,
                    }


                    if match_id not in self.markets:
                        self.markets[match_id] = []


                    replaced = False

                    for index, existing_market in enumerate(
                        self.markets[match_id]
                    ):

                        if existing_market["market_id"] == market_id:

                            self.markets[match_id][index] = market
                            replaced = True
                            break


                    if not replaced:
                        self.markets[match_id].append(market)


            # Search all nested values too
            for nested_value in value.values():
                self._scan(nested_value)


        elif isinstance(value, list):

            for item in value:
                self._scan(item)


    def get_match(self, match_id):

        return self.matches.get(match_id)


    def get_markets(self, match_id):

        return self.markets.get(match_id, [])


    def get_match_with_markets(self, match_id):

        match = self.get_match(match_id)

        if match is None:
            return None

        return {
            "match": match,
            "markets": self.get_markets(match_id)
        }


    def find_match(self, team_name):

        team_name = team_name.lower().strip()

        results = []

        for match in self.matches.values():

            competitors = match.get("competitors", [])

            for competitor in competitors:

                if team_name in str(competitor).lower():

                    results.append(match)
                    break

        return results


    def find_exact_match(self, team_a, team_b):

        team_a = team_a.lower().strip()
        team_b = team_b.lower().strip()

        results = []

        for match in self.matches.values():

            competitors = [
                str(x).lower()
                for x in match.get("competitors", [])
            ]

            if len(competitors) < 2:
                continue


            first = competitors[0]
            second = competitors[1]


            normal_order = (
                team_a in first
                and team_b in second
            )

            reverse_order = (
                team_b in first
                and team_a in second
            )


            if normal_order or reverse_order:
                results.append(match)


        return results


    def get_1x2_market(self, match_id):

        """
        From the BookieCo data we have already seen,
        marketTypeId 3 is the standard 1X2 market.
        """

        for market in self.get_markets(match_id):

            if market.get("market_type_id") == 3:
                return market

        return None


    def summary(self):

        return {
            "matches_loaded": len(self.matches),
            "markets_loaded": sum(
                len(markets)
                for markets in self.markets.values()
            )
        }
