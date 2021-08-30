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

# have to update the blow items with server speific ID's / variables / emojis
roleInfo = [
  {
    'name': 'Member',
    'emoji': "👶",
    'ID':749437004235800606,
    'roleAccess':None
  },
  {
    'name': 'DBF',
    'emoji': "✈️",
    'ID':881358377127673886,
    'roleAccess':None
  },
  {
    'name': 'Rocketry',
    'emoji': "🚀",
    'ID':749448204776374294,
    'roleAccess':None
  },
  {
    'name': 'Drone',
    'emoji': "💨",
    'ID':881358421801185280,
    'roleAccess':None
  },
  {
    'name': 'Undecided',
    'emoji': "❓",
    'ID':881690756933353522,
    'roleAccess':None
  },
  {
    'name': 'Mechanical Engineer',
    'emoji': "⚙️",
    'ID':881690345597988914,
    'roleAccess':None
  },
  {
    'name': 'Computer Science',
    'emoji': "⌨️",
    'ID':881691595198578748,
    'roleAccess':None
  },
  {
    'name': 'Electrical Engineer',
    'emoji': "⚡",
    'ID':881690433879683132,
    'roleAccess':None
  },
  {
    'name': 'Chemical Engineer',
    'emoji': "⚗️",
    'ID':881690481363386428,
    'roleAccess':None
  },
  {
    'name': 'Aerospace Enthusiast',
    'emoji': "👩‍🚀",
    'ID':881690629086793738,
    'roleAccess':None
  }
]
guildID = 701934476095389747

#@slash.slash(name="test", description="This is just a test command, nothing more.")

# events that occur when the bot first starts up
@client.event
async def on_ready():
  await bootSequence()

# message based events
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif isinstance(message.channel, discord.DMChannel):
      await botRecieveDM(message)
      
# reaction based events
@client.event
async def on_reaction_add(reaction, user):
  global golbalRoleMsg

  if(globalRoleMsg!=None):
    if(reaction.message.id == globalRoleMsg.id):
      await userAddRoles(reaction, user)

# events based on when a new person joins the server
@client.event
async def on_member_join(member):
  await newMember(member)

#
# botRecieveDM(message)
#
# helper function handler for if a user dm's the bot, gets forwarded to who ever the Bot Overlord is, be sure
# to replace the user ID as needed
async def botRecieveDM(message):
  temp = client.get_user(botOverLordID)
  await temp.send("__**DM from: "+message.author.name + "#" + message.author.discriminator+"**__\n"+message.content)

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
  rolesChannel = AIAAGuild.get_channel(881674846436749323)
  await rolesChannel.purge()
  globalRoleMsg = await rolesChannel.send("**__Welcome to the AIAA Server__** \n"
  + "To get roles add the reaction below with the corresponding AIAA branch you would want to join. \n"
  + "You can pick, one, all or undecided if you just wanna take a look around the server! \n"
  +"If you need a role removed DM one of the board members. \n \n"
  + "**__AIAA Roles__**\n"
  + ":airplane: Design Build Fly (DBF)\n"
  +":rocket: Rocketry \n"
  +":dash: Drone \n"
  +":question: Undecided \n\n"
  +"**__Major__**\n"
  +":gear: Mechancial Engineering \n"
  +":keyboard: Computer Science \n"
  +":zap: Electrical Engineering \n"
  +":alembic: Chemcial Engineering \n"
  +":astronaut: Other")

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
    + '**:airplane:DBF Project Manager:** Stevenson Durning, sdurni2@uic.edu \n' 
    + '**:dash:Drone Project Manager:** Alex Rodriguez \n'
    + '**:rocket:Rocket Project Manager:** Cade Vallero, cvalle9@uic.edu')

client.run(os.environ['TOKEN']);
