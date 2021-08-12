from tkinter import *
import time
import sqlite3
import random
import tempfile
import win32api
import win32print

f=''
flag=''
flags=''

login=sqlite3.connect("admin.db")
l=login.cursor()

c=sqlite3.connect("medicine.db")
cur=c.cursor()

columns=('Sl No', 'Nom', 'Type', 'Quantite', 'Prix', 'Indication', 'Date Expiration', 'Rang', 'Fabricant')

def open_win(): #OUVRE MENU ----------------------------------------------------------------------------MENU PRINCIPAL
    global apt, flag
    flag='apt'
    apt=Tk()
    apt.title("Menu Principale")
    Label(apt, text=".Py pharma").grid(row=0,column=0,columnspan=3)
    Label(apt, text='*'*80).grid(row=1,column=0,columnspan=3)
    Label(apt, text='-'*80).grid(row=3,column=0,columnspan=3) 

    Label(apt, text="Maintenance De Stock").grid(row=2,column=0)
    Button(apt,text='Nouveau V.C.', width=25, command=val_cus).grid(row=4,column=0)
    Button(apt,text='Ajouter un produit', width=25,command=stock).grid(row=5,column=0)
    Button(apt,text='Supprimer un produit', width=25,command=delete_stock).grid(row=6,column=0)
    

    Label(apt, text="Accès au stock").grid(row=2,column=1)
    Button(apt,text='Modifier',width=15, command=modify).grid(row=4,column=1)
    Button(apt,text='Chercher', width=15, command=search).grid(row=5,column=1)
    Button(apt,text='Verifier expiration', width=15, command=exp_date).grid(row=6,column=1)

    Label(apt, text="gérer l'argent").grid(row=2,column=2)
    Button(apt,text="Revenue D'aujordhuit", width=20,command=show_rev).grid(row=5,column=2)
    Button(apt,text='Facturation', width=20, command=billing).grid(row=4,column=2)

    Label(apt, text='-'*80).grid(row=12,column=0,columnspan=3)    
    Button(apt,text='Deconnecter',command=again).grid(row=13, column=2)
    apt.mainloop()

def delete_stock(): #OPENS DELETE WINDOW----------------------------------------------------DELETES A PARTICULAR STOCK ITEM
    global cur, c, flag, lb1, d
    apt.destroy()
    flag='d'
    d=Tk()
    d.title("Supprimer un produit Du Stock")
    Label(d,text='Entrer le Product a Supprimer:').grid(row=0,column=0)
    Label(d,text='',width=30,bg='white').grid(row=0,column=1)
    Label(d,text='Produit').grid(row=2,column=0)
    Label(d,text='Qtt.       Exp.dt.         Prix              ').grid(row=2,column=1)
    ren()
    b=Button(d,width=20,text='Supprimer',command=delt).grid(row=0,column=3)
    b=Button(d,width=20,text='Menu Principale',command=main_menu).grid(row=5,column=3)
    d.mainloop()

def ren():
    global lb1,d,cur,c
    def onvsb(*args):
        lb1.yview(*args)
        lb2.yview(*args)
    def onmousewheel():
        lb1.ywiew=('scroll',event.delta,'units')
        lb2.ywiew=('scroll',event.delta,'units')
        return 'break'
    cx=0
    vsb=Scrollbar(orient='vertical',command=onvsb)
    lb1=Listbox(d,width=25, yscrollcommand=vsb.set)
    lb2=Listbox(d,width=30,yscrollcommand=vsb.set)
    vsb.grid(row=3,column=2,sticky=N+S)
    lb1.grid(row=3,column=0)
    lb2.grid(row=3,column=1)
    lb1.bind('<MouseWheel>',onmousewheel)
    lb2.bind('<MouseWheel>',onmousewheel)
    cur.execute("select *from med")
    for i in cur:
        cx+=1
        s1=[str(i[0]),str(i[1])]
        s2=[str(i[3]),str(i[6]),str(i[4])]
        lb1.insert(cx,'. '.join(s1))
        lb2.insert(cx,'   '.join(s2))
    c.commit()
    lb1.bind('<<ListboxSelect>>', sel_del)

