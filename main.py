import discord
import os
from dotenv import load_dotenv
from helpers.tools import return_results, get_trigger_words, get_help_text, check_connection, return_moreinfo

load_dotenv()

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global results
    global object_type
    trigger_words = get_trigger_words()

    if message.author == client.user:
        return
    
    if message.content.startswith(f'{trigger_words["help"]}'):
        await message.channel.send(get_help_text(trigger_words))
    
    if message.content.startswith(f'{trigger_words["choose"]} '):
        a = int(message.content.split(' ', 1)[1].strip()) - 1
        
        if object_type == "":
            await message.channel.send('No item to select')
        
        elif object_type in ["book", "audiobook", "movie", "tv", "album"]:
            try:
                [info, components] = return_moreinfo(results[a], object_type)
                await message.channel.send(embed=info, view=components)
                results = []
                object_type = ''
            except Exception as inst:
                await message.channel.send(f"Unable to add this {object_type}. Please try again.\n Error: {inst}")
        else:
            await message.channel.send('This functionality is not available yet')
        results = []

    if message.content.startswith(f'{trigger_words["book"]} '):
        if check_connection("book"):
            from connectors.books import search_book
            a = message.content.split(' ', 1)[1]
            object_type = 'book'
            b = search_book(a)
            results = b
            await message.channel.send(return_results(b, "book", trigger_words))
        else:
            await message.channel.send("It looks like Readarr (for books) has not been set properly. Please ensure the container running this script has access to the Readarr instance, and the API key is entered correctly.")
    
    if message.content.startswith(f'{trigger_words["audiobook"]} '):
        if check_connection("audiobook"):
            from connectors.audiobooks import search_audiobook
            a = message.content.split(' ', 1)[1]
            object_type = 'audiobook'
            b = search_audiobook(a)
            results = b
            await message.channel.send(return_results(b, "audiobook", trigger_words))
        else:
            await message.channel.send("It looks like Readarr (for audiobooks) has not been set properly. Please ensure the container running this script has access to the Readarr instance, and the API key is entered correctly.")
    
    if message.content.startswith(f'{trigger_words["movie"]} '):
        if check_connection("movie"):
            from connectors.movies import search_movie
            a = message.content.split(' ', 1)[1]
            object_type = 'movie'
            b = search_movie(a)
            results = b
            await message.channel.send(return_results(b, "movie", trigger_words))
        else:
            await message.channel.send("It looks like Radarr has not been set properly. Please ensure the container running this script has access to the Radarr instance, and the API key is entered correctly.")
    
    if message.content.startswith(f'{trigger_words["tv"]} '):
        if check_connection("tv"):
            from connectors.tv import search_series
            a = message.content.split(' ', 1)[1]
            object_type = 'tv'
            b = search_series(a)
            results = b
            await message.channel.send(return_results(b, "show", trigger_words))
        else:
            await message.channel.send("It looks like Sonarr has not been set properly. Please ensure the container running this script has access to the Sonarr instance, and the API key is entered correctly.")
        
    if message.content.startswith(f'{trigger_words["music"]} '):
        if check_connection("music"):
            from connectors.music import search_album
            a = message.content.split(' ', 1)[1]
            object_type = 'album'
            b = search_album(a)
            results = b
            await message.channel.send(return_results(b, "album", trigger_words)) 
        else:
            await message.channel.send("It looks like Lidarr has not been set properly. Please ensure the container running this script has access to the Lidarr instance, and the API key is entered correctly.")


client.run(os.getenv('TOKEN'))