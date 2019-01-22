from bs4 import BeautifulSoup
import asyncio
import discord
import requests
from discord.ext import commands
import json
import urllib
from requests.utils import requote_uri

token = 'TOKEN' #Put your token here

prefix = ['.'] #You can change this if you'd like

bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    print('Bot is ready')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

@bot.command(pass_context=True)
async def hello(ctx):
    msg = 'Hello, {0.author.mention}'.format(ctx.message)
    await bot.send_message(ctx.message.channel, msg)


@bot.command(pass_context=True)
async def stockx(ctx, *keywords):
    #url = 'https://stock.com/search?s='
    searchUrl = " ".join(keywords)
    encodeUrl = requote_uri(searchUrl)
    json_string = json.dumps({"params": f"query={encodeUrl}&hitsPerPage=20&facets=*"})
    byte_payload = bytes(json_string, 'utf-8')
    x = {"x-algolia-agent": "Algolia for vanilla JavaScript 3.27.1", "x-algolia-application-id": "XW7SBCT9V6", "x-algolia-api-key": "6bfb5abee4dcd8cea8f0ca1ca085c2b3"}
    with requests.Session() as s:
        r = s.post("https://xw7sbct9v6-dsn.algolia.net/1/indexes/products/query", params=x, verify=False, data=byte_payload, timeout=30)
        hits = r.json()["hits"][0] #hits is like results
        apiurl = f"https://stockx.com/api/products/{hits['url']}?includes=market,360&currency=USD"

        header = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,ja-JP;q=0.8,ja;q=0.7,la;q=0.6',
            'appos': 'web',
            'appversion': '0.1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        response = requests.get(apiurl, verify=False, headers=header).json()
        try:
            Colorway = str(response['Product']['colorway'])
        except:
            Colorway = 'N/A'
        try:
            SKU = str(response['Product']['traits'][0]['value'])
        except:
            SKU = 'N/A'
        try:
            Retail = response['Product']['retailPrice']
        except:
            Retail = response['Product']['traits'][3]['value']
        try:
            stockx_image = str(response['Product']['media']['360'][0])
        except:
            stockx_image = str(response['Product']['media']['imageUrl'])


        Brand = str(response['Product']['brand']).title()
        urlKey = str(response['Product']['urlKey']).title()
        min_bid = response['Product']['minimumBid']
        shoe_name = str(response['Product']['title']).title()
        highest_bid = response['Product']['market']['highestBid']
        shoe_sizes = response['Product']['children']
        total_sold = response['Product']['market']['deadstockSold']
        last_sold_price = response['Product']['market']['lastSale']
        last_sold_size = response['Product']['market']['lastSaleSize']
        average_ask = response['Product']['market']['averageDeadstockPrice']

        shoe_data = ''
        if Retail >= 0:
            Retail = '$'+str(Retail)
        if min_bid >= 0:
            min_bid = '$'+str(min_bid)
        if average_ask >=0:
            average_ask = '$'+str(average_ask)
        if last_sold_price >=0:
            last_sold_price = '$'+str(last_sold_price)
        last_sold = str(last_sold_size) + ' | ' + ' ' + str(last_sold_price)
        for size in shoe_sizes:
            shoe_data += f"Size {shoe_sizes[size]['shoeSize']} | Min Ask ${shoe_sizes[size]['market']['lowestAsk']} | Max Bid ${shoe_sizes[size]['market']['highestBid']}\n"


        e = discord.Embed(title=str(shoe_name).title(), url='https://stockx.com/' + urlKey, color=0x00FFFF)
        e.set_thumbnail(url=stockx_image)
        e.add_field(name='SKU/PID', value=SKU, inline=True)
        e.add_field(name='Color:', value=Colorway, inline=True)
        e.add_field(name='Brand:', value=Brand, inline=True)
        e.add_field(name='Retail Price:', value=Retail, inline=True)
        e.add_field(name='Total Sold:', value=total_sold, inline=True)
        e.add_field(name='Last Sold:', value=last_sold, inline=True)
        e.add_field(name="Average Ask", value=average_ask, inline=True)
        e.add_field(name="Sizes:", value=shoe_data, inline=False)



        await bot.send_message(ctx.message.channel,embed=e)





bot.run(token)
