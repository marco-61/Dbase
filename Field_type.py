# crea campi della tabella
from abc import ABCMeta, abstractmethod
from dbase.Date import Date
from dbase.Shared import Shared
from dbase.dbs import dbs

class Field_type(metaclass=ABCMeta):
    
    def __init__(self):
        raise NotImplementedError
    @property
    @abstractmethod
    def value(self):
        # return self.value
        raise NotImplementedError
    def _cmp(self,vmin,vmax, v): #ritorna value se è nel range(vmin,vmax) altrimenti vmin o vmax
        if v<vmin:
            return vmin
        elif v>vmax:
            return vmax
        else:
            return v
    @value.setter
    @abstractmethod
    def value(self,value):
        raise NotImplementedError
    def  __eq__(self, value):
        return self.register_db[self.register_field]==value
    def  __qe__(self, value):
        return self.register_db[self.register_field]>=value
    def  __gt__(self, value):
        return self.register_db[self.register_field]>value
    def  __le__(self, value):
        return self.register_db[self.register_field]<=value
    def  __lt__(self, value):
        return self.register_db[self.register_field]<value
    def  __ne__(self, value):
        return self.register_db[self.register_field]!=value
    @abstractmethod
    def __str__():
        raise NotImplementedError
    @abstractmethod
    def __repr__():
        raise NotImplementedError
    def __call__(self,value):
        self.value=value
      
