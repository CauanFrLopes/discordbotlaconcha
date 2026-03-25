import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os
from keep_alive import keep_alive

# Configuração de Intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Configurações otimizadas para o SoundCloud (Evita bloqueios)
ytdl_format_options = {
    'format': 'bestaudio/best',
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
    print(f'✅ Bot logado como {bot.user}')
    print('✅ Servidor de áudio pronto!')

@bot.command(name='play')
async def play(ctx, *, search: str):
    if not ctx.message.author.voice:
        await ctx.send("❌ Entra num canal de voz primeiro!")
        return

    channel = ctx.message.author.voice.channel
    voice_client = ctx.voice_client
    if not voice_client:
        voice_client = await channel.connect()

    await ctx.send(f"🔍 Procurando: **{search}**...")

    # AQUI ESTÁ O TRUQUE: scsearch (SoundCloud) em vez de ytsearch
    loop = asyncio.get_event_loop()
    try:
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(f"scsearch:{search}", download=False))
        if 'entries' in data:
            data = data['entries'][0]

        song_url = data['url']
        title = data['title']

        if not voice_client.is_playing():
            voice_client.play(discord.FFmpegPCMAudio(song_url, **ffmpeg_options))
            await ctx.send(f"🎶 Tocando agora: **{title}**")
        else:
            await ctx.send("⚠️ Já estou a tocar uma música!")
    except Exception as e:
        await ctx.send(f"❌ Erro ao processar áudio: {e}")

@bot.command(name='stop')
async def stop(ctx):
    voice_client = ctx.voice_client
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
        await ctx.send("👋 Desconectado!")

keep_alive()
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)
