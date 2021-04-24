import discord
from discord.ext import commands
from PIL import Image
from io import BytesIO
from PIL import ImageFont, ImageDraw, ImageOps
import os
import arabic_reshaper
import json
from bidi.algorithm import get_display

with open('./config.json', 'r') as f:
    config = json.load(f)


def cleanword(word):
    if len(word) == 1:
        return word
    if word[0] == word[1]:
        return cleanword(word[1:])
    return word[0] + cleanword(word[1:])


class welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(config["welcome_channel"])  # get channel

        img = Image.open("./img/welcome.png")
        ava = member.avatar_url_as(size=128)  # resize avatar member
        data = BytesIO(await ava.read())
        pfp = Image.open(data)

        pfp = pfp.resize((321, 321))
        bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
        mask = Image.new('L', bigsize, 0)

        img.paste(pfp, (163, 104))

        draw = ImageDraw.Draw(mask)

        draw.ellipse((0, 0) + bigsize, fill=255)

        mask = mask.resize(pfp.size, Image.ANTIALIAS)

        pfp.putalpha(mask)

        output = ImageOps.fit(pfp, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        output.save('./img/output.png')
        background = Image.open('./img/welcome.png')

        draw = ImageDraw.Draw(background)
        background.paste(pfp, (125, 52), pfp)

        font = ImageFont.truetype("./fonts/Arial.ttf", size=100)  # font all text
        stroke_width = 2  # stroke width
        color_stroke = "black"  # color stroke

        reshaped_text = arabic_reshaper.reshape(member.name)
        bidi_text = get_display(reshaped_text)
        text = cleanword(word=bidi_text)

        if len(text) > 9:
            text = text[:10] + "..."
        elif len(text) > 8:
            text = text[:9] + ".."
        elif len(text) > 7:
            text = text[:8] + "."

        draw.text(
            [500, 215],
            text,  # add arabic
            font=font,
            stroke_width=stroke_width,
            stroke_fill=color_stroke)

        background.save('./img/overlap.png')
        await channel.send(
            f"مرحبا بك بسيرفر زاك بونش للاعياد: {member.mention}\nrules : <#781902561333870623>",
            file=discord.File("./img/overlap.png"))
        os.remove("./img/output.png")
        os.remove("./img/overlap.png")


def setup(client):
    client.add_cog(welcome(client))