def sel_del(e):
    global lb1, d, cur, c,p, sl2
    p=lb1.curselection()
    print (p)
    x=0
    sl2=''
    cur.execute("select * from med")
    for i in cur:
        print (x, p[0])
        if x==int(p[0]):
            sl2=i[0]
            break
        x+=1
    c.commit()
    print (sl2)
    Label(d,text=' ',bg='white', width=20).grid(row=0,column=1)
    cur.execute('Select * from med')
    for i in cur:
        if i[0]==sl2:
            Label(d,text=i[0]+'. '+i[1],bg='white').grid(row=0,column=1)
    c.commit()
    
def delt():
    global p,c,cur,d
    cur.execute("delete from med where sl_no=?",(sl2,))
    c.commit()
    ren()

def modify():    # page de modification-----------------------------------------------------------------------MODIFIER
    global cur, c, accept, flag, att, up, n, name_, apt, st, col,col_n
    col=('', '', 'type', 'qty_left', 'cost', 'purpose', 'expdt', 'loc', 'mfg')
    col_n=('', '', 'Type', 'Quantite', 'prix', 'symptomes', 'Date Expiration', 'Rang', 'Fabricant')
    flag='st'
    name_=''
    apt.destroy()
    n=[]
    cur.execute("select * from med")
    for i in cur:
        n.append(i[1])
    c.commit()
    st=Tk()
    st.title('MODIFIER')
    Label(st, text='-'*48+' MODIFIER LA BASE DE DONNE'+'-'*48).grid(row=0, column=0,columnspan=6)
    def onvsb(*args):
        name_.yview(*args)
    def onmousewheel():
        name_.ywiew=('scroll',event.delta,'units')
        return 'break'
    cx=0
    vsb=Scrollbar(orient='vertical',command=onvsb)
    vsb.grid(row=1,column=3,sticky=N+S)
    name_=Listbox(st,width=43,yscrollcommand=vsb.set)
    cur.execute("select *from med")
    for i in cur:
        cx+=1
        name_.insert(cx,(str(i[0])+'.  '+str(i[1])))
        name_.grid(row=1,column=1,columnspan=2)
    c.commit()
    name_.bind('<MouseWheel>',onmousewheel)
    name_.bind('<<ListboxSelect>>', sel_mn)

    Label(st, text='Cliquer sur le Medicament: ').grid(row=1, column=0)
    Label(st, text='Entrer la Valeur a Changer').grid(row=2, column=0)
    att=Spinbox(st, values=col_n)
    att.grid(row=2, column=1)
    up=Entry(st)
    up.grid(row=2, column=2)
    Button(st,width=10,text='Soumettre', command=save_mod).grid(row=2, column=4)
    Button(st,width=10,text='Reinitialiser', command=res).grid(row=2, column=5)
    Button(st,width=15,text='Afficher les données', command=show_val).grid(row=1, column=4)
    Label(st, text='-'*120).grid(row=3,column=0,columnspan=6)
    Button(st,width=12,text='Menu Principale',command=main_menu).grid(row=5,column=5)
    st.mainloop()

def res():
    global st, up
    up=Entry(st)
    up.grid(row=2, column=2)
    Label(st,width=20, text='                         ').grid(row=5,column=i)

def sel_mn(e):
    global n,name_, name_mn, sl, c, cur
    name_mn=''
    p=name_.curselection()
    print (p)
    x=0
    sl=''
    cur.execute("select * from med")
    for i in cur:
        print (x, p[0])
        if x==int(p[0]):
            sl=i[0]
            break
        x+=1
    c.commit()
    print (sl)
    name_nm=n[int(sl)]
    print (name_nm)
    
def show_val():
    global st, name_mn, att, cur, c, col, col_n, sl
    for i in range(3):
        Label(st,width=20, text='                         ').grid(row=5,column=i)
    cur.execute("select * from med")
    for i in cur:
        for j in range(9):
            if att.get()==col_n[j] and sl==i[0]:
                Label(st, text=str(i[0])).grid(row=5,column=0)
                Label(st, text=str(i[1])).grid(row=5,column=1)
                Label(st, text=str(i[j])).grid(row=5,column=2)
    c.commit()

def save_mod(): #enregistrer les donnees changees
    global cur, c, att, name_mn, st, up, col_n, sl
    for i in range(9):
        if att.get()==col_n[i]:
            a=col[i]
    sql="update med set '%s' = '%s' where sl_no = '%s'" % (a,up.get(),sl)
    cur.execute(sql)
    c.commit()
    Label(st, text='ok!').grid(row=5,column=4)
    
    
