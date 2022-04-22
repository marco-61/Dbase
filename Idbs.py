"""
Classe     : Idbs.py
Scopo      : Questa classe aggiunge la gestione dei file indice alla classe dbs
Versione   : 1.5
Autore     : Marco Salvati
Data       : 2019-07-05
Revisione   : 2019-01-21 - 2019-04-24 - 2019-11-25
"""
import os,json
from dbase.dbs import *

__author__ = 'Marco Salvati'
__copyright__ = 'Marco Salvati, Copyright (c) 2019'
__license__ = "GPL 3"
__version__ = "1.5.0"
__email__ = "salvatimarco61@gmail.com"

class Idbs:
    def __init__(self,table,filename):
        self.__table=table
        self.__dbs=table.dbs
        self.__filename=filename
        self.__keys=[[]]
        self.__fields=[]
        self.__pk=False  # flag per chiave parziale
        self.__next=0
        self.__next_key=""
        self.__next_key2=""
        self.__pkType=-1
    def index(self,*fields):
        self.__fields=fields
        cursore=self.__dbs.tell() # salva la posizione del cursore
        cycle=range(1,len(self.__dbs))
        for i in cycle: # cicla l'intero dbs
            k=""
            self.__dbs.seek(i)
            for f in fields:
                rf=f.field
                k+="{}-".format(self.__dbs[rf])
            k=k[:-1] # elimina l'ultimo '-'
            self.__keys.append(k) # scrivi la chiave
            self.__keys[0].append(i) # scrivi il record
        self.__dbs.seek(cursore)  # ripristina il cursore  
       
    def reindex(self):
        self._keys=[[]]
        self.__index(self.__fields)
        
    def __contains__(self, key): # operatore in
        self.__pk=False 
        self.__next=0
        self.__next_key=""
        self.__next_key2=""
        self.__pkType=-1
        if "*" in key: # chiave parziale
            self.__pk=True
            return self.__PKsearch(key)
        else:
            if key in self.__keys: # chiave presente
                i=self.__keys.index(key) # posizione dell'indice nella sublista
                self.__dbs.seek(self.__keys[0][i-1])
                self.__next=i+1
                self.__next_key=key
                return True
            else:
                return False
    def __next__(self):
        return self.next()
    def next(self ):
        if self.__pk:
            if self.__pkType==1:
                return self.__testa()
            elif self.__pkType==2:
                return self.__coda()
            else:
                return self.__centro()
        else:    
            try:
                i=self.__keys.index(self.__next_key,self.__next)
                self.__dbs.seek(self.__keys[0][i-1])
                self.__next=i+1
                return True
            except ValueError as e:
                self.__next=0
                self.__next_key=""
                return False
            else:
                return False
    def __PKsearch(self,key):
        pos=key.index('*')
        self.__next=1
        if pos == 0: # coda qualsiasi
            self.__pkType=2
            self.__next_key2=key[pos+1:]
            r=self.__coda()
        elif pos == len(key)-1: # testa qualsiasi
            self.__pkType=1
            self.__next_key=key[:-1]
            r=self.__testa()
        else: # centro
            self.__pkType=2
            self.__next_key,self.__next_key2=key[:pos],key[pos+1:]
            r=self.__centro()
        return r
    def __testa(self):
        for i in range(self.__next,len(self.__keys)):
            if self.__keys[i].startswith(self.__next_key):
                self.__dbs.seek(self.__keys[0][i-1])
                self.__next=i+1
                return True              
        return False
       
    def __coda(self):
        for i in range(self.__next,len(self.__keys)):
            if self.__keys[i].endswith(self.__next_key2):
                self.__dbs.seek(self.__keys[0][i-1])
                self.__next=i+1
                return True
        return False
    def __centro(self):
        for i in range(self.__next,len(self.__keys)):
            if self.__keys[i].startswith(self.__next_key) and self.__keys[i].endswith(self.__next_key2):
                self.__dbs.seek(self.__keys[0][i-1])
                self.__next=i+1
                return True
        return False
    
    def flush(self):
        with open(self.__filename, 'w') as idb_file:
            json.dump(self.__keys,idb_file)# scrive il file indice
           
    def use(self):
         with open(self.__filename, 'r') as idb_file:
            self.__keys= json.load(idb_file)       
            self.__dbs.seek_to_start
    def dbs(self):
        self.__dbs # ritorna l'oggetto database
    def table(self): 
        self.__table # ritorna l'oggetto table
        
    def search(self,key,callback):
        if key in self:
            callback(True) # nessuno errore lancia alla routine utente
            
            while self.next():
                callback(True) # nessuno errore lancia la routine utente
        else:
            callback(False) # "Chiave non presente"
            
    

