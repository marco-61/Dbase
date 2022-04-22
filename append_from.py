def append_from(sfields:list,dfields:list,Filter=None):
    db1=sfields[0].dbs # tabelle di riferimento
    db2=dfields[0].dbs
    pos=db1.tell()
    db1.seek_to_start()
    
    def sub_Call():#sotto funzione
        nonlocal db1,db2,sfields,dfields
        db2.append_blank()
        for i,f in enumerate(sfields):
            dfields[i].value=f.value
            
    while not db1.eof(): # cicla su tutta la tabella    
        if Filter is not None:#se callback è presente
            if Filter(sfields): #ritorna True se campi è validi
                sub_Call()
        else: #senza callback
            sub_Call()
        next(db1)#Prossimo record
        
    db1.seek(pos) # ripristina il puntatore    
        
