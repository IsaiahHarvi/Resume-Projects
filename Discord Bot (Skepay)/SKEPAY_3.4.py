#|=-=-=| Imports |=-=-=|#
import argparse
from ast import Pass
import csv
import io
import json
import os
import random
import re
import smtplib
import ssl
import string
import subprocess
import sys
import time
from datetime import datetime
from discord import Spotify
from random import randint

import discord
import discord.utils
import praw
import wget
from discord.ext import commands
from discord.utils import get

import config

#|=-=-=-=-=-=-=-=-=-=-=|#
#|        v3.4         |#
#|=-=-=-=-=-=-=-=-=-=-=|#
bot = commands.Bot(command_prefix = '>', description="Bot Skepay Help Commands.")
config.uptime = time.time()

#|=-=-=| Start Here |=-=-=|#

@bot.event
async def on_ready():
    print('Started %s'%os.path.basename(__file__), end = ' ')
  


#|=-=-=| Functions |=-=-=|#
def PunctuateList(list1): # Split string ", , , and, ".
    return ', '.join(list1[:-1]) + ', and ' + list1[-1]


def getId(userMentioned): # Get users id, has to remove the discord notation (<@!>)
    mentioned_user_str = ""
    for i in userMentioned:
       if i in string.digits:
           mentioned_user_str += str(i)
    return mentioned_user_str



#|=-=-=| Commands |=-=-=|#
@bot.command() # INVITE LINK W/ EMBED
async def invite(ctx):
    embed_invite = (discord.Embed(description='Discord - A New Way to Chat with Friends & Communities\n https://discordapp.com/oauth2/authorize?&client_id=682462589564747800&scope=bot&permissions=8', color=0x3DF270))
    embed_invite.set_author(name='Invite Skepay Bot to your discord server!', icon_url='')
    embed_invite.set_image(url='https://discord.com/assets/ee7c382d9257652a88c8f7b7f22a994d.png')
    await ctx.send(embed=embed_invite)


@bot.command() # READ TEXT CHAT LOG IN DISCORD
async def log(ctx):
    readLog = open("/home/ubuntu/TextFiles/log.txt","r")
    logMsg = readLog.read()
    logLength = len(logMsg) - 1000
    await ctx.send("```\nReading Log:\n%s```"%logMsg[logLength:1000+logLength])


@bot.command() # CLEAR THE LOG
async def clear(ctx):
    if str(ctx.author.id) == config.ownerID:
        log_delete = open('/home/ubuntu/TextFiles/log.txt','r+')
        log_delete.truncate(0)
        log_delete.close()
        await ctx.message.delete()
    else:
        await ctx.send("You do not have the permissions to clear log.")


@bot.command() # TOGGLES FOR OTHER FUNCTIONS
async def toggle(ctx, boolean_name):
    if str(ctx.author.id) == config.ownerID:        
        if boolean_name == "nsfw":
            config.nsfw = not config.nsfw
            await ctx.send("Set %s to: %s"%(boolean_name, config.nsfw))

        else:
            await ctx.send("Couldnt find a toggle with the name \"%s\""%boolean_name)
    else:
        await ctx.send("Only <@!247154017975664652> can use this command.")


@bot.command() # COMMUNICATES WITH LINUX TERMINAL FROM DISCORD
async def bash(ctx, *command):
    if str(ctx.author.id) in config.ownerID: # if it is myself who is sending the message
        command = ' '.join(command)
        try:
            bash = os.popen(command)
            await ctx.send("```\n%s\n```"%bash.read())

        except Exception as Linux_Error:
            await ctx.send("```\n%s```"%str(Linux_Error))
    

@bot.command() # SKEPAY SAYS
async def say(ctx, *arg): # * gets all words
    await ctx.send(' '.join(arg))
    await ctx.message.delete()


