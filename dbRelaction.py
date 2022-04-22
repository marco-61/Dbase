"""
Classe     : dbRelaction.py
Scopo      : Relazione due o più database tramite un campo chiave univoco
Autore     : Marco Salvati
Data       : 2019-07-05
Revisione   : 2019-01-21 - 2019-04-24
"""

from dbase.dbs import dbs
from dbase.Idbs import Idbs

class dbRelaction:
    def __init__(self,*objdb:Idbs):
        self.__objdb=list(objdb)
        
    def __contains__(self, key): # operatore in
        code=[]
        for i in self.__objdb:
           if key in i:
               code.append(True)
           else:
               code.append(False)
        return not False in code #se uno solo del campi indice da falso non procedere
    def append_blank(self): #appende un record vuoto in tutti i dbs
        for i in self.__objdb:
            i.table.append_blank()
    def flush(self): # salva tutti le tabelle in memoria e i file indice           
        for i in self.__objdb:
            i.table.flush()
            i.flush()
    def reindex(self):  #reindicizza tutti i gli oggetti indice
         for i in self.__objdb:
            i.reindex()      
