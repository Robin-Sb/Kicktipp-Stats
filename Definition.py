from enum import Enum
# flag whether files should be saved to disk in order to avoid making requests every time, you probably won't need this unless you intend to change the code
SAVE_FILES = False
# insert the name of your kicktipp lobby here
LOBBY_NAME = "asbuli2020"

LOCAL_URL = "files/game_day"
BASE_URL = "https://www.kicktipp.de/" + LOBBY_NAME + "/tippuebersicht?&spieltagIndex="
URL = ""
TOTAL_MATCHES = 35

if SAVE_FILES:
    URL = LOCAL_URL
else:
    URL = BASE_URL

class Dicts(Enum):
    TEAM_RESULTS = 1,
    ALL_RESULTS_AGGLOMERATED = 2,
    POINTS_PER_TEAM = 3,
    CLOSE_CALLS = 4,
    MISSED_GAMES = 5,
    POINTS_PER_PREDICTED_RESULT = 6,
    AMOUNT_OF_PREDICTIONS = 7,
    AMOUNT_OF_PREDICTIONS_AGGLOMERATED = 8,
    POINTS_PER_PREDICTED_RESULT_AGGLOMERATED = 9