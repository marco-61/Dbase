"""
Classe     : dbcopy.py
Scopo      : Classe di ausilio implementa vari funzioni di copia 
Versione   : 1.0
Autore     : Marco Salvati
Data       : 2019-11-21
Revisione   : 2019-01-21 - 2019-01-24
"""
#from dbs import dbs
from dbase import *
from dbase.Shared import Shared

class dbCopy:
    def __init__(self,table):
        self.__Shared=Shared()
        self.__dbs=self.__Shared.get_table(table)
      # -------------------Copy Structure----------------------------------------------------
    def copy_structure_to(self,dest_table):
        # copia la struttura del file in da un oggetto a un nuovo oggetto dbs
        self.__dbs2=self.__Shared.get_table(table)
        fields=self.__dbs.dbFields_get
        self.__dbs2.dbFields_set(list(fields))
        
    # ------------------Copy Fields-------------------------------------------------------
    def copy_field_to(self,table2,fields:list,Filter=None):
        # crea un nuovo dbs Filtra i campi indicati
        self.__dbs2=self.__Shared.get_table(table)
        if Filter !=None: # Filtra in  una chiamata callback da gestire
            flag=True
        else:
            flag=False    
        ddiz,f,l=dict(),"",[]
        sdiz=self.__dbs.fields_to_dict
        for j in fields:
            tipo=sdiz[j]
            f="{}:{}".format(j,tipo)
            l.append(f)
        db.dbFields_set(l)
         
        for i in self.__dbs.db_iter():
            rec,ddiz=dict(),dict() #
            rec=self.__dbs.get_record(i)
            if flag: # effettua una valutazione e torna true se ok altrimenti false
                if Filter(rec):
                    for j in fields:
                        ddiz[j]=rec[j]
                    db.append(ddiz)
            else: # tutti ok
                for j in fields:
                    ddiz[j]=rec[j]
                db.append(ddiz)

    def copy_field_to_file(self,filename,*fields,Filter=None):
        # crea un nuovo dbs Filter i campi indicati
        db=dbs(filename)
        self.copy_field_to(db,fields,Filter)
        db.flush()
    
    def copy_from_to(self,db,field_from,field_to):
        """ Copia una  serie di campi anche con un altro nome in un nuovo dbs il nuovo
            deve avere una sua tabella di campi"""
        cursore=self.__dbs.tell
        self.__dbs.seek_to_start
        for i in self.__dbs.db_iter():
            self.__dbs.seek(i)
            db.append_blank
            for i,field in enumerate(field_from):
                db[field_to[i]]=self.__dbs[field]
                
        self.__dbs.seek(cursore)        
            
