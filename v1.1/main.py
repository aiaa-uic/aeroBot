#
# aeroBot
#
# This is the main file for the AIAA @ UIC Discord bot
# Features:
# Poll Command, Role Reactions Managemanet, various silly features, dice roller
#
# Coming Soon?:
# Starboard, remind command (multiple users???)
#
# Philip Korus 7/26/2021
# UIC EE 2022
#
import discord
import time 
import threading
import os
import asyncio
import random

#from dotenv import load_dotenv
from discord import message

# pre-release version that will be shown to the board
versionNum = 0.9

intents=intents=discord.Intents.all()
client = discord.Client(intents=intents)

# a global variable used to add reactions to the rolle message
globalRoleMsg = None

DEBUG = True

# the persons discord ID that DM's sent to the bot will be routed to
botOverLordID = 233611399169966081 

# I dont thing we need
#newMemberRoleID = 841828431956279296

# have to update the blow items with server speific ID's / variables / emojis
roleInfo = [
  {
    'name': 'New Member',
    'emoji': "👶",
    'ID':841828431956279296,
    'roleAccess':None
  },
  {
    'name': 'DBF',
    'emoji': "✈️",
    'ID':836398938235338772,
    'roleAccess':None
  },
  {
    'name': 'Rocketry',
    'emoji': "🚀",
    'ID':836398929402527764,
    'roleAccess':None
  },
  {
    'name': 'Drone',
    'emoji': "💨",
    'ID':836398936104894474,
    'roleAccess':None
  },
  {
    'name': 'Undecided',
    'emoji': "❓",
    'ID':841851497419505674,
    'roleAccess':None
  }
]
guildID = 836392576084738050

#@slash.slash(name="test", description="This is just a test command, nothing more.")

# events that occur when the bot first starts up
@client.event
async def on_ready():
  await bootSequence()

# reaction based events
@client.event
async def on_reaction_add(reaction, user):
  global golbalRoleMsg

  if(globalRoleMsg!=None):
    if(reaction.message.id == globalRoleMsg.id):
      await userAddRoles(reaction, user)

  # gold star feature only works on messages sent while the bot was on, no access to the bots previous message
  # alpha feature
  if(reaction.emoji=="⭐"):
    messageReactionListTemp = reaction.message.reactions
    sumTemp = 0
    for x in range(len(messageReactionListTemp)):
      if(messageReactionListTemp[x].emoji=="⭐"):
        sumTemp = sumTemp + 1

    if(sumTemp > 0):
      AIAAGuild = client.get_guild(guildID)
      starChannel = AIAAGuild.get_channel(836392576084738053)

      await starChannel.send(":star:__"+str(sumTemp)+" Message From:"+reaction.message.author.display_name+"__\n"
      +"> "+reaction.message.content+"\n \n"
      +reaction.message.jump_url)

# message based events
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif isinstance(message.channel, discord.DMChannel):
      await botRecieveDM(message)
    else:
      if(message.content.startswith('!poll')):
        await pollCommand(message)

      elif(message.content.startswith('!roll')):
        await rollCommand(message)

      elif(message.content.startswith('!version')):
        await message.channel.send("__AeroBot Version "+str(versionNum)+"__: Released 8/7/2021")

      elif(message.content.startswith("!help")):
        await helpCommand(message.channel) 

      elif(message.content.startswith('!boop')):
        await boopCommand(message)

      elif(message.content.startswith('!b')):
        await bCommand(message)

      elif(message.content.startswith('!remind')):
        if(validateRemind(message.content)):
          timeWait = await remindTimeParse(message.content)

          #timeWait

          await asyncio.sleep(timeWait)  # 30 seconds delay?
          await job(message)
        else:
          await message.channel.send("Invalid Remind Command: need two commas")

      # a stupid little 'command' to test if the bot is still alive
      elif( (message.content.startswith("rocketz")) | (message.content.startswith("planez")) | (message.content.startswith("dronez")) ):
        await message.channel.send("GO BRRRRRRRR")
      