def stock():    #page ajout au stock------------------------------------------------------------------------AJOUTER DANS LE STOCK
    global cur, c, columns, accept, flag, sto, apt
    apt.destroy()
    flag='sto'
    accept=['']*10
    sto=Tk()
    sto.title('Ajouter un Produit au sStock')
    Label(sto,text='ENTRER LES DONNEÉS DU NOUVEAU PRODUIT').grid(row=0,column=0,columnspan=2)
    Label(sto,text='-'*50).grid(row=1,column=0,columnspan=2)
    for i in range(1,len(columns)):
        Label(sto,width=15,text=' '*(14-len(str(columns[i])))+str(columns[i])+':').grid(row=i+2,column=0)
        accept[i]=Entry(sto)
        accept[i].grid(row=i+2, column=1)
    Button(sto,width=15,text='Soumettre',command=submit).grid(row=12,column=1)
    Label(sto,text='-'*165).grid(row=13,column=0,columnspan=7)
    Button(sto,width=15,text='Reinitialiser',command=reset).grid(row=12,column=0)
    Button(sto,width=15,text='Actualiser le stock',command=ref).grid(row=12,column=4)
    for i in range(1,6):
        Label(sto,text=columns[i]).grid(row=14,column=i-1)
    Label(sto,text='Exp           Rang   Fabricant                      ').grid(row=14,column=5)
    Button(sto,width=12,text='Menu Principale',command=main_menu).grid(row=12,column=5)
    ref()
    sto.mainloop()

def ref(): # creer multi-listbox manuel pour afficher tout la base de donnees
    global sto, c, cur
    def onvsb(*args):
        lb1.yview(*args)
        lb2.yview(*args)
        lb3.yview(*args)
        lb4.yview(*args)
        lb5.yview(*args)
        lb6.yview(*args)

    def onmousewheel():
        lb1.ywiew=('scroll',event.delta,'units')
        lb2.ywiew=('scroll',event.delta,'units')
        lb3.ywiew=('scroll',event.delta,'units')
        lb4.ywiew=('scroll',event.delta,'units')
        lb5.ywiew=('scroll',event.delta,'units')
        lb6.ywiew=('scroll',event.delta,'units')
        
        return 'break'
    cx=0
    vsb=Scrollbar(orient='vertical',command=onvsb)
    lb1=Listbox(sto,yscrollcommand=vsb.set)
    lb2=Listbox(sto,yscrollcommand=vsb.set)
    lb3=Listbox(sto,yscrollcommand=vsb.set,width=10)
    lb4=Listbox(sto,yscrollcommand=vsb.set,width=7)
    lb5=Listbox(sto,yscrollcommand=vsb.set,width=25)
    lb6=Listbox(sto,yscrollcommand=vsb.set,width=37)
    vsb.grid(row=15,column=6,sticky=N+S)
    lb1.grid(row=15,column=0)
    lb2.grid(row=15,column=1)
    lb3.grid(row=15,column=2)
    lb4.grid(row=15,column=3)
    lb5.grid(row=15,column=4)
    lb6.grid(row=15,column=5)
    lb1.bind('<MouseWheel>',onmousewheel)
    lb2.bind('<MouseWheel>',onmousewheel)
    lb3.bind('<MouseWheel>',onmousewheel)
    lb4.bind('<MouseWheel>',onmousewheel)
    lb5.bind('<MouseWheel>',onmousewheel)
    lb6.bind('<MouseWheel>',onmousewheel)
    cur.execute("select *from med")
    for i in cur:
        cx+=1
        seq=(str(i[0]),str(i[1]))
        lb1.insert(cx,'. '.join(seq))
        lb2.insert(cx,i[2])
        lb3.insert(cx,i[3])
        lb4.insert(cx,i[4])
        lb5.insert(cx,i[5])
        lb6.insert(cx,i[6]+'    '+i[7]+'    '+i[8])
    c.commit()

def reset():
    global sto, accept
    for i in range(1,len(columns)):
        Label(sto,width=15,text=' '*(14-len(str(columns[i])))+str(columns[i])+':').grid(row=i+2,column=0)
        accept[i]=Entry(sto)
        accept[i].grid(row=i+2, column=1)
    