########################################################################    
class Field_int(Field_type): 
    def __init__(self,Range=None):
        """ register_db oggetto database
            Register_field campo del dbs a cui agganciarsi
            Range parametro 2 parametri(min, max)"""
        __Shared=Shared()
        self.__Range=Range
        self.register_db=__Shared.get_table()
        self.register_field=self.register_db.free_field()
        self.register_db[self.register_field]= f'Integer{Range}' if Range is not None else 'Integer' 

    @property
    def field(self):
        return self.register_field
    
    @property
    def field_Type(self):
        return 'Integer'

    property
    def dbs(self):
        return self.__db
    
    @property
    def value(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return 0 
        return self.register_db[self.register_field] 
    @value.setter
    def value(self, value):
         if isinstance(value,int):
             if self.__Range is not None:
                 self.register_db[self.register_field]=self._cmp(self.__Range[0],self.__Range[1],value)
             else:       
                 self.register_db[self.register_field]=value
         else:
             raise Exception('Tipo di dato errato solo <integer>')      
    def __str__(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return '0'   
        return str(self.register_db[self.register_field])
    def __repr__(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return repr(0)
        return repr(self.register_db[self.register_field])
####################################################################    
class Field_string(Field_type): 
    def __init__(self,size):
        self.__size=size
        __Shared=Shared()
        self.register_db=__Shared.get_table()
        self.register_field=self.register_db.free_field()
        self.register_db[self.register_field]= 'String({})'.format(self.__size)
        
    @property
    def field(self):
        return self.register_field
    
    @property
    def field_Type(self):
        return 'String'
    
    @property
    def dbs(self):
        return self.register_db
        
    @property
    def value(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return ""
        return self.register_db[self.register_field]
    @value.setter
    def value(self, value):
        if isinstance(value,str):
             if len(value) > self.__size:
                 c=value[:self.__size]
             else:
                 c=value
             self.register_db[self.register_field]=c
             return
        raise Exception('Tipo di dato errato solo <string>')

    def __str__(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return ""
        return (self.register_db[self.register_field])
    def __repr__(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return ""
        return repr(self.register_db[self.register_field])
####################################################################
class Field_complex(Field_type):
    
    def __init__(self,Range=None):
        """ register_db oggetto database
            Register_field campo del dbs a cui agganciarsi
            Range parametro opzionale se presente limita il campo numerico
            è una tupla di 2 parametri(min, max)"""
        __Shared=Shared()
        self.__Range=Range
        self.register_db=__Shared.get_table()
        self.register_field=self.register_db.free_field()
        self.register_db[self.register_field]= f'Complex{Range}' if Range is not None else 'Complex'


    @property
    def field(self):
        return self.register_field
    
    @property
    def field_Type(self):
        return 'Complex'

    @property
    def dbs(self):
        return self.register_db
        
    @property
    def value(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return 0.0j 
        return complex(self.register_db[self.register_field]) 
    @value.setter
    def value(self,value):
        if isinstance(value,complex):
            if self.__Range is not None:
                self.register_db[self.register_field]=str(self.__cmp_complex(value))
            else:
                self.register_db[self.register_field]=str(value)
        else:        
            raise Exception('Tipo di dato errato solo <complex>')
    def  __qe__(self, value): #ridifinisce i metodi di confronto
        val=self.value
        r=val.real >= value.real
        i=val.imag >= value.imag
        return (r and i)
    def  __gt__(self, value):
        val=self.value
        r= value.real < val.real
        i=value.imag < val.imag 
        return (r and i)
    def  __le__(self, value):
       val=self.value
       r=val.real <= value.real
       i=val.imag <= value.imag
       return (r and i)
    def  __lt__(self, value):
        val=self.value
        r=val.real < value.real
        i=val.imag < value.imag
        return (r and i)
    def  __eq__(self, value):
        val=self.value
        r=val.real == value.real
        i=val.imag == value.imag
        return (r and i)
    def  __ne__(self, value):
        return self.value != value
    def __str__(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return '0.0j'   
        return str(self.register_db[self.register_field])
    def __repr__(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return repr(0.0j)  
        return repr(self.register_db[self.register_field])
    #-----------------------------------------------------------#
    def __cmp_complex(self,value): #ritorna value se è nel range(min,max) altrimenti min o max
        if (value.real < self.__Range[0].real) and (value.imag < self.__Range[0].imag):
            return self.__Range[0]
        elif (value.real > self.__Range[0].real) and (value.imag > self.__Range[0].imag):
            return self.__Range[1]
        else: return value
####################################################################    
class Field_float(Field_type):
    
    def __init__(self,Range=None):
        """ register_db oggetto database
            Register_field campo del dbs a cui agganciarsi
            Range parametro opzionale se presente limita il campo numerico
            è una tupla di 2 parametri(min, max)"""
        __Shared=Shared()
        self.__Range=Range
        self.register_db=__Shared.get_table()
        self.register_field=self.register_db.free_field()
        self.register_db[self.register_field]= f'Float{Range}' if Range is not None else 'Float'
        
    @property
    def field(self):
        return self.register_field
    
    @property
    def field_Type(self):
        return 'Float'

    @property
    def dbs(self):
        return self.register_db
           
    @property
    def value(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return 0.0 
        return self.register_db[self.register_field]
       
    @value.setter
    def value(self,value):
        if isinstance(value,float):
            self.register_db[self.register_field]=self._cmp(self.__Range[0],self.__Range[1],value)
        else:
            raise Exception('Tipo di dato errato solo <float>')


    def __str__(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return '0.0'    
        return str(self.register_db[self.register_field])
    def __repr__(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return repr(0.0)
        return repr(self.register_db[self.register_field])
####################################################################
class Field_char(Field_type):
    def __init__(self,valid_char=None):
        """ register_db oggetto database
            Register_field campo del dbs a cui agganciarsi
            valid_char parametro opzionale se presente limita il campo di caratteri validi
            è una tupla di 2 parametri(valid, default) valid stringa con i caratteri validi"""
        self.size=1
        self.__valid_char=valid_char
        __Shared=Shared()
        self.register_db=__Shared.get_table()
        self.register_field=self.register_db.free_field()
        self.register_db[self.register_field]= 'Char'

    @property
    def field(self):
        return self.register_field
    
    @property
    def field_Type(self):
        return 'Char'

    @property
    def dbs(self):
        return self.register_db
    
    @property
    def value(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return "" if self.__valid_char is None else self.__valid_char(1) 
        return self.register_db[self.register_field]
    @value.setter
    def value(self,value):
        if isinstance(value,str):
            if len(value) > self.size: value=value[:1]
            if self.__valid_char is not None:
                if value in self.__valid_char[0]:
                    self.register_db[self.register_field]=value
                    return
                else:
                    self.register_db[self.register_field]=self.__valid_char[1]
                    return
            self.register_db[self.register_field]=value
            return
        raise Exception('Tipo di dato errato solo <char>')
   
    def __str__(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return ""          
        return self.register_db[self.register_field]
    def __repr__(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return ""    
        return repr(self.register_db[self.register_field])
################################################################    

class Field_bool(Field_type):
        
    def __init__(self):
        __Shared=Shared()
        self.register_db=__Shared.get_table()
        self.register_field=self.register_db.free_field()
        self.register_db[self.register_field]= 'Bool'

    @property
    def field(self):
        return self.register_field
    
    @property
    def field_Type(self):
        return 'Bool'

    @property
    def dbs(self):
        return self.register_db
    
    @property
    def value(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return False  
        return self.register_db[self.register_field]
    @value.setter
    def value(self,value):
        if isinstance(value,bool):
             self.register_db[self.register_field]=value
             return
        raise Exception('Tipo di dato errato solo <bool>')
    
    def __str__(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return 'False'    
        return str(self.register_db[self.register_field])
    def __repr__(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return repr(False)     
        return repr(self.register_db[self.register_field])
################################################################
        
class Field_list(Field_type):
    
    def __init__(self):
        __Shared=Shared()
        self.register_db=__Shared.get_table()
        self.register_field=self.register_db.free_field()
        self.register_db[self.register_field]= 'List'

    @property
    def field(self):
        return self.register_field
    
    @property
    def field_Type(self):
        return 'List'

    @property
    def dbs(self):
        return self.register_db
    
    @property
    def value(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return []
        return self.register_db[self.register_field]
    @value.setter
    def value(self, value):
         if isinstance(value,list):
             self.register_db[self.register_field]=value
             return
         raise Exception('Tipo di dato errato solo <list>')
    def __str__(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return str([])
        return str(self.register_db[self.register_field])
    def __repr__(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return repr([])
        return repr(self.register_db[self.register_field])
################################################################
        
class Field_tuple(Field_type):
    
    def __init__(self):
        __Shared=Shared()
        self.register_db=__Shared.get_table()
        self.register_field=self.register_db.free_field()
        self.register_db[self.register_field]= 'Tuple'

    @property
    def field(self):
        return self.register_field
    
    @property
    def field_Type(self):
        return 'Tuple'

    @property
    def dbs(self):
        return self.register_db
    
    @property
    def value(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return ()   
        return self.register_db[self.register_field]
    @value.setter
    def value(self, value):
         if isinstance(value,tuple):
             self.register_db[self.register_field]=value
             return
         raise Exception('Tipo di dato errato solo <tuple>')
    def __str__(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return str(())
        return str(self.register_db[self.register_field])
    def __repr__(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return repr(())   
        return repr(self.register_db[self.register_field])
################################################################
        
class Field_set(Field_type): # l'oggetto set non è supportato dal formato json
    # viene trasformato in modo trasparente in list e in set
    def __init__(self):
        __Shared=Shared()
        self.register_db=__Shared.get_table()
        self.register_field=self.register_db.free_field()
        self.register_db[self.register_field]= 'Set'

    @property
    def field(self):
        return self.register_field
    
    @property
    def field_Type(self):
        return 'Set'

    @property
    def dbs(self):
        return self.register_db
    
    @property
    def value(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return set() 
        return set(self.register_db[self.register_field])
    @value.setter
    def  value(self, value):
        if isinstance(value,set):
            l=list(value)
            self.register_db[self.register_field]=l
            return
        raise Exception('Tipo di dato errato solo <set>')
    def __str__(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return str(set())
        return str(set(self.register_db[self.register_field]))
    def __repr__(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return repr(set()) 
        return repr(set(self.register_db[self.register_field]))
###################################################################    
class Field_dict(Field_type):
    
    def __init__(self):
        __Shared=Shared()
        self.register_db=__Shared.get_table()
        self.register_field=self.register_db.free_field()
        self.register_db[self.register_field]= 'Dict'
    @property
    def field(self):
        return self.register_field
    
    @property
    def field_Type(self):
        return 'Dict'

    @property
    def dbs(self):
        return self.register_db
    
    @property
    def value(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return {} 
        return self.register_db[self.register_field]
    @value.setter
    def value(self, value):
        if isinstance(value,dict):
            self.register_db[self.register_field]=value
            return
        raise Exception('Tipo di dato errato solo <dict>')
    def __str__(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return str({}) 
        return str(self.register_db[self.register_field])
    def __repr__(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return repr({}) 
        return repr(self.register_db[self.register_field])
 ############################################################################       
class Field_date(Field_type): # l'oggetto set non è supportato dal formato json
    # viene trasformato in modo trasparente in stringa e in date
    def __init__(self):
        __Shared=Shared()
        self.register_db=__Shared.get_table()
        self.register_field=self.register_db.free_field()
        self.register_db[self.register_field]= 'Date'
        self.__today=Date.today()
        
    @property
    def field(self):
        return self.register_field
    
    @property
    def field_Type(self):
        return 'Date'

    @property
    def dbs(self):
        return self.register_db
    
    @property
    def value(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return self.__today
        r=Date.today()
        r.split(self.register_db[self.register_field])
        return r
    @value.setter
    def value(self, value):
        r=Date.today()
        if isinstance(value,Date):
            self.register_db[self.register_field]=value.ymd
            return
        raise Exception('Tipo di dato errato solo <Date>')
    def __str__(self):
        r=self.__today
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return str(r)
        return str(self.register_db[self.register_field])
    def __repr__(self):
        r=Date.today()
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return repr(r)
        return repr(r.split(self.register_db[self.register_field]))
############################################################################         
class Field_text(Field_type):
    def __init__(self):
        __Shared=Shared()
        self.register_db=__Shared.get_table()
        self.register_field=self.register_db.free_field()
        self.register_db[self.register_field]= 'Text'        
    @property
    def field(self):
        return self.register_field
    @property
    def field_Type(self):
        return 'Text'

    @property
    def dbs(self):
        return self.register_db
    
    @property
    def value(self):
        if self.register_db[self.register_field] is None:
            self.register_db[self.register_field]=""    
        return self.register_db[self.register_field]
    
    @value.setter
    def value(self, value):    
        if isinstance(value,str):
            self.register_db[self.register_field]=value
            return
        raise Exception('Tipo di dato errato solo <string>')    
    def __str__(self):
        if self.register_db[self.register_field] is None:
            return ""    
        return self.register_db[self.register_field]
    def __repr__(self):
        if self.register_db[self.register_field] is None:
            return""    
        return repr(self.register_db[self.register_field])
    
##############################################################################
class Field_set_of(Field_type): 
    def __init__(self,valid):
        """ register_db oggetto database
            Register_field campo del dbs a cui agganciarsi
            valid set di valori validi"""
        __Shared=Shared()
        if isinstance(valid,set):
            self.__valid=valid
        elif isinstance(valid,(list,tuple)):
            self.__valid=set(valid)            
        else:
            raise('valid is not set')            
        self.register_db=__Shared.get_table()
        self.register_field=self.register_db.free_field()
        self.register_db[self.register_field]= f'Set_of{valid}'

    @property
    def field(self):
        return self.register_field
    
    @property
    def field_Type(self):
        return 'Set_of' 

    property
    def dbs(self):
        return self.__db
    
    @property
    def value(self):
        if self.register_db[self.register_field] is None: raise('value is not defined')
                   
        return self.register_db[self.register_field] 
    @value.setter
    def value(self, value):
        if value in self.__valid:
            self.register_db[self.register_field]=value
        else:    
            raise Exception('value is not in set_of range')
        
        return self.register_db[self.register_field]!=value
    def __str__(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            raise('value is not defined')
        return str(self.register_db[self.register_field])
    def __repr__(self):
        if self.register_db[self.register_field] is None:
            # ritorna un valore di default se il campo è nullo 
            return repr(0)
        return repr(self.register_db[self.register_field])

