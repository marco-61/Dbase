from datetime import datetime, timedelta,date
from calendar import isleap
import math

class DateError(Exception):
    """ date Error"""
    pass

class Date:
    def __init__(self,anno, mese, giorno):
        self.anno,self.mese,self.giorno=anno,mese,giorno
        self.mg={1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
        l=["","Gennaio","Febbraio","Marzo","Aprile","Maggio","Giugno",
           "Luglio","Agosto","Settembre","Ottobre","Novembre""Dicembre"]
        if self.mese>12:
            raise DateError("Errore {} non è un valore accettabile per un mese".format(self.mese))
        self.g=self.mg[self.mese]
        if self.mese==2 and isleap(anno):
            self.g+=1
        if self.giorno>self.g:
            raise DateError("Errore {} non è un giorno accettabile per  mese di {}".format(giorno,l[self.mese]))
    def __str__(self):
        return "{:04d}-{:02d}-{:02d}".format(self.anno,self.mese,self.giorno)
    def  __repr__(self):     
        return "Date({},{},{})".format(self.anno,self.mese,self.giorno) 
    @property
    def dmy(self):
        return  "{:02d}-{:02d}-{:04d}".format(self.giorno,self.mese,self.anno)
    @property
    def mdy(self):
        return  "{:02d}-{:02d}-{:04d}".format(self.mese,self.giorno,self.anno)
    @property
    def ymd(self):
        return "{:04d}-{:02d}-{:02d}".format(self.anno,self.mese,self.giorno)
    @property
    def year(self):
        return self.anno
    @property
    def month(self):
        return self.mese
    @property
    def day(self):
        return self.giorno
    @classmethod
    def today(cls):
        oggi=date.today()
        return Date(oggi.year,oggi.month,oggi.day)
    @property
    def age(self):
        oggi=self.today
        if self > oggi:
            giorni=self-oggi # differenza in giorni
        else:   
            giorni=oggi-self # giorni totali dalla nascita
        anni=giorni//365 # anni 
        dg=giorni-(anni*365) #giorni restanti
        mesi=dg//30 # mesi restanti
        dg=dg-(mesi*30)
        settimane=dg//7
        resto_giorni=dg-(settimane*7)
        return (anni,mesi,settimane,resto_giorni)
    def day_split(self,giorni):
        anni=giorni//365 # anni 
        dg=giorni-(anni*365) # giorni restanti
        mesi=dg//30 # mesi restanti
        dg=dg-(mesi*30)
        settimane=dg//7
        resto_giorni=dg-(settimane*7)
        return (anni,mesi,settimane,resto_giorni)
    def __call__(self,anno, mese, giorno):
        self.__init__(anno, mese, giorno)
    def split(self,dt):
        l=dt.split("-")
        self.__call__(int(l[0]),int(l[1]),int(l[2]))
                          
    def add_days(self,giorni):
        r=Date(2019,11,15)
        b=timedelta(days=giorni)
        a=date(self.anno,self.mese,self.giorno)
        d=a+b
        r(d.year,d.month,d.day)
        return r
        
    def sub_days(self,giorni):
        r=Date(2019,11,15)
        b=timedelta(days=giorni)
        a=date(self.year,self.month,self.day)
        d=a-b
        r(d.year,d.month,d.day)
        return r

    def isleap(self,year):
        return isleap(year)
    
    def  __sub__(self,other):
        a=date(self.year,self.month,self.day)
        b=date(other.year,other.month,other.day)
        c=a-b # timedelta
        return c.days 
 
    def  __eq__(self, other):
        return self.ymd==other.ymd      
    def  __qe__(self, other):
        return self.ymd>=other.ymd
    def  __qt__(self, other):
        return self.ymd>other.ymd
    def  __le__(self, other):
        return self.ymd<=other.ymd
    def  __lt__(self, other):
        return self.ymd<other.ymd
    def  __ne__(self, other):
        return self.ymd!=other.ymd