def submit(): #pour submission de nouvelle entre de stock
    global accept, c, cur, columns, sto
    prev=time.clock()
    x=['']*10
    cur.execute("select * from med")
    for i in cur:
        y=int(i[0])
    for i in range(1,9):
        x[i]=accept[i].get()
    sql="insert into med values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (y+1,x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8])
    cur.execute(sql)
    cur.execute("select * from med")
    c.commit()
    now=time.clock()
    print (now-prev)
    top=Tk()
    Label(top,width=20, text='Succès!').pack()
    top.mainloop()
    main_menu()

def chk(): # verifier si le medicament entre exist deja dan la base avant de modifier
    global cur, c, accept, sto
    cur.execute("select * from med")
    for i in cur:
        if accept[6].get()==i[6] and i[1]==accept[1].get():
            sql="update med set qty_left = '%s' where name = '%s'" % (str(int(i[3])+int(accept[3].get())),accept[1].get())
            cur.execute(sql)
            c.commit()
            top=Tk()
            Label(top,width=20, text='ok!').pack()
            top.mainloop()
            main_menu()
        else:
            submit()
    c.commit()

def exp_date(): # ouvrire page d expiration -----------------------------------------------------------------------------expiration
    global exp, s,c, cur, flag, apt, flags
    apt.destroy()
    flag='exp'
    from datetime import date
    now=time.localtime()
    n=[]
    cur.execute("select *from med")
    for i in cur:
        n.append(i[1])
    c.commit()
    exp=Tk()
    exp.title("verifier date d'expiration")
    Label(exp,text='Aujordhuit : '+str(now[2])+'/'+str(now[1])+'/'+str(now[0])).grid(row=0, column=0, columnspan=3)
    Label(exp,text='Vendre des Medicaments Expirés est illegal').grid(row=1, column=0,columnspan=3)
    Label(exp,text='-'*80).grid(row=2, column=0,columnspan=3)
    s=Spinbox(exp,values=n)
    s.grid(row=3, column=0)
    Button(exp,text="verifier date d'expiration", command=s_exp).grid(row=3, column=1)
    Label(exp,text='-'*80).grid(row=4, column=0,columnspan=3)
    if flags=='apt1':
        Button(exp,text='Menu Principale', command=main_cus).grid(row=5, column=2)
    else:
        Button(exp,width=20,text="verifier tout le Stock", command=exp_dt).grid(row=5, column=0)
        Button(exp,text='Menu Principale', command=main_menu).grid(row=5, column=2)
    exp.mainloop()

def s_exp():    # affiche la date dexpiration d un medicament entree
    global c, cur, s, exp, top
    from datetime import date
    now=time.localtime()
    d1 = date(now[0],now[1],now[2])
    cur.execute("select * from med")
    for i in cur:
        if(i[1]==s.get()):
            q=i[6]
            d2=date(int('20'+q[8:10]),int(q[3:5]),int(q[0:2]))
            if d1>d2:
                Label(exp, text='EXPIRÉ! le '+i[6]).grid(row=3, column=2)
                top=Tk()
                Label(top, text='EXPIRÉ!').pack()
            else:
                Label(exp, text=i[6]).grid(row=3, column=2)
    c.commit()

def exp_dt(): # affiche les medicament qui expirera la semaine prochaine(dans une semaine)
    global c, cur, exp, top
    x=0
    z=1
    from datetime import datetime, timedelta 
    N = 7
    dt = datetime.now() + timedelta(days=N)
    d=str(dt)
    from datetime import date
    now=time.localtime()
    d1 = date(now[0],now[1],now[2])
    d3 = date(int(d[0:4]),int(d[5:7]),int(d[8:10]))
    Label(exp,text='S.No'+'   '+'Nom'+'     Qtt.    '+'Exp_date').grid(row=6,column=0,columnspan=2)
    cur.execute("select * from med")
    for i in cur:
        s=i[6]
        d2=date(int('20'+s[8:10]),int(s[3:5]),int(s[0:2]))
        
        if d1<d2<d3:
            Label(exp,text=str(z)+'.      '+str(i[1])+'    '+str(i[3])+'    '+str(i[6])).grid(row=x+7,column=0,columnspan=2)
            x+=1
            z+=1
        elif d1>d2:
            top=Tk()
            Label(top,width=20, text=str(i[1])+' EST EXPIRÉ!').pack()
    c.commit()
    
