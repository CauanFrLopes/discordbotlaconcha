import discord
from discord.ext import commands
from keep_alive import keep_alive
import yt_dlp
import asyncio
import os

# Configuração de Intents (necessário para ler mensagens)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Configurações do yt-dlp e FFmpeg
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

@bot.event
async def on_ready():
    print(f'Bot logado como {bot.user}')

@bot.command(name='play', help='Toca uma música do YouTube')
async def play(ctx, *, search: str):
    if not ctx.message.author.voice:
        await ctx.send("Você precisa estar em um canal de voz para tocar música!")
        return

    channel = ctx.message.author.voice.channel
    
    # Entra no canal de voz se não estiver
    voice_client = ctx.voice_client
    if not voice_client:
        voice_client = await channel.connect()

    await ctx.send(f"Procurando por: **{search}**...")

    # Extrai o áudio sem baixar o vídeo
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(f"ytsearch:{search}", download=False))
    
    if 'entries' in data:
        data = data['entries'][0]

    song_url = data['url']
    title = data['title']

    # Toca a música
    if not voice_client.is_playing():
        voice_client.play(discord.FFmpegPCMAudio(song_url, **ffmpeg_options))
        await ctx.send(f"🎶 Tocando agora: **{title}**")
    else:
        await ctx.send("O bot já está tocando uma música! (Sistema de fila pode ser adicionado depois).")

@bot.command(name='stop', help='Para a música e sai do canal')
async def stop(ctx):
    voice_client = ctx.voice_client
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
        await ctx.send("Desconectado. Até a próxima!")
    else:
        await ctx.send("Eu não estou em um canal de voz.")

# Inicia o servidor web de mentira
keep_alive()

# Pega o token das variáveis de ambiente
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)