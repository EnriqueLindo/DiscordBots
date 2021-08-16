import urllib.request
import re
 
import youtube_dl
import asyncio
import discord

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
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
 
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
 
class Youtube():
    async def FindVideo(video):
        video = video.split(" ")
        video = '+'.join(video)

        url = "https://www.youtube.com/results?search_query=" + video

        html = urllib.request.urlopen(url)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())        

        link = "http://www.youtube.com/watch?v=" + video_ids[0]      
        
        return link
    
    async def ExtractAudio(URL):
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(URL, download=False))

        #data = ytdl.extract_info(URL, download=False)

        fl = data['url']
        title = data['title']
 
        ms = discord.FFmpegPCMAudio(fl, **ffmpeg_options)
        return ms, title