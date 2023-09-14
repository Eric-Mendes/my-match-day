from typing import List, Any
import datetime
from bidict import bidict
import pandas as pd
import numpy as np
import requests


WEEKDAYS = bidict({
    "Segunda-feira": 0, "Terça-feira": 1, "Quarta-feira": 2, "Quinta-feira": 3, "Sexta-feira": 4, "Sábado": 5, "Domingo": 6
})

FINAL_ROUND = 38

def _get_matches(round: int, team: str, stadiums: List[str], weekdays: List[str], time: datetime.time) -> List[Any]:
    with requests.get(f"https://api.cartola.globo.com/partidas/{round}") as response:
        response_body = response.json()

        all_teams = response_body["clubes"]
        unfiltered_matches = response_body["partidas"]

        team_name_by_id = lambda id: all_teams[str(id)]["nome"]
        utc_to_brazilian_time = lambda timestamp: datetime.datetime.fromtimestamp(timestamp) - datetime.timedelta(hours=0)

        filtered_matches = [
            [match["local"], f"{team_name_by_id(match['clube_casa_id'])} X {team_name_by_id(match['clube_visitante_id'])}", f"{utc_to_brazilian_time(match['timestamp'])}, {WEEKDAYS.inverse[utc_to_brazilian_time(match['timestamp']).weekday()]}"] for match in unfiltered_matches
            if match["local"] in stadiums
            and team in [team_name_by_id(match["clube_visitante_id"]), team_name_by_id(match["clube_casa_id"])]
            and utc_to_brazilian_time(match["timestamp"]).weekday() in [WEEKDAYS[day] for day in weekdays]
            and utc_to_brazilian_time(match["timestamp"]).time() <= time
        ]

        return filtered_matches

def make_schedule(team: str, stadiums: List[str], weekdays: List[str], time: datetime.time) -> pd.DataFrame:
    with requests.get("https://api.cartola.globo.com/partidas") as response:
        CURRENT_ROUND = response.json()["rodada"]

    matches = list()
    for round in range(CURRENT_ROUND, FINAL_ROUND + 1):
        matches.append(_get_matches(round=round, team=team, stadiums=stadiums, weekdays=weekdays, time=time))
    
    matches = np.squeeze(list(filter(lambda match: len(match) > 0, matches)))
    
    if matches.ndim == 1:
        matches = matches[np.newaxis, ...]
    
    matches_df = pd.DataFrame(data=matches, columns=["Estádio", "Jogo", "Data"])

    return matches_df