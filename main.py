import discord
import sys




import discord, io, sys

        
        
        
class cServer(discord.Client):
    async def on_ready(self):
        print("Server running")
        
    async def on_message(self, xMsg):
        if xMsg.author == client.user:
           return

        if len(xTerminals) == 0 or xTerminals[0] != "/bq":
            return
        
        xTerminals = xMsg.content.split(" ")
        xArgs = [x for x in xTerminals[1:] if x.strip()]

        if xArgs
        
                        
            
xToken = open("token.txt", "r").read()
xServer = cServer()    
xServer.run(xToken)