import discord

class Buttons(discord.ui.View):
    def __init__(self, *, dict, type, timeout=None):
        super().__init__(timeout=timeout or 180)
        self.dict = dict
        self.type = type
        self.voted_users = []

        self.upvote_count = 0
        self.downvote_count = 0

    @discord.ui.button(
        label="Yes", style=discord.ButtonStyle.success, emoji="👍"
    )
    async def confirm_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        b = ''
        if self.type == "book":
            from connectors.books import add_book
            b = add_book(self.dict)
        elif self.type == "audiobook":
            from connectors.audiobooks import add_audiobook
            b = add_audiobook(self.dict)
        elif self.type == 'movie':
            from connectors.movies import add_movie
            b = add_movie(self.dict)
        elif self.type == 'tv':
            from connectors.tv import add_series
            b = add_series(self.dict)
        elif self.type == 'album':
            from connectors.music import add_album
            b = add_album(self.dict)
        else:
            b = "Unable to add this item right now"
        await interaction.response.send_message(b, ephemeral=True)
        return True

    @discord.ui.button(label="No", style=discord.ButtonStyle.danger, emoji="👎")
    async def cancel_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message("Selection has been cancelled", ephemeral=True)
        return False