def billing(): # cree une facture pour un client -------------------------------------------------------------system facturation
    global c, cur, apt, flag, t, name, name1, add, st, names, qty, sl, qtys, vc_id, n, namee, lb1
    t=0
    vc_id=''
    names=[]
    qty=[]
    sl=[]
    n=[]
    qtys=['']*10
    cur.execute("select *from med")
    for i in cur:
        n.append(i[1])
    c.commit()
    if flag=='st':
        st.destroy()
    else:
        apt.destroy()
    flag='st'
    st=Tk()
    st.title('SYSTEM FACTURATION')
    Label(st,text='-'*48+'SYSTEM FACTURATION'+'-'*49).grid(row=0,column=0,columnspan=7)
    Label(st,text='Entrer Nom: ').grid(row=1,column=0)
    name1=Entry(st)
    name1.grid(row=1, column=1)
    Label(st,text='Entrer Address: ').grid(row=2,column=0)
    add=Entry(st)
    add.grid(row=2, column=1)
    Label(st,text="Valeur Id (si disponible)").grid(row=3, column=0)
    vc_id=Entry(st)
    vc_id.grid(row=3, column=1)
    Button(st,text='verifier V.C.', command=blue).grid(row=4, column=0)
    Label(st,text='-'*115).grid(row=6, column=0,columnspan=7)
    Label(st,text='SELECTION PRODUIT',width=25,relief='ridge').grid(row=7, column=0)
    Label(st,text=' RANG  QTT     COUT          ',width=25,relief='ridge').grid(row=7, column=1)
    Button(st,text='Ajout a la facture',width=15,command=append2bill).grid(row=8, column=6)
    Label(st,text='QUANTITÉ',width=20,relief='ridge').grid(row=7, column=5)
    qtys=Entry(st)
    qtys.grid(row=8,column=5)
    refresh()
    Button(st,width=15,text='Menu Principale', command=main_menu).grid(row=1,column=6)
    Button(st,width=15,text='Actualiser le Stock', command=refresh).grid(row=3,column=6)
    Button(st,width=15,text='Reinitialiser facture', command=billing).grid(row=4,column=6)
    Button(st,width=15,text='Imprimer facture', command=print_bill).grid(row=5,column=6)
    Button(st,width=15,text='Enreg Facture', command=make_bill).grid(row=7,column=6)
    
    st.mainloop()

def refresh():
    global cur, c, st, lb1, lb2, vsb
    def onvsb(*args):
        lb1.yview(*args)
        lb2.yview(*args)

    def onmousewheel():
        lb1.ywiew=('scroll',event.delta,'units')
        lb2.ywiew=('scroll',event.delta,'units')
        return 'break'
    cx=0
    vsb=Scrollbar(orient='vertical',command=onvsb)
    lb1=Listbox(st,width=25, yscrollcommand=vsb.set)
    lb2=Listbox(st ,width=25,yscrollcommand=vsb.set)
    vsb.grid(row=8,column=2,sticky=N+S)
    lb1.grid(row=8,column=0)
    lb2.grid(row=8,column=1)
    lb1.bind('<MouseWheel>',onmousewheel)
    lb2.bind('<MouseWheel>',onmousewheel)
    cur.execute("select *from med")
    for i in cur:
        cx+=1
        lb1.insert(cx,str(i[0])+'. '+str(i[1]))
        lb2.insert(cx,' '+str(i[7])+'        '+str(i[3])+'             MRU '+str(i[4]))
    c.commit()
    lb1.bind('<<ListboxSelect>>', select_mn)

def select_mn(e): #enregistre le medicament selectionee dans listbox
    global st, lb1, n ,p, nm, sl1
    p=lb1.curselection()
    x=0
    sl1=''
    from datetime import date
    now=time.localtime()
    d1 = date(now[0],now[1],now[2])
    cur.execute("select * from med")
    for i in cur:
        if x==int(p[0]):
            sl1=int(i[0])
            break
        x+=1    
    c.commit()
    print (sl1)
    nm=n[x]
    print (nm)
    
