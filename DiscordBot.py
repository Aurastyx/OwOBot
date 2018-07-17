import discord                                  # Needed by discord.py
import asyncio                                  # Needed by discord.py
import OwOStandardLibrary                       # Some of the nastier functions got moved here to keep the main file cleaner
from random import randint                      # Needed by the bot, used to play games of chance
from discord.voice_client import VoiceClient    # Needed by the bot, used only for audio playback

# If your reading this code, im so sorry, this isnt supposed to publicly available, im just too cheap to buy git premium for a private directory
# This is just a learning project for myself, the bot works and is mostly bug free but the code quality is beyond god awful 
# However it might be useful for other beginners to see some more specific usage of discord.py functions where the docs are fairly vague in their descriptions
# Just dont think of it as the right way to do things, it works, but it aint right 

class TestClient(discord.Client):           
    async def on_ready(self):                           # This SHOULD be used to set up the bot, right now it just alerts you when the bot has finished booting
        print('Logged in as user : ' + self.user.name)  
        print('with ID : ' + self.user.id)
        print('--------------------------------')

    async def on_message(self, message):                # Nasty uber function, it just reads a send message, matches the beginning of the message to a string and runs a corresponding function
        DiscMessage = message.content.casefold()        # This ensures case insensativity, never read messages directly, use this instead

        if message.author == self.user:                 # This just ensures that the bot doesnt get stuck in a feedback loop and reply to himself endlessly
            return
            
        if DiscMessage.startswith('owo coin'):          # Flips a coin and replies with heads or tails
            print ('Flipping coin in server: ' + message.server.name)
            if randint(0,1):
                await client.send_message(discord.Object(id=message.channel.id), 'Heads')
            else:
                 await client.send_message(discord.Object(id=message.channel.id), 'Tails')

        if DiscMessage.startswith('owo yiff'):          # Useless functions, might change it to do something funnier later on
            print ('Yiffing ' + message.author.name + 'In server' + message.server.name)
            await client.send_message(discord.Object(id=message.channel.id), 'Consider yourself Yiffed Mr ' + message.author.name, tts=True)
        
        if DiscMessage.startswith('owo calc'):          # Pretty insane security flaw, i use this for some minor debugging, dont ever allow this to be used on a public server
            MathsToDo = DiscMessage.lstrip ('owo calc')
            try:
                x = (eval (MathsToDo))                  # Here is the security flaw, this allows you to run python commands through the bot, slightly usefull for debugging,
                await client.send_message(discord.Object(id=message.channel.id), x)
                print ('Calculating In channel :' + message.server.name)
            except Exception as errorInfo:
                await client.send_message(discord.Object(id=message.channel.id), 'what the fuck are you trying to say')
                print ('Calculation error in channel : ' + message.server.name + str(errorInfo))
        
        if DiscMessage.startswith('owo lookup'):        # Scrapes the runescape highscores, if no skill is specified just returns unformated data
            RsLookup = DiscMessage.replace('owo lookup ', '')
            if len(RsLookup.split()) == 2:
                RsLookup = RsLookup.rsplit(' ', 1)
                RsLookupResults = OwOStandardLibrary.runescapeLookup(RsLookup[0], RsLookup[1])
                if len(RsLookupResults) == 3:
                    if RsLookupResults[0] != '--':
                        await client.send_message(discord.Object(id=message.channel.id), RsLookup[0] + ' has a ' + RsLookup[1] + ' level of ' + RsLookupResults[2] + ', with ' + RsLookupResults[1] + ' xp, making him rank ' + RsLookupResults [0] )
                        print ('Looking up : ' + RsLookup[1] + 'for player :' + RsLookup[0] + 'in server :' + message.server.name)
            else:
                RsLookupResults = OwOStandardLibrary.runescapeLookup(RsLookup, 0)
                await client.send_message(discord.Object(id=message.channel.id), RsLookup + str(RsLookupResults))
                print('looking up all stats for player : ' + RsLookup + 'in server : ' + message.server.name )

        if DiscMessage.startswith('owo wiki'):          # Scrapes the runescape wiki search function and returns the top article, could be moddified to work with any wikia website
            WikiLookupTag = DiscMessage.replace('owo wiki', '')
            RSWikiLookup = OwOStandardLibrary.rsWikiLookup(WikiLookupTag)
            await client.send_message(discord.Object(id=message.channel.id), RSWikiLookup)
            print ('looking up article' + WikiLookupTag + 'in server : ' + message.server.name)
        
        if DiscMessage.startswith('owo communism'):     # Nasty hacky audio player, currently just playes the soviet national anthem, 
            global OwOCffmpeg       #voice is handled by a voice object, however since this is being created at runtime the editor gets really upset about it
            global OwOVoiceClient   #it's all down to these globals, they are needed so that other functions can work with the same voice object
            
            if (OwOVoiceClient == 0):          
                OwOVoiceClient = await client.join_voice_channel(message.author.voice.voice_channel)
                OwOCffmpeg = OwOVoiceClient.create_ffmpeg_player('Audio/Communism/Communism.mp3')
                OwOCffmpeg.start()
            else:
                await OwOVoiceClient.move_to(message.author.voice.voice_channel)
                OwOCffmpeg.stop()
                OwOCffmpeg = OwOVoiceClient.create_ffmpeg_player('Audio/Communism/Communism.mp3')
                OwOCffmpeg.start()
            print('starting voice')

        if DiscMessage.startswith('owo stop'):          # Stops the audio player, uses a nasty global for this
            global OwOCffmpeg
            OwOCffmpeg.stop()
            print ('stopping voice')
            
        if DiscMessage.startswith('owo yoink'):         # Grabs a random player from the message author's channel and throws him into the afk channel
            channelToYoinkFrom = message.author.voice.voice_channel.voice_members
            playerToYoink = channelToYoinkFrom [ randint(0,(len(channelToYoinkFrom)-1)) ]
            print (playerToYoink)
            await client.move_member(playerToYoink, message.server.afk_channel)

        if DiscMessage.startswith('owo help'):          # Reads from a help file in the TextFiles directory
            helpFile = open('TextFiles/Help.txt','r') 
            helpLine = helpFile.read()
            await client.send_message(discord.Object(id=message.channel.id), helpLine)
            helpFile.close
            
        if DiscMessage.startswith('owo pet'):           # This is more proof of concept rather than something to activly use
            petCountFile = open('TextFiles/Pet.txt', 'r')   #it works, but you need to reset the pet count back to zero
            petCount = petCountFile.read()                  #it's also ugly as all hell, but i just call it code consistancy
            petCountFile.close
            petCount = int(petCount)
            petCount = petCount + 1
            petCount = str(petCount)
            await client.send_message(discord.Object(id=message.channel.id), '<:Hypers:443914491294515200> OwO bot has been petted ' + petCount + ' times <:Hypers:443914491294515200>' )
            petCountFile = open('TextFiles/Pet.txt', 'w')
            petCountFile.write(petCount)
            petCountFile.close()

            
OwOCffmpeg = 0 #These global's are "needed" to get the voice functions working properly
OwOVoiceClient = 0 #They cause so many horrible errors, but i just pretend their not there
client = TestClient()
discord.opus.load_opus('opus')
client.run('MzgzMzg4NjE4NjE1NDIyOTc2.DhwRAQ.GJfmZKcxFc05R5k2y9PCpSHJPys')