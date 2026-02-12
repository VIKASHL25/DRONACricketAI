import os
import requests


API_KEY=os.getenv("CRICKET_API_KEY")
API_HOST=os.getenv("CRICKET_API_HOST")
LIVE_URL=os.getenv("CRICKET_API_URL")
DETAIL_URL=os.getenv("CRICKET_DETAIL_URL")

if not API_KEY or not API_HOST or not LIVE_URL or not DETAIL_URL:
    raise Exception("Missing API environment variables. Check your .env file.")

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}

def get_live_matches():

    try:
        response=requests.get(LIVE_URL, headers=headers, timeout=10)
        response.raise_for_status()
        data=response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Live API Error: {str(e)}")

    matches = []

    type_matches=data.get("typeMatches", [])

    for match_type in type_matches:
        series_list=match_type.get("seriesMatches", [])

        for series in series_list:
            wrapper=series.get("seriesAdWrapper", {})
            match_list=wrapper.get("matches", [])

            for match in match_list:
                info=match.get("matchInfo", {})

                match_id=info.get("matchId")
                team1=info.get("team1", {}).get("teamName", "Team 1")
                team2=info.get("team2", {}).get("teamName", "Team 2")
                status=info.get("status", "Status Unavailable")

                if match_id:
                    matches.append({
                        "match_id": match_id,
                        "name": f"{team1} vs {team2}",
                        "status": status
                    })

    return matches

def get_match_details(match_id):

    try:
        url=f"{DETAIL_URL}/{match_id}"
        response=requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        raise Exception(f"Match Detail API Error: {str(e)}")


