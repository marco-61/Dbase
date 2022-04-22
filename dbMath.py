"""
Classe     : dbMath.py
Scopo      : Classe di ausilio implementa vari funzioni matematiche 
Versione   : 1.0
Autore     : Marco Salvati
Data       : 2019-11-21
Revisione   : 2019-01-21 - 2019-01-24
"""
#from dbase.dbs import dbs
from dbase.Table import Table

class OnlyNumbersError(Exception):
    """Solo campi numerici"""
    pass

class dbMath:
    def __init__(self,table):
        self.dbase=table.dbs
    # -------------------------------------Operazioni-----------------------------------------------------------------------
    def total(self,field,Filter=None): #effettua il totale di un campo numerico gestisce un eventuale condizione  
        rec=self.dbase.tell() # salva il puntatore
        if Filter is not None: # Filter chiamata callback da gestire
            flag=True
        else:
            flag=False
        conta=0
        campo=field.field
        tipo=self.dbase.fieldType(campo)
        if tipo in("Integer","Float","Complex"):
            self.dbase.seek_to_start()
            while not self.dbase.eof():
                value=field.value
                if flag:
                    if Filter(value):
                        conta+=value
                else:  
                    conta+=value
                next(self.dbase)           
        self.dbase.seek(rec) # ripristina il puntatore
        return conta
        
   
    def average(self,field,Filter=None):
        conta=self.total(field,Filter)
        l=len(self.dbase)-1
        return conta / l
    
    def min(self,field):
        rec=self.dbase.tell() # salva il puntatore
        tipo=field.field_Type
        if tipo in("Integer","Float","Complex"):
            self.dbase.seek_to_start()
            vmin=field.value
            while not self.dbase.eof():
                v=field.value
                if tipo=="Complex":
                    if vmin.real > v.real:
                        vmin=v
                    elif (vmin.real == v.real)and(vmin.imag>v.imag):
                        vmin=v
                elif vmin>v:
                    vmin=v
                next(self.dbase)      
        else:
            raise OnlyNumbersError('Solo campi numerici')
        self.dbase.seek(rec) # ripristina il puntatore
        return vmin
    
    def max(self,field):
        rec=self.dbase.tell() # salva il puntatore
        campo=field.field
        tipo=self.dbase.fieldType(campo)
        if tipo in("Integer","Float","Complex"):
            self.dbase.seek_to_start()
            vmax=field.value
            while not self.dbase.eof():
                v=field.value
                if tipo=="Complex":
                    if vmax.real < v.real:
                        vmax=v
                    elif(vmax.real == v.real)and(vmax.imag<v.imag):
                         vmax=v
                elif vmax<v:
                    vmax=v
                next(self.dbase)        
        else:
            raise OnlyNumbersError('Solo campi numerici')
        self.dbase.seek(rec) # ripristina il puntatore
        return vmax

    