def append2bill(): # ajouter a la facture
    global st, names, nm , qty, sl,cur, c, sl1
    sl.append(sl1)
    names.append(nm)
    qty.append(qtys.get())
    print (qty)
    print (sl[len(sl)-1],names[len(names)-1],qty[len(qty)-1])
    
def blue(): # verifier valeur id de client 
    global st ,c, cur, named, addd, t, vc_id
    cur.execute("select * from util")
    for i in cur:
        if vc_id.get()!='' and int(vc_id.get())==i[2]:
            named=i[0]
            addd=i[1]
            Label(st,text=named,width=20).grid(row=1, column=1)
            Label(st,text=addd,width=20).grid(row=2, column=1)
            Label(st,text=i[2],width=20).grid(row=3, column=1)
            Label(st, text='Client Reconnue!').grid(row=4, column=1)
            t=1
            break
    c.commit()

def make_bill(): # faire facture
    global t, c, B, cur, st, names, qty, sl , named, addd, name1, add,det, vc_id
    price=[0.0]*10
    q=0
    det=['','','','','','','','']
    det[2]=str(sl)
    for i in range(len(sl)):
        print (sl[i],' ',qty[i],' ',names[i])
    for k in range(len(sl)):
        cur.execute("select * from med where sl_no=?",(sl[k],))
        for i in cur:
            price[k]=int(qty[k])*float(i[4])
            print (qty[k],price[k])
            cur.execute("update med set qty_left=? where sl_no=?",(int(i[3])-int(qty[k]),sl[k]))
        c.commit()
    det[5]=str(random.randint(100,999))
    B='fact_'+str(det[5])+'.txt'
    total=0.00
    for i in range(10):
        if price[i] != '':
            total+=price[i] #totalling
    m='\n\n\n'
    m+="===============================================\n"
    m+="                                  No :%s\n\n" % det[5]
    m+="                 .PY PHARMA \n"
    m+="       UNIVERSITE DE NOUAKCHOTT AL'ASRYA\n\n"
    m+="-----------------------------------------------\n"
    if t==1:
        m+="Name: %s\n" % named
        m+="Address: %s\n" % addd
        det[0]=named
        det[1]=addd
        cur.execute('select * from util')
        for i in cur:
            if i[0]==named:
                det[7]=i[2]
    else:
        m+="Nom: %s\n" % name1.get()
        m+="Address: %s\n" % add.get()
        det[0]=name1.get()
        det[1]=add.get()
    m+="-----------------------------------------------\n"
    m+="Produit                      Qtt.       Prix\n"
    m+="-----------------------------------------------\n"#47, qty=27, price=8 after 2
    for i in range(len(sl)):
        if names[i] != 'nil':
            s1=' '
            s1=(names[i]) + (s1 * (27-len(names[i]))) + s1*(3-len(qty[i])) +qty[i]+ s1*(15-len(str(price[i])))+str(price[i]) + '\n'
            m+=s1
    m+="\n-----------------------------------------------\n"
    if t==1:
        ntotal=total*0.8
        m+='Total'+(' '*24)+(' '*(15-len(str(total)))) + str(total)+'\n'
        m+="Valeur de remise "+ (' '*(20-len(str(total-ntotal))))+'-'+str(total-ntotal)+'\n'
        m+="-----------------------------------------------\n"
        m+='Total'+(' '*24)+(' '*(12-len(str(ntotal)))) +'MRU '+ str(ntotal)+'\n'
        det[3]=str(ntotal)
    else:
        m+='Total'+(' '*24)+(' '*(12-len(str(total)))) +'MRU '+ str(total)+'\n'
        det[3]=str(total)
        
    m+="-----------------------------------------------\n\n"
    m+=" signature Du Vendeur:__________________________\n"
    m+="===============================================\n"
    print (m)
    p=time.localtime()
    det[4]=str(p[2])+'/'+str(p[1])+'/'+str(p[0])
    det[6]=m
    bill=open(B,'w')
    bill.write(m)
    bill.close()
    cb=('cus_name','cus_add','items','Total_cost','bill_dt','bill_no','bill','val_id')
    cur.execute('insert into fact values(?,?,?,?,?,?,?,?)',(det[0],det[1],det[2],det[3],det[4],det[5],det[6],det[7]))
    c.commit()
    
