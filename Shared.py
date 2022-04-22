from dbase.dbs import dbs

class Shared:
    """ classe condivisa"""
    _stato={}
    
    def __init__(self):
        """ Singleton una sola istanza """
        self.__dict__=self._stato 
    
    def set_table(self, table):
        """ relaziona una tabella ad un oggetto dbs """
        if '.' in table:
            t=table.split('.')
            self.__dict__[t[0]]=dbs("{}.{}".format(t[0],t[1]))
        else:
            self.__dict__[table]=dbs(table+'.tab')
                               
    def get_table(self, table=None):
        """ ritorna un oggetto dbs """                             
        if table:
            return self.__dict__[table]
        t=self.__dict__['use_table']
        return self.__dict__[t]
                                    
    def set_use_table(self,table):
        """ setta tabella in uso """                            
        self.__dict__['use_table']=table
                                    
    def get_use_table(self):
         """ ritorna tabella in uso """  
         return self.__dict__['use_table']
                                    
    def __getitem__(self,key):
        """ ritorna il valore della chiave """
        return self.__dict__[key]
    
    def __setitem__(self, key, value):
        """ ritorna setta la chiave """
        self.__dict__[key]=value
        
    def __delitem__(self, key):
        """ cancella la chiave """
        del(self.__dict__[key])
        
    def keys(self):
        """ritorna le chiavi del dizionario"""
        return self.__dict__.keys()
    
    def values(self):
        """ritorna i valori del dizionario"""
        return self.__dict__.values()
    def items(self):
        """ritorna le chiavi e valori del dizionario"""
        return self.__dict__.items()
    
    def __len__ (self):
        """ritorna il numero delle chiavi"""
        return len(self.__dict__)
    def __contains__(self, key):
        """operatore in """
        return key in self.__dict__
    
