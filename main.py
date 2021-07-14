import discord
import time 
import threading
import os
from discord_slash import SlashCommand

intents=intents=discord.Intents.all()
client = discord.Client(intents=intents)
slash = SlashCommand(client, sync_commands=True)

globalRoleMsg = None

# have to update the blow items with server speicif ID's / variables / emojis
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
    'name': 'Quadcopter',
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

@slash.slash(name="test", description="This is just a test command, nothing more.")

@client.event
async def on_ready():
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

@client.event
async def on_reaction_add(reaction, user):
  global roleInfo

  if(globalRoleMsg!=None):
    if(reaction.message.id == globalRoleMsg.id):
      if(user!=client.user):
        if((next((item for item in roleInfo if item['emoji'] == reaction.emoji), None))!=None):
          if roleInfo[0]['roleAccess'] in user.roles:
            await user.remove_roles(roleInfo[0]['roleAccess'])
          
          pos = next(i for i, item in enumerate(roleInfo) if item['emoji'] == reaction.emoji)
          await user.add_roles(roleInfo[pos]['roleAccess'])

  # gold star feature only works on messages sent while the bot was on
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


        


@client.event
async def on_message(message):

    if message.author == client.user:
        return
    else:
      if(message.content.startswith('//poll')):
        cutMsg = message.content[7:]
        pollReturn = pollCommandProcess(cutMsg)
        botPollMsg = await message.channel.send(pollReturn[1])
        if(pollReturn[0]):
          reactionsToAdd = pollReturn[2]
          for x in range(len(reactionsToAdd)):
            await botPollMsg.add_reaction(emoji=reactionsToAdd[x])
          await message.delete()
      elif(message.content.startswith('//remind')):
        timeActive = "19:33:24"
        timeActiveHrs = int(timeActive[0:2])
        timeActiveMin = int(timeActive[3:5])
        timeActiveSec = int(timeActive[6:8])

        timeRemind = "19:34:24"
        timeRemindHrs = int(timeRemind[0:2])
        timeRemindMin = int(timeRemind[3:5])
        timeRemindSec = int(timeRemind[6:8])

        timeWait = (timeRemindHrs-timeActiveHrs)*3600 + (timeRemindMin-timeActiveMin)*60 + (timeRemindSec-timeActiveSec) 
        #await reminderFunc(message,timeWait)
        thread = threading.Thread(target = await reminderFunc, args = (message,timeWait,))
        thread.start()
        #remindMessageData = message.content[9:]
        #tempAt = ""
        #print(remindMessageData)
        #for guild in client.guilds:
        #  for member in guild.members:
            # check for @ roles too
            # when you @ someone it gives you their ID's no need to actually do this for loop search
            # the thing below actually works sorta
        #    if((member.name==remindMessageData)|(member.nick==remindMessageData)):
        #      tempAt = member.mention
        #await message.channel.send("Reminder for:"+message.author.mention+ tempAt
        #  + "about: ")
      elif(message.content.startswith("rocketz")):
        await message.channel.send("GO BRRRRRRRR")
      #  rocketryID = 836398929402527764
      #  role = message.guild.get_role(rocketryID)
      #  await message.author.add_roles(role)
      
async def reminderFunc(message, timeWait):
      await message.channel.send("Waiting start")
      time.sleep(timeWait)   
      await message.channel.send("Done waiting")

def pollCommandProcess(msg):
  reactions = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]
  reactionsText = [":one:",":two:",":three:",":four:",":five:",":six:",":seven:",":eight:",":nine:"]

  # set up default returns
  validMsg = False
  messageToSend = ("//poll command syntax: \n" 
    +"//poll POLL TITLE, OPTION 1, OPTION 2, OPTION 3, ... , OPTION 9 \n"
    + "Currently the //poll command only supports 9 options. And you need atleast 1 option to be a valid poll.")
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


@client.event
async def on_member_join(member):
  newMemberID = 841828431956279296
  role = member.guild.get_role(newMemberID)
  await member.add_roles(role)
  await member.send('This is an automated message. Do not respond to this. \n \n'
      +'__**Welcome to the UIC AIAA Discord server!**__ \n '
      + 'To get started please introduce yourself in #introductions and change your nickname to your real name. Next react to the message found in #roles in order to gain further access to the server, and team specific channels. If you would like to contact a specific team manager for more info they are listed below.\n \n' 
      + '**AIAA President:** Philip Korus pkorus3@uic.edu \n'
      + '**:rocket:Rocket Project Manager:** Cade Vacaroni, whjads \n'
      + '**:airplane:DBF Project Manager:** Stevenson Durning, osaijdoj \n' 
      + '**:dash:Drone Project Manager:** Alex Rodriguez')


client.run(os.environ['TOKEN']);
