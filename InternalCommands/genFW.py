import requests
from bs4 import BeautifulSoup as bs
import discord

session = requests.session()

async def run(msg, sub, pageName = None):
    if pageName == None:
        req = session.get(f"https://{sub}.fandom.com/api.php?action=query&format=json&prop=info|extracts|pageimages&generator=random&inprop=url&grnnamespace=0")
    else:
        req = session.get(f"https://{sub}.fandom.com/api.php?action=query&format=json&prop=info|extracts|pageimages&inprop=url&titles={pageName}")

    try:
        data = req.json()
    except:
        embed = discord.Embed(title = f"ERROR IN GENERATING PAGE FROM {sub}", description = "This may be due to the sub being invalid, please verify")
        msg.edit(embed = embed)

    try:

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

        embed = discord.Embed(title = f"RANDOM PAGE FROM {sub.upper()}: {pageName}", description = text)
        await msg.edit(embed = embed)

        #get image
        imageUrl = None
        try:
            imageUrl = page["pageimage"]
        except Exception as e:
            print("no image")
            pass #no image on page
        else:
            try:
                imReq = session.get(f"https://{sub}.fandom.com/api.php?action=query&prop=imageinfo&iiprop=extmetadata&titles=File:{imageUrl}&format=json")
                imData = imReq.json()
                for pageId in imData["query"]["pages"].keys():
                    emd = imData["query"]["pages"][pageId]["imageinfo"][0]["extmetadata"]
                    break

                license = emd["UsageTerms"]["value"]
                author = emd["DateTime"]["value"]
                date = emd["DateTime"]["value"]
                licenseUrl = emd["LicenseUrl"]["value"]
            except Exception as e:
                print("Error ", e)
            else:
                #check if license is usable
                print(license, author, date, licenseUrl)
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
                    embed = discord.Embed(title = f"RANDOM PAGE FROM {sub.upper()}: {pageName}", description = text)
                    url = "https://commons.wikimedia.org/wiki/Special:FilePath/" + imageUrl
                    embed.set_thumbnail(url = url)
                    await msg.edit(embed = embed)
                else:
                    print("no accepted url")

    except:
        print(f"WE GOT A FANDOM WIKI ERROR\npageName: {pageName}\nerror: {e}")
        if pageName != None:
            embed = discord.Embed(title = f"Error generating wikipage with name: {pageName}", description = "Whoopsy, try checking your page name, for some reason it is case-sensitive")
        else:
            embed = discord.Embed(title = "Error in generating wiki", description = "whoopsy, let me know about this")
        
        await msg.edit(embed = embed)