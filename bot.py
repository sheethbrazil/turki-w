import os
import discord
from discord.ext import commands
from discord.utils import utcnow

# ========= الإعدادات =========
WELCOME_CHANNEL_ID = 1429240464720134288  # حط ايدي روم الترحيب
BOT_PREFIX = "!"
# =============================

intents = discord.Intents.default()
intents.members = True  # لازم تفعّل Server Members Intent من Developer Portal

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online | Logged in as {bot.user}")

@bot.event
async def on_member_join(member: discord.Member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel is None:
        return

    created_at = member.created_at
    now = utcnow()

    account_age_days = (now - created_at).days
    account_age_years = account_age_days // 365

    embed = discord.Embed(
        description=f"👋 **{member.mention} joined the server!**",
        color=0xFFC513,  # اللون: #ffc513
        timestamp=now
    )

    embed.set_author(
        name=str(member),
        icon_url=member.display_avatar.url
    )

    embed.set_thumbnail(url=member.display_avatar.url)

    embed.add_field(
        name="📅 Account Created",
        value=f"{created_at.strftime('%d/%m/%Y %H:%M UTC')}",
        inline=False
    )

    embed.add_field(
        name="⏳ Account Age",
        value=f"**{account_age_years} years** ({account_age_days} days)",
        inline=False
    )

    embed.set_footer(text=f"User ID: {member.id}")

    await channel.send(embed=embed)

# ===== تشغيل البوت =====
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is not set! Add it in Railway Variables.")
bot.run(TOKEN)
