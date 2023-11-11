import nextcord
from nextcord.ext import commands
import yt_dlp

TOKEN = 'YOUR_DISCORD_BOT_TOKEN'

intents = nextcord.Intents.all()
intents.voice_states = True
bot = commands.Bot(command_prefix='!', intents=intents)

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'verbose': True,  # Добавленный параметр для получения подробного вывода
}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='play')
async def play(ctx, query):
    channel = ctx.author.voice.channel
    voice_channel = await channel.connect()

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        url = info['formats'][0]['url']
        print(f'Playing track: {url}')  # Добавленный вывод для отслеживания URL

    voice_channel.play(nextcord.FFmpegPCMAudio(url, executable="ffmpeg"))

@bot.command(name='disconnect')
async def disconnect(ctx):
    await ctx.voice_client.disconnect()

bot.run(TOKEN)
