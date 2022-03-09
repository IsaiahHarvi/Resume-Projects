#Enable or disable nsfw messages.
nsfw = True

#Get the id of the last person to send a message.
last_author = None

#Get the last gfuel file that was sent.
last_gfuel = None

#Stores bot token
token = "NjgyNDYyNTg5NTY0NzQ3ODAw.XldW0A.MH83dK53U3joQy1IbUaEkAIsuZU"

#Stores reddit secret.
reddit_secret = "CYBC6XsEl60GO56SvE1fqWOmag8"

#Stores reddit password.
reddit_password = "Richard91!"

#Uptime.
uptime = None

#LiarID.
liarID = None

#Spotify.
spotifyTimer = 300

#My personal ID.
ownerID = "247154017975664652"

#List of Authenticated Users. 
with open("IDs/auth.txt", "r") as authFile:
    authUsers = authFile.read().splitlines()

#List of Developers.
with open("IDs/devs.txt", "r") as devFile:
    devs = devFile.read().splitlines()