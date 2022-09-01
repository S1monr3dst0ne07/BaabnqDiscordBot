import discord
import sys
import Compiler
import threading
import vm
import io
import discord, io, sys
from discord.ext import commands

xIntents = discord.Intents.all()
xClient = commands.Bot(command_prefix='/', intents=xIntents)        
DELIM = '```'
        
class cServer:            
    @staticmethod
    def CompError(xMsg):
        raise Exception(xMsg)
    
    @staticmethod
    def Cons(xTerms):
        xBuffer = []
        while len(xTerms) > 0 and xTerms[0] != DELIM: 
            xBuffer.append(xTerms.pop(0))
            
        return xBuffer
    
    @staticmethod
    def Depo(xTerms):
        if len(xTerms) > 0 and xTerms[0] == DELIM:
            xTerms.pop(0)       
    
    @xClient.event
    async def on_ready():
        print("Server running")

    @xClient.event
    async def on_message(xMsg):
        if xMsg.author == xClient.user or not xMsg.content.startswith("/bq"):
           return

        if xMsg.attachments:
            xCodeBuffer = str((await xMsg.attachments[0].read()).decode('utf-8')).replace("\r", "").split("\n")            
            
        else:            
            #consume terminals
            xTerminals = xMsg.content.split("\n")
            xArgs = [x for x in xTerminals[1:] if x.strip()]
            xCall        = cServer.Cons(xArgs)
            cServer.Depo(xArgs)
            xCodeBuffer  = cServer.Cons(xArgs)
            cServer.Depo(xArgs)
            xInputBuffer = cServer.Cons(xArgs)
            cServer.Depo(xArgs)



        try:
            xCompiler = Compiler.cCompiler()
            xAsm = xCompiler.Compile("\n".join(xCodeBuffer))

        except Exception as E:
            await xMsg.channel.send(f'<@{xMsg.author.id}> {E}')

        else:
            xVM = vm.cMain()
            xVM.LoadFile(xAsm[0])
            xVM.xConfig.update({ "DisplayTime" : True })
            
            xTempStd = sys.stdout
            sys.stdout = xStdOutCap = io.StringIO()
            
            xRunner = threading.Thread(target = xVM.Interpret)
            xRunner.start()
            xRunner.join(timeout = 30)
                        
            if xRunner.is_alive():
                await xMsg.channel.send(f'<@{xMsg.author.id}> Timeout reached, killing runner (sorry QwQ)')
                xVM.xProgrammIndex = len(xVM.xLineStructures) + 1
                
            else:
                try:
                    xOutput = xStdOutCap.getvalue()
                    await xMsg.channel.send(f'```\n{xOutput}\n```')

                except discord.errors.HTTPException:
                    await xMsg.channel.send(f'<@{xMsg.author.id}> Senpai, *moan*, your output is too big')
                    

                
            sys.stdout = xTempStd
            xRunner.join()
            
                    
Compiler.cUtils.Error = cServer.CompError
xToken = open("token.txt", "r").read()
xClient.run(xToken)



