import json


class BookieCoMarketReader:

    def __init__(self):
        self.matches = {}
        self.markets = {}


    def process_message(self, raw_message):
        """
        Reads a BookieCo WebSocket message and stores
        useful match and market information.
        """

        try:

            if isinstance(raw_message, str):
                data = json.loads(raw_message)
            else:
                data = raw_message

        except Exception:
            return None


        if not isinstance(data, dict):
            return None


        object_type = data.get("object")


        # ---------- MATCH ----------
        if object_type == "match":

            match_id = data.get("id")

            if match_id is None:
                return None

            competitors = data.get("competitors", [])

            match = {
                "match_id": match_id,
                "uuid": data.get("uuid"),
                "tournament_id": data.get("tournamentId"),
                "competitors": competitors,
                "start_time": data.get("startTs"),
                "number_of_markets": data.get("nrMarkets"),
            }

            self.matches[match_id] = match

            return {
                "type": "match",
                "data": match
            }


        # ---------- MARKET ----------
        if object_type == "market":

            market_id = data.get("id")
            match_id = data.get("matchId")

            if market_id is None or match_id is None:
                return None

            selections = []

            for selection in data.get("selections", []):

                selections.append({
                    "selection_id": selection.get("id"),
                    "outcome": selection.get("outcome"),
                    "odds": selection.get("odds"),
                    "probability": selection.get("probability"),
                })


            market = {
                "market_id": market_id,
                "match_id": match_id,
                "market_type_id": data.get("marketTypeId"),
                "special": data.get("special"),
                "is_suspended": data.get("isSuspended"),
                "selections": selections,
            }


            if match_id not in self.markets:
                self.markets[match_id] = []


            # Replace an existing version of the same market
            # instead of storing duplicates.

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


            return {
                "type": "market",
                "data": market
            }


        return None


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

        team_name = team_name.lower()

        results = []

        for match in self.matches.values():

            competitors = match.get("competitors", [])

            for competitor in competitors:

                if team_name in str(competitor).lower():

                    results.append(match)

                    break

        return results


    def summary(self):

        return {
            "matches_loaded": len(self.matches),
            "markets_loaded": sum(
                len(markets)
                for markets in self.markets.values()
            )
        }
