
def pre_text(type):
    return f'I have found the following {type}s:\n \n'

def post_text(type, choose):
    return f'\nChoose your {type} by typing `{choose}` followed by the number of the item above'

def return_results(dicts, type, trigger_words):
    n=1
    arr = []
    if type in ['book', 'audiobook']:
        for i in dicts:
            arr.append(f'{n}. **{i["title"]}** by *{i["author"]["authorName"]}* \n')
            n=n+1
    elif type in ['movie', 'show']:
        for i in dicts[:10]:
            arr.append(f'{n}. **{i["title"]}** ({i["year"]}) \n')
            n=n+1
    elif type=="album":
        for i in dicts:
            arr.append(f'{n}. **{i["title"]}** by *{i["artist"]["artistName"]}* \n')
            n=n+1
    return pre_text(type) + ''.join(arr) + post_text(type, trigger_words["choose"])

def return_moreinfo(dict, type):
    from discord import Embed
    from helpers.buttons import Buttons
    a = Embed(title=f'Is this the {type} you are looking for?')
    confirm_button = Buttons(dict=dict, type=type)
    b = confirm_button
    if type in ['book', 'audiobook']:
        a.add_field(name='Title', value=dict["title"], inline=False)
        a.add_field(name='Author', value=dict["author"]["authorName"], inline=False)
        a.set_image(url=dict["images"][0]["url"])
    elif type in ['movie', 'tv']:
        a.add_field(name='Title', value=f'{dict["title"]} ({dict["year"]})', inline=False)
        a.add_field(name='Overview', value=dict["overview"], inline=False)
        a.set_image(url=dict["remotePoster"])
    elif type == 'album':
        a.add_field(name='Title', value=f'{dict["title"]}', inline=False)
        a.add_field(name='Artist', value=f'{dict["artist"]["artistName"]}', inline=False)
        #a.add_field(name='Overview', value=dict["overview"], inline=False)
        a.set_image(url=dict["remoteCover"])
    return [a,b]

def check_connection(type):
    import os
    if type == 'book' and os.getenv('READARR_BOOK_URL') and os.getenv('READARR_BOOK_APIKEY'):
        return True
    elif type == 'audiobook' and os.getenv('READARR_AUDIOBOOK_URL') and os.getenv('READARR_AUDIOBOOK_APIKEY'):
        return True
    elif type == 'movie' and os.getenv('RADARR_URL') and os.getenv('RADARR_APIKEY'):
        return True
    elif type == 'tv' and os.getenv('SONARR_URL') and os.getenv('SONARR_APIKEY'):
        return True
    elif type == 'music' and os.getenv('LIDARR_URL') and os.getenv('LIDARR_APIKEY'):
        return True
    else:
        return False

def get_trigger_words():
    import os
    a = {}
    def get_trigger_word(b, c):
        if os.getenv(f'BOT_TRIGGER_{b}'):
            return os.getenv(f'BOT_TRIGGER_{b}')
        elif os.getenv('BOT_TRIGGER'):
            return f'{os.getenv("BOT_TRIGGER")}{c}'
        else:
            return f'/{c}'
    a["help"] = get_trigger_word('HELP', 'help')
    a["choose"] = get_trigger_word('CHOOSE', 'choose')
    a["book"] = get_trigger_word('BOOK', 'book')
    a["audiobook"] = get_trigger_word('AUDIOBOOK', 'ab')
    a["movie"] = get_trigger_word('MOVIE', 'movie')
    a["tv"] = get_trigger_word('TVSHOW', 'tv')
    a["music"] = get_trigger_word('MUSIC', 'album')
    return a
        
def get_help_text(d):
    return f'''
# Discarr

Thank you for trying Discarr, a Discord bot that listens to you and begins the downloads of items you request.
## Search
First you will have to search for the relevant media by the following methods.
### Books

To search for a book type `{d["book"]}` followed by the book you would like.
> `{d["book"]} Robinson Crusoe`
### Audiobooks

To search for an audiobook type `{d["audiobook"]}` followed by the audiobook you would like.
> `{d["audiobook"]} Sapiens`
### Movies

To search for a movie type `{d["movie"]}` followed by the movie you would like.
> `{d["movie"]} 12 Years A Slave`
### TV Shows

To search for a TV show type `{d["tv"]}` followed by the series you would like.
> `{d["tv"]} Arrested Development`
### Music Albums

To search for an album type `{d["music"]}` followed by the album you would like.
> `{d["music"]} 1989`
## Select

If successful, Discarr will return to you a numbered list of options.
Select the listing you would like to add by typing `{d["choose"]}` followed by the number of the item.
> `{d["choose"]} 2`

## Test
In the future, testing connections will also be possible via this bot. For now, this is work in progress

'''