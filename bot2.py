import discord
from discord.ext import commands
import mysql.connector

intents = discord.Intents.default()
intents.all()
intents.message_content = True

# MySQL configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234567890',
    'database': 'maha',
}

# Create a MySQL connection
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Create a table to store Discord server tokens
create_table_query = '''
CREATE TABLE IF NOT EXISTS discord_servers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    server_id VARCHAR(255) NOT NULL,
    auth_token VARCHAR(255) NOT NULL
);
'''
cursor.execute(create_table_query)
conn.commit()

# Discord bot token
TOKEN = 'MTE4NDM2MzY2MTE4ODQxMTQ1NA.GItqX5.5hk5sv_Rhs9n2NDXX8148jYK-Up_eCob7L4GYs'

# Create a bot instance with a command prefix
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.command(name='hello')
async def hello(ctx):
    # Check if the command is invoked in a guild (server)
    if ctx.guild is not None:
        server_id = str(ctx.guild.id)
        print(f"Received command from server ID: {server_id}")

        # Retrieve the auth token from the database
        get_auth_token_query = '''
        SELECT auth_token FROM discord_servers WHERE server_id = %s;
        '''
        cursor.execute(get_auth_token_query, (server_id,))
        result = cursor.fetchone()

        # Ensure the result set is consumed
        cursor.fetchall()

        if result:
            auth_token = result[0]

            # Check if the user has the correct role or permission
            # This is just a placeholder, customize based on your needs
            if '@everyone' in [role.name for role in ctx.author.roles]:
                # Print the "Hello World" message
                print(f"Hello World from {ctx.guild.name}")

                # Send a message to the Discord channel
                await ctx.send(f"Hello World from {ctx.guild.name}!")
            else:
                await ctx.send("You don't have the required role or permission.")
        else:
            await ctx.send("This server is not authenticated.")
    else:
        # Handle the case when the command is invoked outside a server
        await ctx.send("This command can only be used in a server.")

@bot.command(name='authenticate')
async def authenticate(ctx):
    # Check if the command is invoked in a guild (server)
    if ctx.guild is not None:
        server_id = str(ctx.guild.id)
        print(f"Authenticating server ID: {server_id}")

        # Check if the server is already authenticated
        check_auth_query = '''
        SELECT COUNT(*) FROM discord_servers WHERE server_id = %s;
        '''
        cursor.execute(check_auth_query, (server_id,))
        result = cursor.fetchone()

        if result and result[0] > 0:
            await ctx.send("This server is already authenticated.")
        else:
            # Insert the server_id and a placeholder auth_token (replace with your logic)
            insert_query = "INSERT INTO discord_servers (server_id, auth_token) VALUES (%s, 'your_auth_token');"
            cursor.execute(insert_query, (server_id,))
            conn.commit()

            await ctx.send("Server authenticated successfully.")
    else:
        # Handle the case when the command is invoked outside a server
        await ctx.send("This command can only be used in a server.")

if __name__ == '__main__':
    bot.run(TOKEN)
