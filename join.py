"""
Classe     : join.py
Scopo      : Copia i campi da una ho più tabelle in un nuova nuova tabella
Versione   : 2.0
Autore     : Marco Salvati
Data       : 2021-03-05
"""
from dbase.dbs import dbs
from dbase.Table import Table
from dbase.Field_type import Field_type

def join(sfields,dfields,Filter=None):
    """ copia in un database vuoto i campi indicati con un possibile filtraggio
     con  una chiamata callback da gestire"""
    flag= False if Filter is None else True
    db1=sfields[0].dbs # tabelle di riferimento
    db2=dfields[0].dbs
    l1=db1.dbLen() # record in db1
    l2=db2.dbLen() # record in db2
    rec=db1.tell()
    rec2=db2.tell()
    if l1-l2>0:
        for i in range(l1-l2): db2.append_blank() # crea i posti
    for f1,f2 in zip(sfields,dfields): # itera su entrambe le liste
        db1.seek_to_start()
        db2.seek_to_start()
        while not db1.eof():
            if flag:
                if not Filter(f1,f2): # se il filtro è attivo funzione utente
                    f2.value=f1.value    
                
                db1.next()
                db2.next()    
            else: 
                f2.value=f1.value
                db1.next()
                db2.next()
            
    db1.seek(rec)
    db2.seek(rec2)
    
            
