import requests
async def run(sub):
    req = requests.get(f"http://{sub}.fandom.com/")

    if req.status_code == 404:
        return False
    else:
        return True