import discord
import asyncio
import OwOStandardLibrary
from time import sleep
from random import randint
from discord.voice_client import VoiceClient



class TestClient(discord.Client):
    async def on_ready(self):
        print('Logged in as user : ' + self.user.name)
        print('with ID : ' + self.user.id)
        print('--------------------------------')

    async def on_message(self, message):
        DiscMessage = message.content.casefold()

        if message.author == self.user:
            return
            
        if DiscMessage.startswith('owo coin'):
            print ('Flipping coin in server: ' + message.server.name)
            if randint(0,1):
                await client.send_message(discord.Object(id=message.channel.id), 'Heads')
            else:
                 await client.send_message(discord.Object(id=message.channel.id), 'Tails')

        if DiscMessage.startswith('owo yiff'):
            print ('Yiffing ' + message.author.name + 'In server' + message.server.name)
            await client.send_message(discord.Object(id=message.channel.id), 'Consider yourself Yiffed Mr ' + message.author.name, tts=True)
        
        if DiscMessage.startswith('owo calc'):
            MathsToDo = DiscMessage.lstrip ('owo calc')
            try:
                x = (eval (MathsToDo))
                await client.send_message(discord.Object(id=message.channel.id), x)
                print ('Calculating In channel :' + message.server.name)
            except Exception as errorInfo:
                await client.send_message(discord.Object(id=message.channel.id), 'what the fuck are you trying to say')
                print ('Calculation error in channel : ' + message.server.name + str(errorInfo))
        
        if DiscMessage.startswith('owo lookup'):
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

        if DiscMessage.startswith('owo wiki'):
            WikiLookupTag = DiscMessage.replace('owo wiki', '')
            RSWikiLookup = OwOStandardLibrary.rsWikiLookup(WikiLookupTag)
            await client.send_message(discord.Object(id=message.channel.id), RSWikiLookup)
            print ('looking up article' + WikiLookupTag + 'in server : ' + message.server.name)
        
        if DiscMessage.startswith('owo communism'):
            global OwOCffmpeg
            global OwOVoiceClient
            
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

        if DiscMessage.startswith('owo stop'):
            global OwOCffmpeg
            OwOCffmpeg.stop()
            print ('stopping voice')
            
        if DiscMessage.startswith('owo yoink'):
            channelToYoinkFrom = message.author.voice.voice_channel.voice_members
            playerToYoink = channelToYoinkFrom [ randint(0,(len(channelToYoinkFrom)-1)) ]
            print (playerToYoink)
            await client.move_member(playerToYoink, message.server.afk_channel)

        if DiscMessage.startswith('owo help'):
            helpFile = open('TextFiles/Help.txt','r') 
            helpLine = helpFile.read()
            await client.send_message(discord.Object(id=message.channel.id), helpLine)
            helpFile.close
            
        if DiscMessage.startswith('owo pet'):
            petCountFile = open('TextFiles/Pet.txt', 'r')
            petCount = petCountFile.read()
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