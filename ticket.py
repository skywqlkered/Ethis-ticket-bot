from dotenv import load_dotenv
import discord
import os
import asyncio

load_dotenv()
TOKEN = os.getenv('ETHIS_BOT_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))




welcome_message = """
Then a <@&1261617495954034698> member will process your ticket shortly!

```
**What do you enjoy doing in Minecraft?**
- Answer

**What has been your experience playing on Minecraft servers or SMPs?**
- Answer

**Tell us more about yourself! Share your hobbies, a fun fact, or anything else you’d like us to know!**
- Answer


``` 


"""



def setup_embed() -> discord.Embed:
    """returns the embed format for ticket

    Returns:
        discord.Embed: Embed with question fields
    """
    embed: discord.Embed = discord.Embed(color=discord.Color.from_rgb(216, 107, 44))
    embed.add_field(name='Please answer the questions below:', value=welcome_message, inline=True)
    return embed

async def get_first_message_author(ticket_channel: discord.TextChannel) -> discord.User | discord.Member | str :
    try:
        first_message_list: list[discord.Message] = await ticket_channel.history(limit=1, oldest_first=True).flatten()
        first_message: discord.Message = first_message_list[0]
        member = first_message.mentions[0]
        return member
    except Exception as errorman:
        return str(errorman)

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if message.content.startswith('/send form') and 1261617495954034698 in [role.id for role in message.author.roles]:
        try:
            await message.channel.send(embed=setup_embed())
            await message.delete()
        except Exception as errorman:
            await message.guild.get_channel(1419741195424366612).send(str(errorman))



    
    if channel.category.id == 1226215408126791832 and channel.name.startswith('ticket'):
        try:
                async def answer_message_check(channel):
                    return message.author == await get_first_message_author(channel)
                
                message_by_applicant = await answer_message_check(message)
                
                await client.wait_for("message", check=answer_message_check)
                
                
            except Exception as errorman:
                await channel.guild.get_channel(1419741195424366612).send(str(errorman))



@client.event
async def on_guild_channel_create(channel: discord.abc.GuildChannel):
    if channel.category is None:
        return
    if channel.category.id == 1226215408126791832 and channel.name.startswith('ticket'):
        try:
            def check(message):
                return message.channel == channel

            await client.wait_for('message', check=check)
            await channel.send(embed=setup_embed())
        except Exception as errorman:
            await channel.guild.get_channel(1419741195424366612).send(str(errorman))
            
        

@client.event
async def on_guild_channel_update(before, after: discord.TextChannel):
    if isinstance(after, discord.TextChannel):
        if after.name.startswith('closed'):
            return_value = await get_first_message_author(after)
            if isinstance(return_value, str):
                await after.guild.get_channel(1419741195424366612).send(return_value)
            if isinstance(return_value, discord.User) or isinstance(return_value, discord.Member):
                member_name = return_value
                await after.edit(name=(member_name.name + "-" + after.name.split("-")[-1]))


client.run(TOKEN)
