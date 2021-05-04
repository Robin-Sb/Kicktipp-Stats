# flag whether files should be saved to disk in order to avoid making requests every time, you probably won't need this unless you intend to change the code
SAVE_FILES = False
# insert the name of your kicktipp lobby here
LOBBY_NAME = "asbuli2020"

LOCAL_URL = "files/game_day"
BASE_URL = "https://www.kicktipp.de/" + LOBBY_NAME + "/tippuebersicht?&spieltagIndex="
URL = ""

if SAVE_FILES:
    URL = LOCAL_URL
else:
    URL = BASE_URL