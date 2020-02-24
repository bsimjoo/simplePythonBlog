import cherrypy
import configparser
import re
import os
from Configuration import *

class HomePage:
    def __init__(self):
        self.HtmlPage=None

    @cherrypy.expose
    def index(self):
        if self.HtmlPage==None:
            templateFile=open(HomePageTemplateFile)
            self.HtmlPage=ConvertTemplateCode(templateFile.read(),LoopSource={'post':postIterator(PostsDir)})
            templateFile.close()
        return self.HtmlPage

def ConvertTemplateCode(TemplateCode:str,VarsDictionary=DefaultVariables,LoopSource=None):
    result=TemplateCode
    searchPattern=re.compile(r'(\[::([^\]]*)])')        #searching for template code variables
    for oldString,variableName in searchPattern.findall(result):
        if variableName in VarsDictionary:
            result=result.replace(oldString,VarsDictionary[variableName])
    if LoopSource!=None:

        for regGroups in re.findall(r'(\[::foreach (\w*)](\n(\s*((?!\[::end\]).)*\n?)*)\[::end])',result):
            #searching for template code foreach
            #foreach regex groups:
            # 0: old full string for replacing
            # 1: foreach source
            # 2: repeatable template
            # 3: the last content line.(no needed, just needed for regex algurithm)
            newHtml=''
            for localVarsDict in LoopSource[regGroups[1]]:
                sec=ConvertTemplateCode(regGroups[2])
                sec=ConvertTemplateCode(sec,localVarsDict)
                newHtml+=sec
            result=result.replace(regGroups[0],newHtml)
    return result

class postIterator:
    def __init__(self,filesDir):
        self.filesDir=filesDir
        self.filesList= [os.path.join(filesDir,p) for p in os.listdir(filesDir)]
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if len(self.filesList)>0:
            filePath=self.filesList.pop()
            f=open(filePath)
            header=f.readline()
            res=f.read()
            f.close()
            return {'header':header,'content':res}
        raise StopIteration

if __name__ == "__main__":
    conf = {"global":
        {
            "server.socket_host": 'localhost',
            "server.socket_port": 80,
            "log.screen": True,
            "log.access_file": 'access.txt',
            "log.error_file": 'error.log',
            "tools.staticdir.root": '\\',
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "",
        }
    }
    cherrypy.quickstart(HomePage(), "/", conf)