# events based on when a new person joins the server
@client.event
async def on_member_join(member):
  await newMember(member)

async def bCommand(message):
  messageToSend = ""
  messageLowerAnalyze = message.content
  while( messageLowerAnalyze.find("b")!=-1):
    bLocation = messageLowerAnalyze.find("b")
    if(bLocation==0):
        print("hi")
        messageToSend= "🅱"
    elif(messageLowerAnalyze[bLocation-1]==" "):
        print("trust")
        messageToSend= messageToSend+messageLowerAnalyze[0:bLocation]+" 🅱"
        
    print("DEBUG:"+messageLowerAnalyze)    
    messageLowerAnalyze = messageLowerAnalyze[bLocation+1:]
    
  messageToSend =  messageToSend+messageLowerAnalyze[0:bLocation]

  messageUpperAnalyze = messageToSend
  while( messageUpperAnalyze.find("B")!=-1):
    bLocation = messageUpperAnalyze.find("B")
    if(bLocation==0):
        print("hi")
        messageToSend= "🅱"
    elif(messageUpperAnalyze[bLocation-1]==" "):
        print("trust")
        messageToSend= messageToSend+messageUpperAnalyze[0:bLocation]+" 🅱"
        
    print("DEBUG:"+messageUpperAnalyze)    
    messageUpperAnalyze = messageUpperAnalyze[bLocation+1:]
    
  messageToSend =  messageToSend+messageUpperAnalyze[0:bLocation]
  await message.channel.send(messageToSend)



#
# helpCommand(message.channel)
#
# pritns out help info
async def helpCommand(msgChannel):
  await msgChannel.send("__Supported commands: (enter in the command for sytanx)__ \n"
  + "!roll : rolls a dice of user's choice \n"
  + "!poll : created a reaction poll, suports up to 10 options\n"
  + "!remind : bot will send a delayed reminder message to user/s \n"
  + "!version : gets my current version number\n"
  + "!help : you dummy it should be obvious what this is >:(\n"
  + "!boop : boops user/s, essentially just a cuter @ uwu \n"
  + "'rocketz', 'dronez', 'planez': GO BRRRRRRRR ")

#
# boopCommand(meessage)
#
# boops a user, essentially a  cuter ping, uwu rawr X3
async def boopCommand(message):
  usersToBeBooped = message.mentions
  boopMsg = ""
  for x in range (len(usersToBeBooped)):
    boopMsg = boopMsg + usersToBeBooped[x].mention +" "
  if(boopMsg == ""):
    await message.channel.send("Syntax: !boop @user1 @user2 ...")
  else:
    if(len(usersToBeBooped)>1):
      boopMsg = boopMsg + "have been booped by "+message.author.mention
    else:
      boopMsg = boopMsg + "has been booped by "+message.author.mention
    await message.channel.send(boopMsg)
    
#
# rollCommand(message)
#
# rolls a dice of the user choice 1d5 or 2d7
async def rollCommand(message):
  dice = message.content[6:]
  dPos = dice.find("d")
  if(dPos != -1):
    numOfDice = int(dice[:dPos])
    valueOfDice = int(dice[dPos+1:])
    if((numOfDice > 0)):
      if(valueOfDice>0):
        diceRollMsg = ""
        for x in range(numOfDice):
          roll = random.randint(0,valueOfDice)
          diceRollMsg = diceRollMsg + "Di #"+str(x+1)+", has value of: "+str(roll)+"\n"
        await message.channel.send(diceRollMsg)
      else:
        await message.channel.send("Invalid dice command: Value of dice must be greater than zero!")
        
    else:
      await message.channel.send("Invalid dice command: Number of dice must be greater than zero!")
  else:
    await message.channel.send("Invalid dice command")

