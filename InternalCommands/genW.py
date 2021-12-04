from discord import message
import requests
from bs4 import BeautifulSoup as bs
import discord

session = requests.session()

async def run(msg, pageName = None):
    if pageName == None:
        req = session.get("https://en.wikipedia.org/w/api.php?action=query&format=json&prop=info|extracts|pageimages&generator=random&inprop=url&grnnamespace=0&piprop=thumbnail|name&pithumbsize=2000")
    else:
        req = session.get(f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=info|extracts|pageimages&inprop=url&titles={pageName}&piprop=thumbnail|name&pithumbsize=2000")

    try:

        data = req.json()

        pageId = data["query"]["pages"].keys()
        for key in pageId:
            page = data["query"]["pages"][key]
            break

        url = page["fullurl"]
        pageName = page["title"]

        parsedPage = bs(page["extract"], "html.parser")
        text = parsedPage.text
        text = text[:1000]
        try:
            text = text[:text.find("References")]
        except:
            pass

        text += f"\nFor more information: [{pageName}]({url})"

        embed = discord.Embed(title = f"RANDOM PAGE FROM WIKIPEDIA: {pageName}", description = text)
        await msg.edit(embed = embed)

        #get image
        imageUrl = None
        try:
            imageUrl = page["pageimage"]
        except Exception as e:
            pass #no image
        else:
            try:
                imReq = session.get(f"https://en.wikipedia.org/w/api.php?action=query&prop=imageinfo&iiprop=extmetadata&titles=File:{imageUrl}&format=json")
                imData = imReq.json()
                emd = imData["query"]["pages"]["-1"]["imageinfo"][0]["extmetadata"]

                license = emd["UsageTerms"]["value"]
                author = emd["DateTime"]["value"]
                date = emd["DateTime"]["value"]
                licenseUrl = emd["LicenseUrl"]["value"]
            except Exception as e:
                print("Error ", e)
            else:
                #check if license is usable
                acceptedlicense = None
                licenses = ["creative commons", "attribution-share alike 3.0", "attribution-share alike 4.0", "attribution 2.0", "public domain"]
                if license.lower() != "pd":
                    for lic in licenses:
                        if lic in license.lower():
                            acceptedlicense = license
                else:
                    acceptedlicense = license
                if acceptedlicense != None:
                    #found a valud license
                    text += f"\n[Hover for image license information](https://www.youtube.com/watch?v=dQw4w9WgXcQ 'license: {acceptedlicense}\nauthor: {author}\ndate: {date}\nlicenseUrl: {licenseUrl}')"
                    embed = discord.Embed(title = f"RANDOM PAGE FROM WIKIPEDIA: {pageName}", description = text)
                    url = "https://commons.wikimedia.org/wiki/Special:FilePath/" + imageUrl
                    embed.set_thumbnail(url = url)
                    await msg.edit(embed = embed)
    except Exception as e:
        print(f"WE GOT A WIKI ERROR\npageName: {pageName}\nerror: {e}")
        if pageName != None:
            embed = discord.Embed(title = f"Error generating wikipage with name: {pageName}", description = "Whoopsy, try checking your page name, for some reason it is case-sensitive")
        else:
            embed = discord.Embed(title = "Error in generating wiki", description = "whoopsy, let me know about this")
        
        await msg.edit(embed = embed)