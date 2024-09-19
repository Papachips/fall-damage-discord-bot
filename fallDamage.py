import discord
from youtubesearchpython import VideosSearch
import sqlite3
import random
import requests

#creates database if it doesn't exist on my local pc
#this is only for tracking what youtube links have been posted to joeys-moshpit
def sql():
    conn = sqlite3.connect(r'PATH_HERE')
    cursor = conn.cursor()
    sql ='''CREATE TABLE IF NOT EXISTS YOUTUBE(URL text)'''
    cursor.execute(sql)
    conn.commit()
    conn.close()

#runs sql function
sql()

#instantiate discord instance
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#catches trigger events from messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #returns spotify playlist of music
    if (message.content.startswith('$spotify')):
       await sendSpotifyPlaylist(message)

    #returns random youtube link from playlist
    if (message.content.startswith('$youtube')):
        await getYouTubeLink(message)

    #get builds for various classes
    if (message.content.startswith('$deathknight')):
        await getBuilds(message, 'death knight', 'demon hunter', ['blood', 'frost', 'unholy'])
    
    if (message.content.startswith('$demonhunter')):
        await getBuilds(message, 'demon hunter', 'druid', ['havoc', 'vengeance'])

    if (message.content.startswith('$druid')):
        await getBuilds(message, 'druid', 'evoker', ['balance', 'feral', 'guardian', 'restoration'])

    if (message.content.startswith('$evoker')):
        await getBuilds(message, 'evoker', 'hunter', ['augmentation', 'devastation', 'preservation'])

    if (message.content.startswith('$hunter')):
        await getBuilds(message, 'hunter', 'mage', ['beast mastery', 'marksmanship', 'survival'])

    if (message.content.startswith('$mage')):
        await getBuilds(message, 'mage', 'monk', ['arcane', 'fire', 'frost'])

    if (message.content.startswith('$monk')):
        await getBuilds(message, 'monk', 'paladin', ['brewmaster', 'mistweaver', 'windwalker'])

    if (message.content.startswith('$paladin')):
        await getBuilds(message, 'paladin', 'priest', ['holy', 'protection', 'retribution'])

    if (message.content.startswith('$priest')):
        await getBuilds(message, 'priest', 'rogue', ['discipline', 'holy', 'shadow'])

    if (message.content.startswith('$rogue')):
        await getBuilds(message, 'rogue', 'shaman', ['assassination', 'outlaw', 'subtlety'])

    if (message.content.startswith('$shaman')):
        await getBuilds(message, 'shaman', 'warlock', ['elemental', 'enhancement', 'restoration'])

    if (message.content.startswith('$warlock')):
        await getBuilds(message, 'warlock', 'warrior', ['affliction', 'demonology', 'destruction'])

    if (message.content.startswith('$warrior')):
        await getBuilds(message, 'warrior', 'wowhead class writers', ['arms', 'fury', 'protection'])
    
    #randomize gender,race,class,and spec for new alt
    if (message.content.startswith('$alt')):
        await altChooser(message)

#sends back hardcoded spotify link for playlist
async def sendSpotifyPlaylist(message):
    await message.channel.send('SPOTIFY_PLAYLIST_URL_HERE')

