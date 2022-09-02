import os, requests
import tornado.web, tornado.gen
import requests
import shutil
import asyncio

def make_app():
    return tornado.web.Application([
        (r"/images/medals-client/osuhow-(.*)", custom_medal_handler),
        (r"/images/medals-client/(.*)", normal_medal_handler),
        (r"/medals/web/(.*)", medals_web_handler),
        (r"/medals/client/(.*)", medals_client_handler)
    ])

class normal_medal_handler(tornado.web.RequestHandler):
    def get(self, medal = None):
        try:
            #Before we get started, let's check some things
            if medal is None or len(medal) == 0:
                raise Exception("No medal requested!")

            #First, we need to check if we already have the medal
            if os.path.isfile(f"medals/osu/{medal}"):
                #We already have it, send the one we already have.
                with open(f"medals/osu/{medal}", "rb") as file:
                    data = file.read()
            else:
                #We don't have it saved locally, request it from osu! and save it.
                req = requests.get(f"https://s.ppy.sh/images/medals-client/{medal}", stream=True)
                if req.status_code == 200:
                    with open(f"medals/osu/{medal}", "wb") as file:
                        req.raw.decode_content = True
                        shutil.copyfileobj(req.raw, file)
                else:
                    raise Exception(f"Medal dosen't exist, osu! said: {req.status_code}")
                #Now that we have it saved, we'll grab it.
                with open(f"medals/osu/{medal}", "rb") as file:
                    data = file.read()
            
            #Send the medal.
            self.write(data)
            self.set_header("Content-type", "image/png")
            self.set_header("Content-length", len(data))
            return

        except Exception as e:
            self.set_status(404)
            print(f"Error: {e}")
            return

class custom_medal_handler(tornado.web.RequestHandler):
    def get(self, medal = None):
        try:
            #Before we get started, let's check some things
            if medal is None or len(medal) == 0:
                raise Exception("No medal requested!")

            #First, we need to check if we have the medal.
            if os.path.isfile(f"medals/osuhow/{medal}"):
                #We already have it, let's grab it.
                with open(f"medals/osu/{medal}", "rb") as file:
                    data = file.read()
            else:
                #We don't have it.
                raise Exception("Custom medal not found.")
            
            #Send the medal.
            self.write(data)
            self.set_header("Content-type", "image/png")
            self.set_header("Content-length", len(data))
            return

        except Exception as e:
            self.set_status(404)
            print(f"Error: {e}")
            return

class medals_web_handler(tornado.web.RequestHandler):
    def get(self, medal = None):
        try:
            #Before we get started, let's check some things
            if medal is None or len(medal) == 0:
                raise Exception("No medal requested!")

            #First, we need to check if we already have the medal
            if os.path.isfile(f"medals/web/{medal}"):
                #We already have it, send the one we already have.
                with open(f"medals/web/{medal}", "rb") as file:
                    data = file.read()
            else:
                #We don't have it saved locally, request it from osu! and save it.
                req = requests.get(f"https://assets.ppy.sh/medals/web/{medal}", stream=True)
                if req.status_code == 200:
                    with open(f"medals/web/{medal}", "wb") as file:
                        req.raw.decode_content = True
                        shutil.copyfileobj(req.raw, file)
                else:
                    raise Exception(f"Medal dosen't exist, osu! said: {req.status_code}")
                #Now that we have it saved, we'll grab it.
                with open(f"medals/web/{medal}", "rb") as file:
                    data = file.read()
            
            #Send the medal.
            self.write(data)
            self.set_header("Content-type", "image/png")
            self.set_header("Content-length", len(data))
            return

        except Exception as e:
            self.set_status(404)
            print(f"Error: {e}")
            return

class medals_client_handler(tornado.web.RequestHandler):
    def get(self, medal = None):
        try:
            #Before we get started, let's check some things
            if medal is None or len(medal) == 0:
                raise Exception("No medal requested!")

            #First, we need to check if we already have the medal
            if os.path.isfile(f"medals/client/{medal}"):
                #We already have it, send the one we already have.
                with open(f"medals/client/{medal}", "rb") as file:
                    data = file.read()
            else:
                #We don't have it saved locally, request it from osu! and save it.
                req = requests.get(f"https://assets.ppy.sh/medals/client/{medal}", stream=True)
                if req.status_code == 200:
                    with open(f"medals/client/{medal}", "wb") as file:
                        req.raw.decode_content = True
                        shutil.copyfileobj(req.raw, file)
                else:
                    raise Exception(f"Medal dosen't exist, osu! said: {req.status_code}")
                #Now that we have it saved, we'll grab it.
                with open(f"medals/client/{medal}", "rb") as file:
                    data = file.read()
            
            #Send the medal.
            self.write(data)
            self.set_header("Content-type", "image/png")
            self.set_header("Content-length", len(data))
            return

        except Exception as e:
            self.set_status(404)
            print(f"Error: {e}")
            return



async def main():
    app = make_app()
    app.listen(5008)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
