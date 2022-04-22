"""
Classe     : dbs.py
Scopo      : Classe contenente le primitive per la gestione del database

Versione   : 2.0
Autore     : Marco Salvati
Data       : 2019-01-04
Revisione   : 2019-01-21 - 2019-01-24 - 04-03-2021
"""
import os,json
import datetime
from queue import SimpleQueue

__author__ = 'Marco Salvati'
__copyright__ = 'Marco Salvati, Copyright (c) 2019'
__license__ = "GPL"
__version__ = "3.0.0"
__email__ = "salvatimarco61@gmail.com"

class dbs:
    def __init__(self,dbName):
        self.__dbName=dbName # nome di default del database
        self.__fields={} # campi e loro tipo
        self.__dbAr=[] # database
        self.__seek=0  # puntatore al record attuale 
        self.__order=-1
        self.__queue=SimpleQueue()
        self.q=self.__queue
    #----------------------Gestione Database in memoria------------------
    
    def free_field(self): #Chiamata dalle classi fiel_type incrementa il numero di campi assegnati
        self.__order+=1
        return str(self.__order)
    
    def seek(self,record): # posiziona il puntatore sul record desiderato
        if record<1:
            self.__seek=1
        if record <self.__len__():
            self.__seek=record
              
    def tell(self):          # ritorna la posizione del puntatore del file
        return self.__seek
    
    def seek_to_start(self): # posiziona il puntatore sul primo record
        self.__seek=1
        
       
    def seek_to_end(self):   # posiziona il puntatore sull'ultimo record 
        self.__seek=self.__len__()-1
       
    def __next__(self):         # prossimo record
        if self.__seek<self.__len__():
            self.__seek+=1


    def eof(self):          # ritorna True se fine file
        if self.tell() < self.__len__():
            return False
        else:
            return True
        
    def append_blank(self):  #Crea un record vuoto
        
        d={}
        for k in range(self.__order+1):
            d[str(k)]=None
        self.__dbAr.append(d)
        self.seek_to_end()
            
    def fieldType(self,field): # ritorna il tipo di campo
        r=self.__dbAr[0]
        t=r[field]
        if '(' in t:
            a=t.split('(')
            a=a[0]
        else:
            a=t
        return a

    def fieldValue(self,record,field): # ritorna il valore di un campo
        r=self.__dbAr[record]
        t=r[field]
        return t
        
        # ------------------------- Carica il database in memoria -----------------------------
    def __dbLoad(self,name): # uso interno
        # carica il database
        with open(name, 'r') as dbs_file:
            self.__dbAr= json.load(dbs_file) 
        self.seek_to_start()
        
    def use(self,name=""):
        # permette di aprire correttamente il dbs
        if name=="": name=self.__dbName
        if self.dbAccess(name):
            if self.isValidDb(name):
                self.__dbLoad(name)
                return 0 # file aperto correttamente
            else:
                return -1 # il file esiste, ma non  un valido dbs
        else:
            return 2 # il dbs  non esiste

         #-------------------------------Salva il database---------------------------
    def flush(self,name=""):
        # salva il database
        if name=="": name=self.__dbName
        with open(name, 'w') as dbs_file:
            json.dump(self.__dbAr,dbs_file)# scrive il database

    def dbCreate(self,name=""):
        # crea un database vuoto con la tabella dei campi
        if name=="": name=self.__dbName
        with open(name, 'w') as dbs_file:
            json.dump([self.__dbAr[0]],dbs_file)# scrive la tabella dei campi

    def __len__(self):     # ritorna il numero di record del database
        return len(self.__dbAr)
 
    def isValidDb(self,name):    # Controlla se è un database valido
        with open(name,"r") as f:
            m=f.read(2)
        if m=="[{":
            return True
        else:
            return False

    def dbAccess(self,filename):
        # ritorna true se il database o qualsiasi altro file esiste
        if filename=="": filename=self.__dbName
        return os.access(filename,os.F_OK)        

           # -----------------ITEM---------------------------------------
    def __getitem__(self,key):   #legge una chiave del record
        dt=self.__dbAr[self.tell()]
        return dt[key]
    
    def __setitem__(self,key,value): # setta una chiave del record
        d=self.__dbAr[self.tell()]
        d[key]=value
        self.__dbAr[self.tell()]= d
    def __delitem__(self,record): #Cancella il record desiderato se record=0 cancella il record attuale
        if isinstance(record, int):
            if record >0 and record <self.__len__():
                del self.__dbAr[record]
            elif record==0:
                record=self.tell()
                del self.__dbAr[record]
        elif isinstance(record, slice): #cancella più record contigui
            if record.start is None or record.start==0:
                del self.__dbAr[1:record.stop:record.step]#evita di cancellare la tabella dei record
            else:
                del self.__dbAr[record]

        # -------------------Sort database-------------------------------------
    
    def sort(self,field,reverse=False): # sort del database per il campo assegnato
        c=self.__dbAr[1:] # record database
        t=self.__dbAr[:1] # tabella dei campi
        c.sort(key=lambda item: item[field],reverse=reverse)
        self.__dbAr=t+c
    
    def dbGet(self):    # ritorna una copia dell' intero database
        return self.__dbAr[:]
          
    def search(self,dato,field): # Ricerca sequenziale
        # trova un elenco di voci per il campo indicato ricerca sequenziale
        ft=field
        voce=1
        d=dict()
        if '*' in dato:
            return self.__chiave_parziale(dato,field)           
        for i in range(1,self.__len__()):
            d=self.__dbAr[i]
            dato2=d[ft]
            if dato==dato2:
                self.__queue.put(voce)
            voce+=1
        if not self.__queue.empty():
            self.seek(self.__queue.get())        
            return True
        else:
            return False
            
    def __chiave_parziale(self,dato,field): #uso interno
        ft=field
        voce=1
        d=dict()        
        k=dato.split('*')
        if k[0]=='': # '*'  in testa
            for i in range(1,self.__len__()):
                d=self.__dbAr[i]
                dato2=d[ft]
                if dato2.endswith(k[1]):
                    self.__queue.put(voce) 
                voce+=1
            if not self.__queue.empty():
                self.seek(self.__queue.get())
                return True
            else:
                return False
        elif k[1]=='': # in coda
            for i in range(1,self.__len__()):
                d=self.__dbAr[i]
                dato2=d[ft]
                if dato2.startswith(k[0]):
                    self.__queue.put(voce) 
                voce+=1
            if not self.__queue.empty():
                self.seek(self.__queue.get())
                return True
            else:
                return False

        else: # al centro
            for i in self.db_iter():
                d=self.__dbAr[i]
                dato2=d[ft]
                if dato2.startswith(k[0])and dato2.endswith(k[1]):
                    self.__queue.put(voce) 
                voce+=1
            if not self.__queue.empty():
                self.seek(self.__queue.get())
                return True
            else:
                return False


                            
    def  next(self): #prossima ricerca
        if not self.__queue.empty():
            self.seek(self.__queue.get())
            return True
        else:
            return False