#sends back youtube link from local file of songs from playlist
#will probably make this run once a day or something and not use a command to call it later
async def getYouTubeLink(message):
    #opens file
    f = open("PATH_HERE", 'r', encoding="utf-8")
    #puts all lines into code
    lines = f.readlines()
    #closes file
    f.close()
    #chooses random track from list. comes in as artist - track name
    searchTerms = lines[random.randint(0, len(lines)-1)]
    #search youtube and return top video from search terms
    link = VideosSearch(searchTerms, limit = 1)
    #gets link from search result    
    link = link.result()['result'][0]['link']

    #open database and get all currently posted links
    conn = sqlite3.connect(r'PATH_HERE')
    cursor = conn.cursor()
    cursor = conn.execute("SELECT * FROM YOUTUBE")
    results = cursor.fetchall()
    conn.close()

    #don't want to post duplicates, so skip if it's been posted
    #if not, post it and record to database
    if link not in str(results):
        conn = sqlite3.connect(r'PATH_HERE')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO YOUTUBE (URL) VALUES (?)", (link,))
        conn.commit()
        conn.close()
        await message.channel.send(link)
    else:
        #recursive call to run until it finds one it hasn't posted
        await getYouTubeLink(message)


    url = 'https://www.wowhead.com/guide/best-hero-talent-builds-all-war-within-classes-raids-mythic-plus-delves'
    content = str(requests.post(url).content)
    raidBuilds = content.split('Best Mage Talent Builds')[1].split('Best Monk Talent Builds')[0].split('[copy=\\\\"Raid\\\\"]')
    arcaneRaid =  raidBuilds[1].split('[\\\\/copy]')[0]
    fireRaid = raidBuilds[2].split('[\\\\/copy]')[0]
    frostRaid = raidBuilds[3].split('[\\\\/copy]')[0]

    mythicBuilds = content.split('Best Mage Talent Builds')[1].split('Best Monk Talent Builds')[0].split('[copy=\\\\"Mythic+\\\\"]')
    arcaneMythic =  mythicBuilds[1].split('[\\\\/copy]')[0]
    fireMythic = mythicBuilds[2].split('[\\\\/copy]')[0]
    frostMythic = mythicBuilds[3].split('[\\\\/copy]')[0]

    delveBuilds = content.split('Best Mage Talent Builds')[1].split('Best Monk Talent Builds')[0].split('[copy=\\\\"Delves"\\\\"]')[0].split('[copy=\\\\"Delves\\\\"]')
    arcaneDelve =  delveBuilds[1].split('[\\\\/copy]')[0]
    fireDelve= delveBuilds[2].split('[\\\\/copy]')[0]
    frostDelve = delveBuilds[3].split('[\\\\/copy]')[0]

    embeded = discord.Embed(title='Mage Builds - Wowhead', url='https://www.wowhead.com/guides/classes/mage')
    embeded.add_field(name = 'Beast Mastery Raid' , value = arcaneRaid)
    embeded.add_field(name = 'Marksmanship Raid' , value = fireRaid)
    embeded.add_field(name = 'Survival Raid' , value = frostRaid)
    embeded.add_field(name = chr(173), value = chr(173), inline = False)
    embeded.add_field(name = 'Beast Mastery Mythic+' , value = arcaneMythic)
    embeded.add_field(name = 'Marksmanship Mythic+' , value = fireMythic)
    embeded.add_field(name = 'Survival Mythic+' , value = frostMythic)
    embeded.add_field(name = chr(173), value = chr(173), inline = False)
    embeded.add_field(name = 'Beast Mastery Delve' , value = arcaneDelve)
    embeded.add_field(name = 'Marksmanship Delve' , value = fireDelve)
    embeded.add_field(name = 'Survival Delve' , value = frostDelve)
    await message.channel.send(embed=embeded)

#sends back builds from wowhead
async def getBuilds(message, currentClass:str, nextClass:str, specs):
    #builds are stored in a script tag so we need to get the page and parse it
    url = 'https://www.wowhead.com/guide/best-hero-talent-builds-all-war-within-classes-raids-mythic-plus-delves'
    content = str(requests.post(url).content)
    #get raid builds and navigate dom structure to find them
    raidBuilds = content.split(f'Best {currentClass.title()} Talent Builds')[1].split(f'Best {nextClass.title()} Talent Builds')[0].split('[copy=\\\\"Raid\\\\"]')
    raid1 =  raidBuilds[1].split('[\\\\/copy]')[0]
    raid2 = raidBuilds[2].split('[\\\\/copy]')[0]
    if (currentClass != 'demon hunter'):
        raid3 = raidBuilds[3].split('[\\\\/copy]')[0]
    if (currentClass == 'druid'):
        raid4 = raidBuilds[4].split('[\\\\/copy]')[0]

    #get mythic builds and navigate dom structure to find them
    mythicBuilds = content.split(f'Best {currentClass.title()} Talent Builds')[1].split(f'Best {nextClass.title()} Talent Builds')[0].split('[copy=\\\\"Mythic+\\\\"]')
    mythic1 =  mythicBuilds[1].split('[\\\\/copy]')[0]
    mythic2 = mythicBuilds[2].split('[\\\\/copy]')[0]
    if (currentClass != 'demon hunter'):
        mythic3 = mythicBuilds[3].split('[\\\\/copy]')[0]
    if (currentClass == 'druid'):
        mythic4 = mythicBuilds[4].split('[\\\\/copy]')[0]

    #get delve builds and navigate dom structure to find them
    delveBuilds = content.split(f'Best {currentClass.title()} Talent Builds')[1].split(f'Best {nextClass.title()} Talent Builds')[0].split('[copy=\\\\"Delves"\\\\"]')[0].split('[copy=\\\\"Delves\\\\"]')
    delve1 =  delveBuilds[1].split('[\\\\/copy]')[0]
    delve2= delveBuilds[2].split('[\\\\/copy]')[0]
    if (currentClass != 'demon hunter'):
        delve3 = delveBuilds[3].split('[\\\\/copy]')[0]
    if (currentClass == 'druid'):
        delve4 = delveBuilds[4].split('[\\\\/copy]')[0]   

    #create embedded message with link to wowhead with builds
    embeded = discord.Embed(title=f'{currentClass.title()} Builds - Wowhead', url=f'https://www.wowhead.com/guides/classes/{currentClass.replace(" ", "-")}')
    embeded.add_field(name = f'{specs[0].title()} Raid' , value = raid1)
    embeded.add_field(name = f'{specs[1].title()} Raid' , value = raid2)
    if (currentClass != 'demon hunter'):
        embeded.add_field(name = f'{specs[2].title()} Raid' , value = raid3)
    if (currentClass == 'druid'):
        embeded.add_field(name = f'{specs[3].title()} Raid' , value = raid4)
    embeded.add_field(name = chr(173), value = chr(173), inline = False)
    embeded.add_field(name = f'{specs[0].title()} Mythic+' , value = mythic1)
    embeded.add_field(name = f'{specs[1].title()} Mythic+' , value = mythic2)
    if (currentClass != 'demon hunter'):
        embeded.add_field(name = f'{specs[2].title()} Mythic+' , value = mythic3)
    if (currentClass == 'druid'):
        embeded.add_field(name = f'{specs[3].title()} Mythic+' , value = mythic4)
    embeded.add_field(name = chr(173), value = chr(173), inline = False)
    embeded.add_field(name = f'{specs[0].title()} Delve' , value = delve1)
    embeded.add_field(name = f'{specs[1].title()} Delve' , value = delve2)
    if (currentClass != 'demon hunter'):
        embeded.add_field(name = f'{specs[2].title()} Delve' , value = delve3)
    if (currentClass == 'druid'):
        embeded.add_field(name = f'{specs[3].title()} Delve' , value = delve4)
    await message.channel.send(embed=embeded)

