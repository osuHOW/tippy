from quart import Quart, send_file
from aiohttp import ClientSession
from aiofiles.os import path
import aiofiles
from ratelimit import limits, RateLimitException

app = Quart(__name__)

# thanks airiuwu for helping me to make this faster <3

@app.route("/medals/client/<medal>")
@app.route("/medals/web/<medal>")
@app.route("/images/medals-client/<medal>")
async def medalRequest(medal):
    Path = f"medals/osu/{medal}"
    # if we already have it, pull from the disk.
    if not await path.exists(Path):
        #We don't have it saved locally, request it from osu!
        try:
            if await requestMedalFromOsu(medal, Path):
                return await send_file(Path)

            return "not found"

        except RateLimitException: 
            return "rate limit"
            
    return await send_file(Path)

# This should be a good limit,
# You might need to increase it if you don't already have all the medals saved.
@limits(calls=20, period=1200)
async def requestMedalFromOsu(medal, Path):
    async with ClientSession() as session:
        async with session.get(f"https://s.ppy.sh/images/medals-client/{medal}") as req:
            if req.status != 200:
                return False

            file = await aiofiles.open(Path, mode="wb")
            await file.write(await req.read())
            await file.close()
            return True

app.run()