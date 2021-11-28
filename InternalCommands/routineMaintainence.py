import json

async def run(bot):
    print("\nperforming maintainence:\n")

    with open("./Data/wikiSubs.json", "r") as file:
        data = json.load(file)

    #remove channels and servers with no subs
    for serverId in data.keys():
        serverEmpty = True
        for channelId in data[serverId]["CHANNELS"].keys():
            channelEmpty = True
            for hour in data[serverId]["CHANNELS"][channelId]["SUBS_BY_HOUR"].keys():
                if len(data[serverId]["CHANNELS"][channelId]["SUBS_BY_HOUR"][hour]) > 0:
                    channelEmpty = False
                    serverEmpty = False
            if channelEmpty:
                del data[serverId]["CHANNELS"][channelId]
        if serverEmpty:
            del data[serverId]

    with open("./Data/wikiSubs.json", "w") as file:
        json.dump(data, file, indent = 4)