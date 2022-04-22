import dbase.dbs
from dbase.Date import date
from dbase.Shared import Shared
from abc import ABCMeta, abstractmethod

class Table(metaclass=ABCMeta):
    def __init__(self, tabname):
        """
        Classe   : Table crea tabelle del database
        """
        self.__Shared=Shared() # classe condivisa
        self.__Shared.set_table(tabname) # Crea oggeto database associato alla tabella
        self.__Shared.set_use_table(tabname) # tabella attuale è quella in uso
        self.__db=self.__Shared.get_table() # ricupera l'oggetto database
        self.__db.append_blank()  #prepara per il record dei campi

    @property
    def dbs(self): # ritorna il dbs
        return self.__db
    
    # link ai metodi del database    
    def seek(self,record):
        self.__db.seek(record)

    def tell(self):
        return self.__db.tell()
    
    def seek_to_start(self):
        self.__db.seek_to_start()
        
    def seek_to_end(self):
        self.__db.seek_to_end()
        
    def __iter__(self):
        self.seek_to_start()
        while not self.eof():
            yield self.tell()
            next(self)      
    def __next__(self):
        next(self.__db)
    def eof(self):
        return self.__db.eof()
    
    def erase(self,record=0):
        self.__db.record(record)
        
    def flush(self,name=""):
        self.__db.flush(name)
    def __len__(self):
        return len(self.__db)
    
    def append_blank(self):
        """Crea un campo vuoto"""
        self.__db.append_blank()
        
    def use(self,name=""):    
        return self.__db.use(name)
          
    def dbCreate(self,filename=""):
        self.__db.dbCreate(filename)
        
    def sort(self,field):
        """ordina la tabella in ordine ascendente secondo il campo"""
        f=field.field # campo della tabella
        self.__db.sort(f)
   
    def search(self, choise, field):
        """
        semplice ricerca sequenziale ritorna True record trovato altrimenti False
        usare self.next per posizionare i records, la chiave puo essere anche parziale 3 casi:
        *no po* st*o
        """
        return self.__db.search(choise,field.field)
    def next(self):
        return self.__db.next()
    def __delitem__(self, record):
        del self.__db[record]
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        pass
    def __repr__(self):
        raise NotImplementedError()
    def __str__(self):
        raise NotImplementedError()  