def print_bill():
    win32api.ShellExecute (0,"print",B,'/d:"%s"' % win32print.GetDefaultPrinter (),".",0)
    
def show_rev(): # ouvre page de revenue ----------------------------------------------------------------------- TOTAL REVENUE
    global c, cur, flag,rev
    apt.destroy()
    cb=('cus_name','cus_add','items','Total_cost','bill_dt','bill_no','bill','val_id')
    flag='rev'
    rev=Tk()
    rev.title("REVENUE D'AUJORDHUIT")
    total=0.0
    today=str(time.localtime()[2])+'/'+str(time.localtime()[1])+'/'+str(time.localtime()[0])
    Label(rev,text='Aujordhuit: '+today).grid(row=0,column=0)
    cur.execute('select * from fact')
    for i in cur:
        if i[4]==today:
            total+=float(i[3])
    print (total)
    Label(rev,width=22,text='Total revenue: MRU '+str(total), bg='black',fg='white').grid(row=1,column=0)
    cx=0
    vsb=Scrollbar(orient='vertical')
    lb1=Listbox(rev,width=25, yscrollcommand=vsb.set)
    vsb.grid(row=2,column=1,sticky=N+S)
    lb1.grid(row=2,column=0)
    vsb.config( command = lb1.yview )
    cur.execute("select * from fact")
    for i in cur:
        if i[4]==today:
            cx+=1
            lb1.insert(cx,'Facture No.: '+str(i[5])+'    : MRU '+str(i[3]))
    c.commit()
    Button(rev,text='Menu Principale',command=main_menu).grid(row=15,column=0)
    rev.mainloop()


def search():   #page chercher un medicament et symptome --------------------------------- chercher medicament
    global c, cur, flag, st, mn, sym, flags
    flag='st'
    apt.destroy()
    cur.execute("Select * from med")
    symp=['nil']
    med_name=['nil']
    for i in cur:
        symp.append(i[5])
        med_name.append(i[1])
    st=Tk()
    st.title('CHERCHER')
    Label(st, text=' CHERCHER MEDICAMENT ').grid(row=0, column=0,columnspan=3)
    Label(st, text='~'*40).grid(row=1, column=0,columnspan=3)
    Label(st, text='Symptomes').grid(row=3, column=0)
    sym=Spinbox(st,values=symp)
    sym.grid(row=3, column=1)
    Button(st,width=15, text='CHERCHER', command=search_med).grid(row=3, column=2)
    Label(st, text='-'*70).grid(row=4, column=0,columnspan=3)
    if flags=='apt1':
        Button(st,width=15, text='Menu Principal', command=main_cus).grid(row=6, column=2)
    else:
        Button(st,width=15, text='Menu Principal', command=main_menu).grid(row=6, column=2)
    st.mainloop()

def search_med():
    global c, cur, st, sym, columns
    cur.execute("select * from med")
    y=[]
    x=0
    for i in cur:
        if i[5]==sym.get():
            y.append(str(i[0])+'. '+str(i[1])+'  MRU '+str(i[4])+'    Rack : '+str(i[7])+'    Mfg : '+str(i[8]))
            x=x+1
    top=Tk()
    for i in range(len(y)):
        Label(top,text=y[i]).grid(row=i, column=0)
    Button(top,text='OK',command=top.destroy).grid(row=5, column=0)
    c.commit()
    top.mainloop()

def val_cus():  #nouveau utilisateur-----------------------------------------------------------nouveau utilisateur
    global val, flag, dbt, name_vc, add_vc, cur, c, vc_id
    apt.destroy()
    cur.execute("select * from util")
    flag='val'
    val=Tk()
    val.title("Ajouter un Client")
    Label(val,text="ENTRER LES DETAILS DU CLIENT").grid(row=0,column=0,columnspan=3)
    Label(val,text="-"*60).grid(row=1,column=0,columnspan=3)
    Label(val,text="Nom: ").grid(row=2,column=0)
    name_vc=Entry(val)
    name_vc.grid(row=2, column=1)
    Label(val,text="Address: ").grid(row=3,column=0)
    add_vc=Entry(val)
    add_vc.grid(row=3, column=1)
    Label(val,text="Valeur Id: ").grid(row=4,column=0)
    vc_id=Entry(val)
    vc_id.grid(row=4, column=1)
    Button(val,text='Soumettre',command=val_get).grid(row=5, column=1)
    Button(val,text='Menu Principal',command=main_menu).grid(row=5, column=2)
    Label(val,text='-'*60).grid(row=6,column=0,columnspan=3)
    val.mainloop()