@bot.command() # REDDIT WEB SCRAPER
async def r(ctx, subChoice, limit = None):
    try:
        reddit = praw.Reddit(client_id = '-nK5Ai3qBkefMg', client_secret = config.reddit_secret, user_agent = 'Skepay', username = 'skepay2', password = config.reddit_password); censoredSubs = ["porn","nsfw","hentai","animetitties","simps","blowjob","anal"]
        subreddit = reddit.subreddit(subChoice)
        if type(limit) == int and limit <= 500:
            SubRed = subreddit.hot(limit = int(limit))
        else:
            SubRed = subreddit.hot(limit = 10)
        post = random.choice(list(SubRed))
        submission = reddit.submission(id=post)

        # embed msg
        RedditEmbed = discord.Embed(color = 0x00FFD4)
        RedditEmbed.set_author(name = submission.title, url = 'http://www.reddit.com/%s'%submission.id) # sets the submission title and allows it to take you to the url when clicked
        RedditEmbed.description = submission.selftext
        RedditEmbed.set_footer(text='%s Upvotes         %s Comments'%("{:,}".format(submission.score), submission.num_comments)) # number of comments and upvotes

        if submission.over_18: # if the subreddit is tagged as nsfw
            if config.nsfw: # if nsfw messages are enabled
                if subChoice not in censoredSubs: # if the user isnt trying to use a disabled subreddit
                    if 'nsfw' not in submission.title.lower(): # adds [NSFW] to the description of the post
                        RedditEmbed.set_author(name = '%s\n[NSFW]'%submission.title, url = 'http://www.reddit.com/%s'%submission.id)
                
                    DirToPicture  = os.path.dirname(os.path.abspath(__file__)) 
                    pic_file = wget.download(submission.url, DirToPicture) # downloads the picture in the subreddit
                    os.rename(pic_file, 'SPOILER_picture.png') # renames the picture to have SPOILER_ so discord will spoil it
                    
                    await ctx.send(embed = RedditEmbed)
                    await ctx.send(file = discord.File('%s/SPOILER_picture.png'%DirToPicture))

                    os.popen('rm %s/SPOILER_picture.png'%DirToPicture) # deletes the picture to save storage
                    
                else: # if the subreddit isnt allowed
                    await ctx.send("This subreddit is disabled <@!%s>.. you pervert."%str(ctx.author.id))
                    return
            else: # if nsfw messages are disabled in the servers
                await ctx.send("NSFW messages are disabled.")
                return
             
        else: # if the post isnt nsfw
            RedditEmbed.set_image(url = submission.url)
            await ctx.send(embed = RedditEmbed)
    
    except Exception as redditError: # discord specific error messages to be output in text channel
        if '(error code: 50035)' in str(redditError): # too long of a message
            redditError = 'The description of this post was too large to send to discord.'
        elif '/subreddits/search' in str(redditError) or '`display_name`' in str(redditError) or '403' in str(redditError) or 'empty sequence' in str(redditError): # finding subreddit error substitution
            redditError = 'Couldnt find subreddit with that name.  Check your spelling.'

        await ctx.send("```\n%s```"%str(redditError))

    
@bot.command() # LIE COUNTER
async def lied(liar):
    if liar == '<@!247154017975664652>': # cant accuse me for lying
        config.liarID = None
        return 'Isaiah would never tell a lie!'

    fileNames = []
    fileLies = []
    with open ('lies.csv', newline = '') as file:
        filedata = csv.reader(file,delimiter = ',')
        for row in filedata:
            fileNames.append(row[0])
            fileLies.append(int(row[1]))

    index = None
    for i in range(len(fileNames)):
        if liar.lower() == fileNames[i]:
            index = i 

    if not index:
        index = len(fileNames)
        fileNames.append(liar.lower())
        fileLies.append(0)
    fileLies[index] += 1


    with open('lies.csv', mode = 'w') as w:
        ew = csv.writer(w, delimiter = ',', lineterminator='\n')
        for i in range(len(fileNames)):
            ew.writerow([fileNames[i],fileLies[i]])
    
    config.liarID = None
    return 'The %s lie counter has been incremented by 1.\n%s has lied %g times now.'%(liar, liar, fileLies[index])


@bot.command() # LIAR LEADERBOARD
async def liars(ctx):
    board = {}
    outStr = ""
    with open('lies.csv', newline = '') as leaderboard_file:
        leaderboard_data = csv.reader(leaderboard_file, delimiter = ',')
        for row in leaderboard_data:
            board[row[0]] = int(row[1])

    sortedLies = sorted(board.items(), key=lambda x: x[1], reverse=True) # Sort the dictionary items

    for index, i in enumerate(sortedLies[0:5]):
        outStr += "%g. %s - %s\n"%(index+1, i[0], i[1])

    # Embed
    LBembed = discord.Embed(color = 0x00FFD4)
    LBembed.set_author(name = 'Liar Leaderboard')
    LBembed.description = outStr

    await ctx.send(embed = LBembed)


