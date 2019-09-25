# stockx-checker-discord-bot
StockX Discord bot

prefix = '.'
Command = stockx

Example = .stockx (keywords)

This returns an embed of:

- StockX link with it's name
- Image of the item
- SKU/PID of the item if available
- The branding of the item
- Described Colorway of the item if available
- Retail price in $USD of the item
- Size : Lowest Ask : Highest Bid of the item
- Total # sold of the item
- Last size sold of the item corresponding with its price in $USD
- Average Asking price of the item

*You can use .hello to test if the bot is working

*Using keywords inputted by the user in which searches in the global url= https:/stockx.com/
and then grabs the first result that appears. It then uses StockX's unofficial APIto get it's official API which has significantly more data.

Please edit your discord bot token and your command prefix, if you wish.


