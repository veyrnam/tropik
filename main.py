import discord
from discord.ext import commands
import os
import webserver
import random
import datetime
import requests
import json
import re
from collections import defaultdict

# ===== TOKEN =====
DICORD_TOKEN = os.environ['discordkey']
OWNER_ID = 1160070826276683918
webserver.keep_alive()

# ===== BOT SETUP =====
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="t/", intents=intents, help_command=None)
AFK_USERS = {}

# ===== COOLDOWN SETTINGS =====
COMMAND_TRACKER = defaultdict(list)
COOLDOWN_SECONDS = 15
MAX_COMMANDS = 3


def is_on_cooldown(user_id):
    now = datetime.datetime.utcnow()
    COMMAND_TRACKER[user_id] = [
        t for t in COMMAND_TRACKER[user_id] if (now - t).total_seconds() < COOLDOWN_SECONDS
    ]
    if len(COMMAND_TRACKER[user_id]) >= MAX_COMMANDS:
        first_time = COMMAND_TRACKER[user_id][0]
        remaining = COOLDOWN_SECONDS - (now - first_time).total_seconds()
        return True, max(1, int(remaining))
    return False, 0


SETTINGS_FILE = "settings.json"

# ===== HELPER FUNCTIONS =====
def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {"welcome": {}, "bye": {}}
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)


def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)


SETTINGS = load_settings()


def user_tag(member: discord.Member):
    return f"@{member.name} ({member.display_name})"


# ===== ON READY =====
@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Tasking Tropikal! 🌴"
        )
    )
    print(f"✅ Logged in as {bot.user}")


# ===== COOLDOWN CHECK (applies to all public commands) =====
@bot.check
async def global_cooldown(ctx):
    if ctx.author.id == OWNER_ID:
        return True  # Owner is excluded

    on_cooldown, remaining = is_on_cooldown(ctx.author.id)
    if on_cooldown:
        await ctx.reply(f"❌ Wait! You’re on command cooldown. Please wait for `{remaining}` seconds.")
        return False

    COMMAND_TRACKER[ctx.author.id].append(datetime.datetime.utcnow())
    return True


# ===== PUBLIC COMMANDS =====
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="🌴 Tropikal Bot Commands",
        description="Here’s a list of commands you can use!",
        color=discord.Color.green()
    )
    embed.add_field(
        name="Everyone Commands",
        value="`t/help`, `t/pfp`, `t/banner`, `t/info`, `t/serverinfo`, `t/howgay`, `t/afk`, `t/pet`, `t/labubu`, `t/nailong`, `t/ascii`",
        inline=False
    )
    embed.add_field(
        name="Setup Commands (Owner Only)",
        value="`t/welcome`, `t/bye`, `t/verify`, `t/embed`",
        inline=False
    )
    embed.set_footer(text="Made by @Vyrnam for the Tropikal server 💚")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)


@bot.command()
async def pfp(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"This is {user_tag(member)}", color=discord.Color.blue())
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)


@bot.command()
async def banner(ctx, member: discord.Member = None):
    member = member or ctx.author
    user = await bot.fetch_user(member.id)
    if user.banner:
        embed = discord.Embed(title=f"{user_tag(member)}", color=discord.Color.blurple())
        embed.set_image(url=user.banner.url)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"{user_tag(member)} has no banner 😢")