#returns parameters for a new alt through randomized settings
async def altChooser(message):
    allRacesClasses = {}

    #horde
    allRacesClasses['Orc'] = ['Warrior', 'Hunter', 'Mage', 'Rogue', 'Priest', 'Warlock', 'Monk', 'Shaman', 'Death Knight']
    allRacesClasses['Undead'] = ['Warrior', 'Hunter', 'Mage', 'Rogue', 'Priest', 'Warlock', 'Monk', 'Death Knight']
    allRacesClasses['Tauren'] = ['Warrior', 'Hunter', 'Mage', 'Rogue', 'Priest', 'Warlock', 'Paladin', 'Druid', 'Monk', 'Shaman', 'Death Knight']
    allRacesClasses['Troll'] = ['Warrior', 'Hunter', 'Mage', 'Rogue', 'Priest', 'Warlock', 'Druid', 'Monk', 'Shaman', 'Death Knight']
    allRacesClasses['Blood Elf'] = ['Warrior', 'Hunter', 'Mage', 'Rogue', 'Priest', 'Warlock', 'Paladin', 'Monk', 'Demon Hunter', 'Death Knight']
    allRacesClasses['Goblin'] = ['Warrior', 'Hunter', 'Mage', 'Rogue', 'Priest', 'Warlock', 'Monk', 'Shaman', 'Death Knight']
    allRacesClasses['Nightborne'] = ['Warrior', 'Hunter', 'Mage', 'Rogue', 'Priest', 'Warlock', 'Monk', 'Death Knight', 'Demon Hunter']
    allRacesClasses['High Mountain Tauren'] = ['Warrior', 'Hunter', 'Mage', 'Rogue', 'Priest', 'Warlock', 'Druid', 'Monk', 'Shaman', 'Death Knight']
    allRacesClasses["Mag'har Orc"] = ['Warrior', 'Hunter', 'Mage', 'Rogue', 'Priest', 'Warlock', 'Monk', 'Shaman', 'Death Knight']
    allRacesClasses['Zandalari Troll'] = ['Warrior', 'Hunter', 'Mage', 'Rogue', 'Priest', 'Warlock', 'Paladin', 'Druid', 'Monk', 'Shaman', 'Death Knight']
    allRacesClasses['Vulpera'] = ['Warrior', 'Hunter', 'Mage', 'Rogue', 'Priest', 'Warlock', 'Monk', 'Shaman', 'Death Knight']

    #alliance
    allRacesClasses['Human'] = ['Warrior', 'Hunter', 'Mage', 'Rogue', 'Priest', 'Warlock', 'Paladin', 'Monk', 'Death Knight']
    allRacesClasses['Dwarf'] = ['Warrior', 'Hunter', 'Mage', 'Rogue', 'Priest', 'Warlock', 'Paladin', 'Shaman', 'Monk', 'Death Knight']
    allRacesClasses['Night Elf'] = ['Warrior', 'Hunter', 'Mage', 'Rogue', 'Priest', 'Warlock', 'Druid', 'Monk', 'Demon Hunter', 'Death Knight']
    allRacesClasses['Gnome'] = ['Warrior', 'Hunter', 'Mage', 'Rogue', 'Priest', 'Warlock', 'Monk', 'Death Knight']
    allRacesClasses['Draenei'] = ['Warrior', 'Hunter', 'Mage', 'Rogue', 'Priest', 'Warlock', 'Paladin', 'Shaman', 'Monk', 'Death Knight']
    allRacesClasses['Worgen'] = ['Warrior', 'Hunter', 'Mage', 'Rogue', 'Priest', 'Warlock', 'Druid', 'Monk', 'Death Knight']
    allRacesClasses['Void Elf'] = ['Warrior', 'Hunter', 'Mage', 'Rogue', 'Priest', 'Warlock', 'Monk', 'Death Knight']
    allRacesClasses['Lightforged Draenei'] = ['Warrior', 'Hunter', 'Mage', 'Rogue', 'Priest', 'Warlock', 'Paladin', 'Monk', 'Death Knight']
    allRacesClasses['Dark Iron Dwarf'] = ['Warrior', 'Hunter', 'Mage', 'Rogue', 'Priest', 'Warlock', 'Paladin', 'Shaman', 'Monk', 'Death Knight']
    allRacesClasses['Kul Tiran'] = ['Warrior', 'Hunter', 'Mage', 'Rogue', 'Priest', 'Warlock', 'Druid', 'Shaman', 'Monk', 'Death Knight']
    allRacesClasses['Mechagnome'] = ['Warrior', 'Hunter', 'Mage', 'Rogue', 'Priest', 'Warlock', 'Monk', 'Death Knight']

    #neutral
    allRacesClasses['Pandaren'] = ['Warrior', 'Hunter', 'Mage', 'Rogue', 'Priest', 'Warlock', 'Monk', 'Shaman', 'Death Knight']
    allRacesClasses['Dracthyr'] = ['Hunter', 'Rogue', 'Priest', 'Mage', 'Warrior', 'Warlock','Evoker']
    allRacesClasses['Earthen'] = ['Hunter', 'Mage', 'Monk', 'Paladin', 'Priest', 'Rogue', 'Shaman', 'Warlock', 'Warrior']

    allSpecs = {}

    allSpecs['Warrior'] = ['Arms', 'Fury', 'Protection']
    allSpecs['Hunter'] = ['Beast Mastery', 'Marksmanship', 'Survival']
    allSpecs['Mage'] = ['Arcane', 'Fire', 'Frost']
    allSpecs['Rogue'] = ['Assassination', 'Outlaw', 'Subtlety']
    allSpecs['Priest'] = ['Discipline', 'Holy', 'Shadow']
    allSpecs['Warlock'] = ['Affliction', 'Demonology', 'Destruction']
    allSpecs['Shaman'] = ['Elemental', 'Enhancement', 'Restoration']
    allSpecs['Monk'] = ['Brewmaster', 'Mistweaver', 'Windwalker']
    allSpecs['Death Knight'] = ['Blood', 'Frost', 'Unholy']
    allSpecs['Druid'] = ['Balance', 'Feral', 'Guardian', 'Restoration']
    allSpecs['Evoker'] = ['Augmentation', 'Devestation', 'Preservation']
    allSpecs['Paladin'] = ['Protection', 'Holy', 'Retribution']
    allSpecs['Demon Hunter'] = ['Havoc', 'Vengeance']

    #get race
    raceToPlay = random.choice(list(allRacesClasses))

    #get class
    classIndex = random.randint(0, len(allRacesClasses[raceToPlay])-1)
    classToPlay = allRacesClasses[raceToPlay][classIndex]

    #get spec
    specIndex = random.randint(0, len(allSpecs[classToPlay])-1)
    specToPlay = allSpecs[classToPlay][specIndex]

    #get gender
    gender = 'Male ' if random.randint(0,1) == 1 else 'Female '

    #only get faction if allied race, otherwise skip
    if (raceToPlay == 'Dracthyr' or raceToPlay == 'Pandaren' or raceToPlay == 'Earthen'):
        hordeOrAlliance = 'Horde ' if random.randint(0, 1) == 1 else 'Alliance '
        await message.channel.send(hordeOrAlliance + gender + raceToPlay + ' ' + specToPlay +' ' + classToPlay)
    else:
        await message.channel.send(gender + raceToPlay + ' ' + specToPlay +' ' + classToPlay)

#runs the bot on discord
client.run('API_KEY_HERE')