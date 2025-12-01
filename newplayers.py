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
    # print(non_member_message.mentions)
    # members = [member for member in non_member_message.guild.members if len(member.roles) == 1]

async def get_message() -> discord.Message:
    """
    Returns the discord message with non-members
    Returns:
        non_member_message: discord.Message
    """
    return await (discord.utils.get(discord.utils.get(client.guilds, id=925805443887022121).channels,
                                                  id=1424407719976108162)).fetch_message(1424410900848312340)

def parse_message(message: discord.Message) -> list[str]:
    """
    Args:
        message: discord.Message

    Returns:
        mentions of members: list[str]
    """
    return [user.mention for user in message.mentions]

def format_names(names:list[str]) -> str:
    """
    Args:
        names: list[str]

    Returns:
        formated string: str
    """
    return ', '.join(names)

async def add_member_to_message(member: discord.Member):
    """
    Adds a member to the message

    Args:
        member: discord.Member

    Returns:
        None
    """
    non_members_messsage = await get_message()
    names = parse_message(non_members_messsage)
    if member.mention not in names:
        names.append(member.mention)
        await non_members_messsage.edit(content=format_names(names))


async def remove_member_from_message(member: discord.Member):
    """
    Removes a member from the message
    Args:
        member: discord.Member

    Returns:
        None
    """
    non_members_messsage = await get_message()
    names = parse_message(non_members_messsage)
    if member.mention in names:
        names.remove(member.mention)
        await non_members_messsage.edit(content=format_names(names))

def has_member(member: discord.Member) -> bool:
    """
    Checks whether member has member role
    Args:
        member: discord.Member

    Returns:
        true if member has member role: bool
        false otherwise: bool
    """
    if 925808103436455936 in [role.id for role in member.roles]: # member role id = 925808103436455936
        return True
    else:
        return False


async def in_names(member: discord.Member) -> bool:
    """
    Checks whether member mention is in the message in the channel
    Args:
        member: discord.Member

    Returns:
        True if in message: bool
        False otherwise: bool

    """
    non_members_messsage = await get_message()
    names = parse_message(non_members_messsage)
    if member.mention in names:
        return True
    else:
        return False

@client.event
async def on_member_join(Member: discord.Member):
    await add_member_to_message(Member)

@client.event
async def on_raw_member_remove(Payload):
    await remove_member_from_message(Payload.user)


@client.event
async def on_member_update(before: discord.Member, after: discord.Member):
    if not has_member(after) and not await in_names(after):
        await add_member_to_message(after)
    if has_member(after) and await in_names(after):
        await remove_member_from_message(after)


client.run(TOKEN)