#
# botRecieveDM(message)
#
# helper function handler for if a user dm's the bot, gets forwarded to who ever the Bot Overlord is, be sure
# to replace the user ID as needed
async def botRecieveDM(message):
  temp = client.get_user(botOverLordID)
  await temp.send("__**DM from: "+message.author.name + "#" + message.author.discriminator+"**__\n"+message.content)

def validateRemind(messageIn):
  firstComma = messageIn.find(",")
  print(firstComma)
  if((firstComma)!=-1):
    messageCut = messageIn[firstComma+1:]
    secondComma = messageIn.find(",")
    if(secondComma!=-1):
      return True
  else:
    print("whats up")
    return False


#
# remindTimeParse(messageIn)
#
# pulls out the needed info for the remind command
async def remindTimeParse(messageIn):
  print(messageIn)
  if( messageIn.find(",")!=-1 ):
    messageMinusAts = messageIn[messageIn.find(",")+1:]
    hoursColon = messageMinusAts.find(":")
    hours = messageMinusAts[0:hoursColon]
    
    messageMinusAts = messageMinusAts[hoursColon+1:]
    minColon = messageMinusAts.find(":")
    min = messageMinusAts[:minColon]
    messageMinusAts = messageMinusAts[minColon+1:]

    seconds = messageMinusAts[0:messageMinusAts.find(",")]


    if(DEBUG):
      print("DEBUG: Hours: "+hours+" Min: "+min+" Sec: "+seconds)

    return (int(hours)*3600)+(int(min)*60)+(int(seconds))

  else:
    return -999


#
# bootSequence()
#
# boot sequence for the bot, sets up the role reactions message, and completes the roleInfo data structure
# also sets the presence of the bot
async def bootSequence():
  global globalRoleMsg
  global roleInfo
  global guildID
  print('We have logged in as {0.user}'.format(client))
  game = discord.Game("with GLaDOS")
  await client.change_presence(status=discord.Status.online, activity=game)
  #we have restarted the bot so we want to reset the reaction roles message
  AIAAGuild = client.get_guild(guildID)
  #newPersonRole = AIAAGuild.get_role(841828431956279296)
  for x in range (len(roleInfo)):
    roleInfo[x]['roleAccess'] = AIAAGuild.get_role(roleInfo[x]['ID'])

  # make code more general instead of channel id
  rolesChannel = AIAAGuild.get_channel(836398238579032084)
  await rolesChannel.purge()
  globalRoleMsg = await rolesChannel.send("**__Welcome to the AIAA Server__** \n"
  + "To get roles add the reaction below with the corresponding AIAA branch you would want to join. \n"
  + "You can pick, one, all or undecided if you just wanna take a look around the server! \n"
  +"If you need a role removed DM one of the board members. \n \n"
  + "**__AIAA Roles__**\n"
  + ":airplane: Design Build Fly (DBF)\n"
  +":rocket: Rocketry \n"
  +":dash: Quadcopters \n"
  +":question: Undecided \n\n"
  +"**__Major__**\n"
  +":gear: Mechancial Engineering \n"
  +":keyboard: Computer Science \n"
  +":bulb: Electrical Engineering \n"
  +":alembic: Chemcial Engineering \n"
  +":astronaut: Other \n \n"
  +"**__Offtopic Roles__**\n"
  +":books: School\n"
  +":video_game: Gaming")

  for x in range(1,len(roleInfo)):
    await globalRoleMsg.add_reaction(emoji=roleInfo[x]['emoji'])

#
# userAddRoles(reaction, user)
#
# Helper function that removes the "New Member" role if the user still has it, and pulls  the corresponing from
# the dictionary that the user selected to get
async def userAddRoles(reaction, user):
  global roleInfo
  if(user!=client.user):
    if((next((item for item in roleInfo if item['emoji'] == reaction.emoji), None))!=None):
      if roleInfo[0]['roleAccess'] in user.roles:
        await user.remove_roles(roleInfo[0]['roleAccess'])
          
      pos = next(i for i, item in enumerate(roleInfo) if item['emoji'] == reaction.emoji)
      await user.add_roles(roleInfo[pos]['roleAccess'])