@bot.command() # QUADRIATIC FORMULA
async def math(ctx, *equation):
    try:
        a = int(equation[0])
        b = int(equation[1])
        c = int(equation[2])
    except:
        await ctx.send("Error converting input to integers.")
        return

    d = b**2 - 4*a*c
    if d < 0:
        await ctx.send("```\nThere are zero solutions.\n```")
    elif d == 0:
        x1 = -b/(2*a)
        await ctx.send("```\nThere is a singular solution:\n%g\n```"%x1)
    else:
        x1 = (-b+math.sqrt(d))/(2*a)
        x2 = (-b-math.sqrt(d))/(2*a)
        await ctx.send('```\nThere are two solutions for this problem:\n%g\n%g\n```'%(x1, x2))


@bot.command() # FACTOR NUMBER
async def factor(ctx, n):
    n = int(n)
    try:
        if n <= 10000000000:
            factors = set(
                factor for i in range(1, int(n**0.5) + 1) if n % i == 0 for factor in (i, n//i)
                ) # Supposedly the fastest method of factoring in Python

            factors = list(factors)
            factors.sort()
            await ctx.send("```\nThe factors of %s are:\n%s```"%(str(n), ', '.join(map(str, factors))))

        else:
            await ctx.send("Your number is too high to factor quickly.")

    except ValueError:
        await ctx.send("Error most likely due to your input.")


@bot.command() # FLIP
async def flip(ctx):
    await ctx.send("It is %s"%random.choice(["Heads","Tails"]))


def writeGfuel(tier_flavor, gfuelList, file): # writes to the user specific energy drink tierlist
    if "r" in tier_flavor[0]: 
        gfuelList.remove(gfuelList[int(tier_flavor[1])-1])

    elif "swap" in tier_flavor[0]:
        gfuelList[int(tier_flavor[1])-1], gfuelList[int(tier_flavor[2])-1] = gfuelList[int(tier_flavor[2])-1], gfuelList[int(tier_flavor[1])-1]

    else:
        with open(file, 'r') as f: gfuelFile = f.readlines()
        
        if not len(gfuelFile): # If the file contents are empty, just write the given flavor.
            with open(file, 'a') as wf:
                wf.write(' '.join(tier_flavor[1:]))
            return             

        gfuelList.insert(int(tier_flavor[0])-1, "%s\n"%' '.join(tier_flavor[1:])) # If there is something in the file, write the flavor in order.

    with open(file, 'w') as gfw:
        gfw.write(''.join(gfuelList))


@bot.command()
async def gfuel(ctx, *tier_flavor):
    outStr = ""
    fileName = "gfuels/gfuel_%s.txt"%str(ctx.author.id)
    authorName = str(ctx.author.id)

    if tier_flavor and "<" in tier_flavor[0] and ">" in tier_flavor[0]:
        foundFile = False
        for i in os.listdir('gfuels'):
            if getId(tier_flavor[0]) in i:
                fileName = "gfuels/%s"%i
                authorName = getId(tier_flavor[0])
                foundFile = True
                break

        if not foundFile:
            await ctx.send("```perl\nThis user doesn't have a GFUEL Tier List.  Tell them to make one with \">gfuel {integer rank}{flavor}\"!```")
            return # sus

    else:
        try:
            with open(fileName, 'r') as gfr:
                gfuelList = gfr.readlines()
        except FileNotFoundError:
            open(fileName, 'w').close() # Create a file with the users ID

        if tier_flavor: # If theyre adding to the list
            writeGfuel(tier_flavor, gfuelList, fileName)
            

    # Send File Contents.
    with open(fileName, 'r') as gfro: # Check updated file
        gff = gfro.readlines()

    if not len(gff): # If the file is empty
        outStr = "This Tier List is currently empty.\nUse \">gfuel {integer rank}{flavor}\" to add flavors."

    else: # If the file isnt empty
        for index, i in enumerate(gff):
            outStr += "%g.%s%s"%(index+1, "   "[0:-len(str(index+1))], i)   


    await ctx.send("**<@!%s>'s GFUEL TIER LIST**\n```perl\n%s```"%(authorName, outStr))


@bot.command() # sends a random drink from the users energy drink tierlist
async def randomGfuel(ctx, *args):
    with open('gfuels/gfuel_%s.txt'%str(ctx.author.id), 'r') as gfr:
        gfuelList = gfr.readlines()

    await ctx.send(random.choice(["Pop open a good ol'", "Drink a", "Personally, I'll be drinking some ", "Pour yourself some"]) + " " + random.choice(gfuelList))


@bot.command() # SEND USER ID
async def id(ctx, user):
    await ctx.send(getId(user))


""" Moderation Commands now Disabled by request.
@bot.command() # PURGE
async def purge(ctx, amount):
    await ctx.channel.purge(limit=int(amount)+1)
    await ctx.send("<@!%s> deleted %s messages"%(str(ctx.author.id), str(amount)))


@bot.command() # BAN
async def ban(ctx, member: discord.Member, reason = None):
    if str(member.id) != "247154017975664652":
        await member.ban(reason=reason)
        await ctx.send("Banned %s from the server."%member)


@bot.command() # KICK
async def kick(ctx, member: discord.Member, reason = None):
    if str(member.id) != "247154017975664652":
        await member.kick(reason=reason)
        await ctx.send("Kicked %s from the server."%member)


@bot.command(pass_context=True)
async def add role(ctx, user:discord.Member, role: discord.Role):
    if user and role:
        await user.add_roles(role)
        await ctx.message.delete()

    else:
        await ctx.send("There was an error fetching the user and role object.")
"""
            

@bot.command()
async def uptime(ctx):
    uptime = ((time.time() - config.uptime)/60)/60
    uptime = str(uptime)[0:str(uptime).index('.')+3]
    await ctx.send("```\n%s Uptime\n%s HOURS\n```"%(os.path.basename(__file__),str(uptime)[0:5]))
    

@bot.command() # With Spotify utilities, checks the users spotify status
async def spotify(ctx, user: discord.Member, activity=True):
    for i in user.activities:
        if isinstance(i, Spotify):
            if activity:
                Sembed = discord.Embed(color=0x0ff00)
                Sembed.set_thumbnail(url=i.album_cover_url)
                Sembed.title = "%s's Spotify Status"%user.name
                Sembed.description = "Listening to %s."%i.title
                Sembed.add_field(name="Artist", value=i.artist)
                Sembed.add_field(name="Album", value=i.album)
                await ctx.send(embed=Sembed)
            
            await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=i.title)) # Sets skepay status
            if str(user.id) != config.ownerID: config.spotifyTimer = time.time()                                                                  # Sets 5 min timer so skepay status wont be spammed
            return

    if activity: 
        try:
            await ctx.send("Couldn't find a Spotify status for this user.")
        except: pass


