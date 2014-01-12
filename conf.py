# -*- coding: iso-8859-1 -*-

import os
#import files

class Confdat():
    """Speichermodel fuer die Configurationen"""
    def __init__(self):
            self.alias = []

class Conf():
    """Klasse fuer das Auslesen von .conf Dateien"""
    def __init__(self):

        self.files = []
        self.data = {}
        self.data['alias'] = {}

        self.data['var'] = {}
        self.data['list'] = {}
        self.data['tuple'] = {}

        #Comment Charachter
        self.__commentCh = "#"
        self.__endLine = ";"
        self.__pLineTmp = ""

    def addFile(self,conf):
        if not os.path.exists(conf):
            a = open(conf,"a")
            a.close()
        self.files.append(conf)
        return True

    def loadFiles(self):
        """Laedt alle Dateien nacheinander"""
        for f in self.files:
            conf = open(f,"r")
            self.parseFile(conf)
            conf.close()

    def parseFile(self,conf):
        conf = self.stripComments(conf)
        pconf = [];
        for l in conf:
            nl = self.parseLine(l)
            if nl is not "":
                pconf.append(nl)
                self.parseCmd(nl)
        return pconf

    def parseCmd(self,l):
        #Bereich der Zuweisung von d.h. enthaellt =
        if "=" in l:
            # Aufteilen der Befehle
            cmd = l.split("=")
            if cmd[0].startswith("alias "):
                # Zuweisen der Alias Befehle
                alkey = cmd[0][6:].strip()
                string = self.getString(cmd[1])
                self.data['alias'][alkey]=string
            elif cmd[0].strip().endswith("[]"):
                # Behandeln von Listen
                listname = cmd[0].strip()[:-2]
                if not listname in self.data["list"]:
                    self.data["list"][listname] = []
                self.data["list"][listname].append(self.getString(cmd[1]))
            elif cmd[0].strip().endswith("()"):
                # Behandeln von Tupeln
                tuplename = cmd[0].strip()[:-2]
                self.data["tuple"][tuplename] = self.getTuple(cmd[1]) 
            elif self.isString(cmd[1]):
                # Zuweisung der Variablen
                alkey = cmd[0].strip()
                string = self.getString(cmd[1])
                self.data['var'][alkey]=string
            else:
                # Zuweisung der Variablen
                alkey = cmd[0].strip()
                string = self.setType(cmd[1])
                self.data['var'][alkey]=string


    def parseLine(self,l):
        """Schreibt die Zeile in einen Zwischenspeicher oder liefert den Befehl zurueck"""
        if not self.__endLine in l:
            #Wenn kein Zeilenende definiert ist in den Speicher
            self.__pLineTmp = self.__pLineTmp + l
            return ""
        else:
            #Befehl zusammenbauen
            nl = self.__pLineTmp + l
            #Leerzeichen und Umbrueche entfernen
            nl = nl.strip()
            #Das ; entfernen
            nl = nl[:-1]
            #Zwischenspeicher loeschen
            self.__pLineTmp = ""
            return nl
                    

    def stripComments(self,conf):
        """Geht einmal durch die gane Datei und entfernt die Kommentare"""
        nconf = []
        for l in conf:
            if self.__commentCh in l:
                nconf.append(l[:l.find(self.__commentCh)])
            else:
                nconf.append(l)
        return nconf

    def isTuple(self,s):
        """Stell fest, ob es sich um ein Tupel handel"""
        s = s.strip()
        if s[0] == "(" and s[-1:]==")":
            return True
        else:
            return False
    
    def isString(self,s):
        """Stellt fest, ob es sich um ein String in Hochkomma handelt"""
        s = s.strip()
        if s[0] in ("'",'"') and s[0]==s[-1:]:
                return True
        else:
                return False
                    
    def getTuple(self,s):
        s = s.strip()
        seq = s[1:-1].split(",")
        entries = []
        for element in seq:
            entries.append(self.setType(element))
        return tuple(entries)
    
    def getString(self,s):
        """Extracts the the string between the hochkommas
        or gets an Alias"""
        s = s.strip()
        if self.isString(s):
                return s[1:-1]
        else:
                if self.data['alias'].has_key(s):
                        return self.data['alias'][s]
                else:
                        print "No key %s found as alias in the conf file" % s
    def setType(self,s):
        """ Gets an Inputstring and returns the value with the right datatype"""
        s = s.strip()
        if s.isdigit():
            return int(s)
        elif s.replace(".","").isdigit():
            return float(s)
        else:
            return s
    
    def setWriteString(self,s):
        """Gets the type and returns the string for the conf File
        just used for writing data to a file"""
        if isinstance(s,str):
            s = "\"%s\"" % (s)
        return str(s)
                        
    def writeConf(self,confFileName):
        """
        Schreibt die komplette Configuration in eine Datei
        """
        confFile = open(confFileName,"w")
        for key,val in self.data['alias'].iteritems():
            confFile.write("alias %s = \"%s\";\n" % (key,val))
        for key,val in self.data['var'].iteritems():
            confFile.write("%s = %s;\n" % (key,self.setWriteString(val)))
        for key,conflist in self.data['list'].iteritems():
            if len(conflist)>0:
                for val in conflist:
                    confFile.write("%s[] = %s;\n" % (key,self.setWriteString(val)))
        for key,tuple in self.data['tuple'].iteritems():
            if len(tuple)>0:
                writeStr = "%s() = (" % (key)
                for val in tuple:
                    writeStr = "%s%s," % (writeStr,self.setWriteString(val))
                confFile.write("%s);\n" % (writeStr[:-1]))
        confFile.close()
            