async def remindMessageParse(messageIn):
  colFind = messageIn.find(",")
  messageIn = messageIn[colFind+1:]
  colFind = messageIn.find(",")
  messageIn = messageIn[colFind+1:]
  return messageIn


#
# job(message)
#
# Helper function that is called for the remind me command, still in BETA
async def job(message):
  usersToAt = ""
  usersToRemind = message.mentions
  for x in range(len(usersToRemind)):
    usersToAt = usersToAt + " " + usersToRemind[x].mention
  remindMessage = await remindMessageParse(message.content)
  await message.channel.send("Reminder for "+ usersToAt+":"+remindMessage)

#
# pollCommand(message)
#
# creates a poll with up to 10 options, uses pollCommandProcess to parse out/ get the sting info set up properly
async def pollCommand(message):
  cutMsg = message.content[6:]
  pollReturn = pollCommandProcess(cutMsg)
  botPollMsg = await message.channel.send(pollReturn[1])
  if(pollReturn[0]):
    reactionsToAdd = pollReturn[2]
    for x in range(len(reactionsToAdd)):
      await botPollMsg.add_reaction(emoji=reactionsToAdd[x])
    await message.delete()

#
# pollCommandProcess(msg)
#
# takes in a comma seperated string and pulls out the info, returns a how to use of the format is not correct
def pollCommandProcess(msg):
  reactions = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]
  reactionsText = [":one:",":two:",":three:",":four:",":five:",":six:",":seven:",":eight:",":nine:"]

  # set up default returns
  validMsg = False
  messageToSend = ("!poll command syntax: \n" 
    +"!poll POLL TITLE, OPTION 1, OPTION 2, OPTION 3, ... , OPTION 9 \n"
    + "Currently the !poll command only supports 9 options. And you need atleast 1 option to be a valid poll.")
  reactionsToAdd = []
  pollArray = []
  if(msg.find(",")!=-1):
    pollArray.append(msg[0:msg.find(",")])
    msg = msg[msg.find(",")+1:]
  else:
    return [validMsg,messageToSend,reactions]

  if(msg.find(",")==-1):
    messageToSend = "__**"+pollArray[0]+"**__"+"\n"+reactionsText[0]+msg


  validMsg = True
  while(msg.find(",")!=-1):
    pollArray.append(msg[0:msg.find(",")])
    msg = msg[msg.find(",")+1:]
  pollArray.append(msg)

  #special formatting for poll title
  messageToSend = "__**"+pollArray[0]+"**__"
  pollArray.pop(0)

  for x in range(len(pollArray)):
    messageToSend = messageToSend + "\n" + reactionsText[x] + " " + pollArray[x]
    reactionsToAdd.append(reactions[x])
  return [validMsg,messageToSend,reactionsToAdd]

#
# newMember(member)
#
# helper function that DM's the new user and gives them the "New Member Role"
async def newMember(member):
  global newMemberRoleID
  #role = member.guild.get_role(newMemberRoleID)
  #await user.add_roles(roleInfo[pos]['roleAccess'])
  await member.add_roles(roleInfo[0]['roleAccess'])
  await member.send('This is an automated message. Do not respond to this. \n \n'
      +'__**Welcome to the UIC AIAA Discord server!**__ \n '
      + 'To get started please introduce yourself in #introductions and change your nickname to your real name. Next react to the message found in #roles in order to gain further access to the server, and team specific channels. If you would like to contact a specific team manager for more info they are listed below.\n \n' 
      + '**AIAA President:** Philip Korus pkorus3@uic.edu \n'
      + '**:rocket:Rocket Project Manager:** Cade Vacaroni, whjads \n'
      + '**:airplane:DBF Project Manager:** Stevenson Durning, osaijdoj \n' 
      + '**:dash:Drone Project Manager:** Alex Rodriguez')

client.run(os.environ['TOKEN']);