def val_get():  #submettre details de nouvelle valeur client
    global name_vc, add_vc, val, dbt ,c, cur, apt, vc_id
    cur.execute("insert into util values(?,?,?)",(name_vc.get(),add_vc.get(),vc_id.get()))
    l.execute("insert into log values(?,?)",(name_vc.get(),vc_id.get()))
    cur.execute("select * from util")
    for i in cur:
        print (i[0], i[1], i[2])
    c.commit()
    login.commit()
    
def again():    #page connection #login#-----------------------------------------------------------------------------LOGIN WINDOW
    global un, pwd, flag, root, apt
    if flag=='apt':
        apt.destroy()
    root=Tk()
    usr= PhotoImage(file="img/user.png")
    pas= PhotoImage(file="img/pas.png")
    root.title('.pyPharma')
    Label(root,text='.py pharma').grid(row=0,column=0,columnspan=5)
    Label(root,text="UNIVERSITE DE NOUAKCHOTT AL'ASRYA").grid(row=1,column=0,columnspan=5)
    Label(root,text='-------------------------------------------------------').grid(row=2,column=0,columnspan=5)
    Label(root, text='Utilisateur').grid(row=3, column=0)
    Label(root, text='u',image=usr).grid(row=3, column=1)
    un=Entry(root,width=10)
    un.grid(row=3, column=2)
    Label(root, text='MotDePass').grid(row=4, column=0)
    Label(root, text='p',image=pas).grid(row=4, column=1)
    pwd=Entry(root,width=10, show='*')
    pwd.grid(row=4, column=2)
    Button(root,width=6,text='Entrer',command=check).grid(row=5, column=1)
    Button(root,width=6,text='Fermer',command=root.destroy).grid(row=5, column=2)
    root.mainloop()
    
def check():    #pour button entrer login
    global un, pwd, login, l, root
    u=un.get()
    p=pwd.get()
    l.execute("select * from log")
    for i in l:     
        if i[0]==u and i[1]==p and u=='admin':
            root.destroy()
            open_win()
        elif i[0]==u and i[1]==p:
            root.destroy()
            open_cus()
    login.commit()

def main_menu(): #control ouverture fermeture menu principale----------------------------------------RETURN A MENU PRINCIPAL
    global sto, apt, flag, root, st, val, exp, st1,rev
    if flag=='sto':
        sto.destroy()
    if flag=='rev':
        rev.destroy()
    elif flag=='st':
        st.destroy()
    elif flag=='st1':
        st1.destroy()
    elif flag=='val':
        val.destroy()
    elif flag=='exp':
        exp.destroy()
    elif flag=='d':
        d.destroy()
    open_win()    

def main_cus():
    global st, flag, exp
    if flag=='exp':
        exp.destroy()
    elif flag=='st':
        st.destroy()
    open_cus()
    
def open_cus(): #OUVRE MENU PRINCIPALE----------------------------------------------------------------------------MENU PRINCIPALE
    global apt, flag, flags
    flags='apt1'
    apt=Tk()
    apt.title(".Py pharma")
    Label(apt, text=".Py PHARMA").grid(row=0,column=0)
    Label(apt, text='*'*40).grid(row=1,column=0)
    Label(apt, text='*  BIENVENUE  *').grid(row=2,column=0)
    Label(apt, text='-'*40).grid(row=3,column=0)
    Label(apt, text="Service Client").grid(row=4,column=0)
    Label(apt, text='-'*40).grid(row=5,column=0)
    Button(apt,text='Chercher', width=15, command=search).grid(row=6,column=0)
    Button(apt,text='Verifier Expiration', width=15, command=exp_date).grid(row=7,column=0)
    
    Label(apt, text='-'*40).grid(row=8,column=0)    
    Button(apt,text='Deconnecter',command=again1).grid(row=9, column=0)
    apt.mainloop()
def again1():
    global flags
    apt.destroy()
    flags=''
    again()
again()