@bot.command()
async def version(ctx):             
    await ctx.send('```\nVERSION\nCurrently running %s\n\n%s```'%(os.path.basename(__file__), patchnotes))


@bot.listen()
async def on_message(message):
    msgStr = message.content; msgList = message.content.split()
    #Print message information.
    print('NAME: %s   ID: %s\n%s\n'%(message.author, str(message.author.id), msgStr))



    #Logging messages.
    if str(message.author.id) != "682462589564747800": # If it is not a self message
        try:
            logFilePath = "/home/ubuntu/application/TextFiles/log.txt"
            log_size = os.path.getsize(logFilePath)
        except:
            log_size = 0
            logFilePath = "log.txt"

        if log_size < 50000:
            writingContent = list(message.content)
            # Remove embed quotes and filtered words for other bots.
            if "`" in writingContent:
                while "`" in writingContent:
                    writingContent.remove("`")

            writingContent = ''.join(writingContent)

            log = open(logFilePath, 'a')
            if str(message.author.id) == config.last_author:
                log.write('%s\n'%(writingContent))
            else:
                log.write('\n\n%s\n%s\n'%(message.author,writingContent))
            log.close()
        else:
            logClear = open(logFilePath,'r+')
            logClear.truncate(0)
            logClear.close()


    # Lie Counter.
    if len(msgList) == 2 and "<" in msgList[0] and ">" in msgList[0]:
        # Calls the lie asynchrinous lie function
        if "lie" in msgList[1]:
            if getId(msgList[0]) == str(message.mentions[0].id):
                config.liarID = msgList[0]
                await message.channel.send(await lied(str(config.liarID)))

            else:
                await message.channel.send("I couldn't find the liar you are mentioning.")


    # Solve Rudimentary Math.
    if len(msgList) == 3 and msgList[1] in ["+","-","/","*"]:
        try:
            int(msgList[0]); int(msgList[2]) # Just to be sure these are numbers.
            ans = eval("%s %s %s"%(msgList[0], msgList[1], msgList[2]))
            await message.channel.send(ans)
        except: pass


    # Check Spotify.
    if time.time()-config.spotifyTimer >= 300:
        await spotify(message, message.author, activity=False)

    
    # Thanks.
    if 'thank' in msgStr.lower() and 'skep' in msgStr.lower():
        await message.channel.send('You\'re welcome, %s.'%message.author.name)


    # Youre filter.
    if 'youre' in msgStr.lower() and not randint(0,5):
        await message.channel.send('%sou\'re*'%msgStr[msgStr.lower().index('youre')][0])


    # Sets id of the last user to send a message.
    config.last_author = str(message.author.id)





bot.run(config.token)