@bot.command()
async def info(ctx, member: discord.Member = None):
    member = member or ctx.author
    roles = [r.mention for r in member.roles if r.name != "@everyone"]
    embed = discord.Embed(title=f"👤 Info for {user_tag(member)}", color=discord.Color.orange())
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="Username", value=member.name, inline=True)
    embed.add_field(name="Nickname", value=member.display_name, inline=True)
    embed.add_field(name="Joined Discord", value=member.created_at.strftime("%B %d, %Y"), inline=False)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%B %d, %Y"), inline=False)
    embed.add_field(name="Roles", value=", ".join(roles) or "None", inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(
        title=f"🏝️ {guild.name}",
        description=f"Information about **{guild.name}**",
        color=discord.Color.gold()
    )
    embed.add_field(
        name="Owner", value=f"@{guild.owner.name} ({guild.owner.display_name})" if guild.owner else "Unknown", inline=True
    )
    embed.add_field(name="Members", value=len(guild.members), inline=True)
    embed.add_field(name="Boosts", value=guild.premium_subscription_count, inline=True)
    embed.add_field(name="Created On", value=guild.created_at.strftime("%B %d, %Y"), inline=False)
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    await ctx.send(embed=embed)


@bot.command()
async def howgay(ctx, member: discord.Member = None):
    member = member or ctx.author
    percent = random.randint(1, 100)
    await ctx.send(f"🏳️‍🌈 {user_tag(member)} is **{percent}%** gay!")


@bot.command()
async def ascii(ctx):
    art = """
⠀⠀⠀⠀⠀⠀⠀⣠⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣰⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⠋⠁⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⡆⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢠⠁⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠤⠀⠒⣶⣶⡶⠂⠀
⠀⠀⠀⠀⢸⢀⠠⠔⠒⠒⠒⠒⠂⠤⣀⠤⠒⠉⠀⠀⠀⢀⡠⠟⠉⠀⠀⠀
⠀⠀⠀⠀⡸⠁⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⣀⠠⠐⠊⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⢃⣖⢢⠀⠀⠀⠀⠀⣠⢤⣄⠀⠈⡄⠀⠀⣀⠠⠄⠀⠒⠒⠀⠇
⠀⠀⠀⡜⠈⠛⠛⠀⣐⠂⠀⠀⠻⠿⠏⠀⠀⡗⠊⠁⠀⠀⠀⠀⠀⠀⡜⠀
⠀⠀⢰⠉⢱⠀⠱⠞⠁⠉⠒⡖⠀⢀⠔⠢⡄⡇⠀⠀⠀⠀⠀⠀⠀⡐⠀⠀
⠀⠀⠀⢶⠊⠀⠀⢣⠀⠀⢠⠃⠀⠘⢄⣀⢾⠃⠀⡤⠤⠤⠤⠤⠔⠀⠀⠀
⠀⠀⠀⠀⢱⢄⠀⠀⠢⠔⠃⠀⠀⠀⠀⢀⢎⢢⠀⠰⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣌⠀⠁⠂⠀⠀⠀⠀⠀⠐⠈⠁⢸⡤⠓⢀⡇⠀⠀⠀⠀⠀⠀⠀
⣄⡀⠀⣰⢸⠀⠀⠀⠀⢀⢀⠂⠀⠀⠀⠀⠄⢳⡈⢁⡀⠀⠀⠀⠀⠀⠀⠀
⢿⣷⠁⠀⠈⡄⠀⠀⠀⠈⡞⠀⠀⠀⠀⡰⠉⠀⢈⠻⠿⠀⠀⠀⠀⠀⠀⠀
⡇⠈⡆⠀⠀⠱⡀⠀⠀⠀⡇⠀⠀⠀⢠⠁⠀⠀⠈⢀⠇⠀⠀⠀⠀⠀⠀⠀
⠘⡄⢀⠀⠀⠀⠱⡀⠀⠀⠁⠀⠀⡠⠁⠀⠀⢰⠀⡜⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠈⠉⠉⠉⠀⠐⠛⠶⠒⠣⠦⠤⠗⠒⠒⠒⠚⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""
    await ctx.send(f"```\n{art}\n```")


@bot.command()
async def afk(ctx):
    user = ctx.author
    AFK_USERS[user.id] = datetime.datetime.utcnow()
    embed = discord.Embed(
        title="💤 AFK Notice",
        description=f"{user.mention} is now marked as AFK.",
        color=discord.Color.light_gray()
    )
    await ctx.send(embed=embed)


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("t/afk"):
        return await bot.process_commands(message)

    # remove AFK if user talks
    if message.author.id in AFK_USERS:
        del AFK_USERS[message.author.id]
        await message.channel.send(f"👋 Welcome back, {message.author.mention}! You’re no longer AFK.")
        return await bot.process_commands(message)

    # notify when pinging AFK users
    mentioned_users = {user.id for user in message.mentions}
    for user_id in list(AFK_USERS.keys()):
        if user_id in mentioned_users:
            elapsed = datetime.datetime.utcnow() - AFK_USERS[user_id]
            elapsed_str = str(elapsed).split(".")[0]
            user = await bot.fetch_user(user_id)
            await message.reply(f"💤 {user.mention} is currently AFK — AFK for `{elapsed_str}`.")
            break

    await bot.process_commands(message)


@bot.command()
async def pet(ctx):
    try:
        res = requests.get("https://g.tenor.com/v1/search?q=cute%20pet&key=LIVDSRZULELA&limit=25")
        data = res.json()
        gif = random.choice(data["results"])["media"][0]["gif"]["url"]
        await ctx.send(gif)
    except Exception:
        await ctx.send("😿 Couldn’t fetch pet gifs right now.")


@bot.command()
async def labubu(ctx):
    try:
        res = requests.get("https://g.tenor.com/v1/search?q=labubu&key=LIVDSRZULELA&limit=25")
        data = res.json()
        gif = random.choice(data["results"])["media"][0]["gif"]["url"]
        await ctx.send(gif)
    except Exception:
        await ctx.send("Couldn’t fetch Labubu gifs right now.")


@bot.command()
async def nailong(ctx):
    try:
        res = requests.get("https://g.tenor.com/v1/search?q=nailong&key=LIVDSRZULELA&limit=25")
        data = res.json()
        gif = random.choice(data["results"])["media"][0]["gif"]["url"]
        await ctx.send(gif)
    except Exception:
        await ctx.send("Couldn’t fetch nailong gifs right now.")

# ===== BYE SETUP =====
@bot.command()
@owner_only()
async def bye(ctx, channel_id: int = None, image_url=None, *, rest=None):
    if not channel_id or not image_url or not rest or "|" not in rest:
        return await ctx.send("📤 Usage: `t/bye <channel_id> <image_url> <title> | <description>`")

    title, description = [x.strip() for x in rest.split("|", 1)]

    SETTINGS.setdefault("bye", {})
    SETTINGS["bye"][str(ctx.guild.id)] = {
        "channel": str(channel_id),
        "image": image_url,
        "title": title,
        "description": description
    }
    save_settings(SETTINGS)
    await ctx.send(f"✅ Goodbye message has been set for <#{channel_id}>!")


# ===== VERIFY EMBED =====
@bot.command()
@commands.is_owner()
async def verify(ctx, *, args=None):
    if not args:
        return await ctx.send(
            "✅ Usage: `t/verify author=<text> title=<text> desc=<text> color=<hex> image=<url> footer=<text> roleid=<id>`"
        )

    import re
    pattern = r'(\w+)=(".*?"|\'.*?\'|[^\s]+)'
    matches = re.findall(pattern, args)
    params = {k.lower(): v.strip('"\'') for k, v in matches}

    author = params.get("author")
    title = params.get("title")
    desc = params.get("desc")
    color = params.get("color", "#2b2d31")
    footer = params.get("footer")
    image = params.get("image")
    role_id = params.get("roleid")

    if not role_id:
        return await ctx.send("⚠️ Missing `roleid=<id>` parameter.")

    try:
        color_value = int(color.replace("#", ""), 16)
    except ValueError:
        color_value = 0x2b2d31

    embed = discord.Embed(
        title=title or discord.Embed.Empty,
        description=desc or discord.Embed.Empty,
        color=color_value
    )
    if author:
        embed.set_author(name=author)
    if footer:
        embed.set_footer(text=footer)
    if image:
        embed.set_image(url=image)

    msg = await ctx.send(embed=embed)
    await msg.add_reaction("✅")

    def check(reaction, user):
        return (
            reaction.message.id == msg.id
            and str(reaction.emoji) == "✅"
            and not user.bot
        )

    remove_role_id = 1394923393748434944

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", check=check)
            guild = ctx.guild
            role_to_add = guild.get_role(int(role_id))
            role_to_remove = guild.get_role(remove_role_id)

            if role_to_add:
                await user.add_roles(role_to_add, reason="Verified via ✅ reaction")
            if role_to_remove:
                await user.remove_roles(role_to_remove, reason="Removed unverified role")

            await msg.remove_reaction("✅", user)
        except Exception as e:
            print(f"[verify cmd] Error: {e}")
            break

@bot.command()
@owner_only()
async def embed(ctx, *, args=None):
    """
    Create a custom embed using pseudo-HTML tags.
    Example:
    t/embed <head>Hello</head> <body>This is a test embed.</body> <color>#ff0000</color> <footer>Footer text</footer>
    """
    if not args:
        return await ctx.send(
            "✅ Usage: `t/embed <head>Title</head> <body>Description</body> <color>#hex</color> <image>url</image> <footer>text</footer> <author>text</author> <thumbnail>url</thumbnail>`"
        )

    # Extract tags like <tag>value</tag>
    pattern = r"<(\w+)>(.*?)</\1>"
    matches = re.findall(pattern, args, re.DOTALL)

    # Store in dict
    params = {k.lower(): v.strip() for k, v in matches}

    title = params.get("head")
    desc = params.get("body")
    color = params.get("color", "#2b2d31")
    image = params.get("image")
    footer = params.get("footer")
    author = params.get("author")
    thumbnail = params.get("thumbnail")

    # Handle color
    try:
        color_value = int(color.replace("#", ""), 16)
    except ValueError:
        color_value = 0x2b2d31

    # Create embed
    embed = discord.Embed(
        title=title or discord.Embed.Empty,
        description=desc or discord.Embed.Empty,
        color=color_value
    )

    if author:
        embed.set_author(name=author)
    if footer:
        embed.set_footer(text=footer)
    if image:
        embed.set_image(url=image)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)

    await ctx.send(embed=embed)

# ===== WELCOME & BYE EVENTS =====


@bot.event
async def on_member_join(member):
    guild_id = str(member.guild.id)
    if guild_id in SETTINGS.get("welcome", {}):
        data = SETTINGS["welcome"][guild_id]
        channel = bot.get_channel(int(data["channel"]))
        if not channel:
            return

        embed = discord.Embed(
            title=data["title"],
            description=data["description"].replace("{user}", member.mention),
            color=discord.Color.green()
        )
        if data["image"]:
            embed.set_image(url=data["image"])
        embed.set_footer(text=f"Welcome to {member.guild.name}! 🌴")
        await channel.send(embed=embed)


@bot.event
async def on_member_remove(member):
    guild_id = str(member.guild.id)
    if guild_id in SETTINGS.get("bye", {}):
        data = SETTINGS["bye"][guild_id]
        channel = bot.get_channel(int(data["channel"]))
        if not channel:
            return

        embed = discord.Embed(
            title=data["title"],
            description=data["description"].replace("{user}", member.name),
            color=discord.Color.red()
        )
        if data["image"]:
            embed.set_image(url=data["image"])
        embed.set_footer(text="We hope to see you again 💔")
        await channel.send(embed=embed)

# ===== RUN =====
bot.run(DICORD_TOKEN)





