import discord
import sys
import Compiler
import threading
import vm
import io
import discord, io, sys

        
DELIM = '```'
        
class cServer(discord.Client):
    def __init__(self):
        super().__init__()
        Compiler.cUtils.Error = cServer.CompError
            
    @staticmethod
    def CompError(xMsg):
        raise Exception(xMsg)
    
    
    def Cons(self, xTerms):
        xBuffer = []
        while len(xTerms) > 0 and xTerms[0] != DELIM: 
            xBuffer.append(xTerms.pop(0))
            
        return xBuffer
    
    def Depo(self, xTerms):
        if len(xTerms) > 0 and xTerms[0] == DELIM:
            xTerms.pop(0)       
    
    async def on_ready(self):
        print("Server running")
        
    async def on_message(self, xMsg):
        if xMsg.author == xServer.user:
           return
       
        xTerminals = xMsg.content.split("\n")
        if len(xTerminals) == 0 or xTerminals[0].strip() != "/bq":
            print(f'Message "{xTerminals}" not matching')
            return
        
        #consume terminals
        xArgs = [x for x in xTerminals[1:] if x.strip()]
                
        xCall        = self.Cons(xArgs)
        self.Depo(xArgs)
        xCodeBuffer  = self.Cons(xArgs)
        self.Depo(xArgs)
        xInputBuffer = self.Cons(xArgs)
        self.Depo(xArgs)

        try:
            self.xCompiler = Compiler.cCompiler()
            xAsm = self.xCompiler.Compile("\n".join(xCodeBuffer))

        except Exception as E:
            await xMsg.channel.send(f'<@{xMsg.author.id}> {E}')

        else:
            xVM = vm.cMain()
            xVM.LoadFile(xAsm[0])
            
            xTempStd = sys.stdout
            sys.stdout = xStdOutCap = io.StringIO()
            
            xRunner = threading.Thread(target = xVM.Interpret)
            xRunner.start()
            xRunner.join(timeout = 5)
                        
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
            
                    
xToken = open("token.txt", "r").read()
xServer = cServer()    
xServer.run(xToken)