from os import path
from quart import Quart, send_file
import requests
import shutil

app = Quart(__name__)

# thanks airiuwu for helping me a bit to make this faster <3
# it's my first time using quart.

@app.route("/medals/client/<medal>")
@app.route("/medals/web/<medal>")
@app.route("/images/medals-client/<medal>")
async def medalRequest(medal):
    # if we already have it, pull from the disk.
    if not path.exists(f"medals/osu/{medal}"):
        #We don't have it saved locally, request it from osu! and save it.
        # TODO: look into aiopath
        req = requests.get(f"https://s.ppy.sh/images/medals-client/{medal}", stream=True)
        if req.status_code != 200:
            return "not found"

        with open(f"medals/osu/{medal}", "wb") as file:
            req.raw.decode_content = True
            shutil.copyfileobj(req.raw, file)
            return await send_file(f"medals/osu/{medal}")

    return await send_file(f"medals/osu/{medal}")

app.run()