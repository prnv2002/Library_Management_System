from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
import Library_features
import datetime
import sqlite3
image1='menu.png'
image2='book.png'
image3='user.png'
image4='login.png'
mem_id=0

class menu:

    def __init__(self):
        self.root=Tk()
        self.root.title('Menu')
        conn=sqlite3.connect('Library.db')
        conn.execute('''create table if not exists book_info
        (ID INTEGER PRIMARY KEY ,
        TITLE VARTEXT NOT NULL,
        AUTHOR VARTEXT NOT NULL,
        GENRE VARTEXT NOT NULL,
        COPIES VARINT NOT NULL,
        LOCATION VARCHAR NOT NULL,
        TIMES_ISSUED VARINT NOT NULL);''')
        conn.commit()
        conn.execute('''create table if not exists user_info
        (ID INTEGER PRIMARY KEY,
        FNAME VARTEXT NOT NULL,
        LNAME VARTEXT NOT NULL,
        PHONE INT(10) NOT NULL,
        EMAIL_ID VARTEXT NOT NULL);''')
        conn.commit()
        conn.execute('''create table if not exists book_issued
        (BOOK_ID INTEGER NOT NULL,
        USER_ID INTEGER NOT NULL,
        ISSUE_DATE DATE NOT NULL,
        RETURN_DATE DATE NOT NULL,
        PRIMARY KEY (BOOK_ID,USER_ID),
        FOREIGN KEY (BOOK_ID)
            REFERENCES book_info (ID),
        FOREIGN KEY (USER_ID)
            REFERENCES user_info (ID));''')
        conn.commit()
        conn.close()
        self.a=self.canvases(image1,0,0)
        l1=Button(self.a,text='MANAGE BOOKS',font='Papyrus 22 bold',fg='black',bg='yellow',width=19,padx=10,borderwidth=0,command=self.book).place(x=50,y=275)
        l2=Button(self.a,text='USER ACTIVITY',font='Papyrus 22 bold',fg='black',bg='yellow',width=19,padx=10,borderwidth=0,command=self.User).place(x=500,y=275)
        self.root.mainloop()
    def canvases(self,images,h,w):
        w = int(self.root.winfo_screenwidth()/2)+w
        h = int(self.root.winfo_screenheight()/2)+h
        photo=Image.open(images)
        photo1=photo.resize((w,h),Image.ANTIALIAS)
        photo2=ImageTk.PhotoImage(photo1)

        self.canvas = Canvas(self.root, width='%d'%w, height='%d'%h)
        self.canvas.grid(row = 0, column = 0)
        self.canvas.grid_propagate(0)
        self.canvas.create_image(0, 0, anchor = NW, image=photo2)
        self.canvas.image=photo2
        return self.canvas
    def book(self):
        self.a.destroy()
        self.a=self.canvases(image2,0,100)
        l1=Button(self.a,text='Add Books',font='Papyrus 22 bold',fg='black',bg='yellow',width=15,padx=10,command=self.addbook).place(x=10,y=30)
        l2=Button(self.a,text='Search Books',font='Papyrus 22 bold',fg='black',bg='yellow',width=15,padx=10,command=self.search).place(x=10,y=130)
        l3=Button(self.a,text='All Books',font='Papyrus 22 bold',fg='black',bg='yellow',width=15,padx=10,command=self.all).place(x=10,y=230)
        l4=Button(self.a,text='Genre Analysis',font='Papyrus 22 bold',fg='black',bg='yellow',width=15,padx=10,command=self.bar_graph).place(x=10,y=330)
        l5=Button(self.a,text='<- Main Menu',font='Papyrus 22 bold',fg='black',bg='yellow',width=15,padx=10,command=self.mainmenu).place(x=10,y=450)

    def addbook(self):
        self.aauthor=StringVar()
        self.aname=StringVar()
        self.acopies=IntVar()
        self.agenre=StringVar()
        self.aloc=StringVar()
        self.f1=Frame(self.a,height=500,width=650,bg='black')
        self.f1.place(x=380,y=30)

        l2=Label(self.f1,text='Title : ',font='Papyrus 12 bold',fg='Orange',bg='Black',pady=1).place(x=50,y=50)
        e1=Entry(self.f1,width=45,bg='orange',fg='black',textvariable=self.aname).place(x=150,y=50)
        l3=Label(self.f1,text='Author : ',font='Papyrus 12 bold',fg='orange',bg='Black',pady=1).place(x=50,y=100)
        e3=Entry(self.f1,width=45,bg='orange',fg='black',textvariable=self.aauthor).place(x=150,y=100)
        l4=Label(self.f1,text='Genre : ',font='Papyrus 12 bold',fg='orange',bg='Black',pady=1).place(x=50,y=150)
        e1=Entry(self.f1,width=45,bg='orange',fg='black',textvariable=self.agenre).place(x=150,y=150)
        l4=Label(self.f1,text='Copies : ',font='Papyrus 12 bold',fg='orange',bg='Black',pady=1).place(x=50,y=200)       
        e2=Entry(self.f1,width=45,bg='orange',fg='black',textvariable=self.acopies).place(x=150,y=200)
        l5=Label(self.f1,text='Location : ',font='Papyrus 12 bold',fg='orange',bg='Black',pady=1).place(x=50,y=250)
        e3=Entry(self.f1,width=45,bg='orange',fg='black',textvariable=self.aloc).place(x=150,y=250)
        self.f1.grid_propagate(0)
        b1=Button(self.f1,text='Add',font='Papyrus 10 bold',fg='black',bg='orange',width=15,bd=3,command=self.addbookdata).place(x=150,y=400)
        b2=Button(self.f1,text='Back',font='Papyrus 10 bold',fg='black',bg='orange',width=15,bd=3,command=self.rm).place(x=350,y=400)

    def rm(self):
        self.f1.destroy()
    def mainmenu(self):
        self.root.destroy()
        a=menu()

    def addbookdata(self):
        b=self.aname.get()
        c=self.aauthor.get()
        d=self.agenre.get()
        goahed=True
        try:
            e=self.acopies.get()
        except:
            messagebox.showinfo("Error","Number of copies cannot be characters.")
            goahed=False
        f=self.aloc.get()
        g=0
        conn=sqlite3.connect('Library.db')
        if goahed==True :
            try:
                if (b and c and d  and f)=="":
                    messagebox.showinfo("Error","Fields cannot be empty.")
                else:
                    conn.execute("insert into book_info (TITLE, AUTHOR, GENRE, COPIES, LOCATION, TIMES_ISSUED)\
                    values (?,?,?,?,?,?)",(b.capitalize(),c.capitalize(),d.capitalize(),e,f.capitalize(),g,));
                    conn.commit()
                    messagebox.showinfo("Success","Book added successfully")
            except sqlite3.IntegrityError:
                messagebox.showinfo("Error","Book is already present.")


        conn.close()

    def search(self):
        self.sid=StringVar()
        self.f1=Frame(self.a,height=500,width=650,bg='black')
        self.f1.place(x=380,y=30)
        l1=Label(self.f1,text='Book ID/Title/Author/Genre: ',font=('Papyrus 10 bold'),bd=2, fg='orange',bg='black').place(x=20,y=40)
        e1=Entry(self.f1,width=25,bd=5,bg='orange',fg='black',textvariable=self.sid).place(x=260,y=40)
        b1=Button(self.f1,text='Search',bg='orange',font='Papyrus 10 bold',width=9,bd=2,command=self.serch1).place(x=500,y=37)
        b1=Button(self.f1,text='Back',bg='orange',font='Papyrus 10 bold',width=10,bd=2,command=self.rm).place(x=250,y=450)

    def create_tree(self,plc,lists):
        self.tree=ttk.Treeview(plc,height=13,column=(lists),show='headings')
        n=0
        while n is not len(lists):
            self.tree.heading("#"+str(n+1),text=lists[n])
            self.tree.column(""+lists[n],width=100)
            n=n+1
        return self.tree


    def serch1(self):
        k=self.sid.get()
        if k!="":
            self.list4=("BOOK ID","TITLE","AUTHOR","GENRE","COPIES","LOCATION")
            self.trees=self.create_tree(self.f1,self.list4)
            self.trees.place(x=25,y=150)
            conn=sqlite3.connect('Library.db')

            c=conn.execute("select * from book_info where ID=? OR TITLE=? OR AUTHOR=? OR GENRE=?",(k.capitalize(),k.capitalize(),k.capitalize(),k.capitalize(),))
            a=c.fetchall()
            if len(a)!=0:
                for row in a:

                    self.trees.insert("",END,values=row)
                conn.commit()
                conn.close()
                self.trees.bind('<<TreeviewSelect>>')
                self.variable = StringVar(self.f1)
                self.variable.set("Select Action:")


                self.cm =ttk.Combobox(self.f1,textvariable=self.variable ,state='readonly',font='Papyrus 15 bold',height=50,width=15,)
                self.cm.config(values =('Add Copies', 'Delete Copies', 'Delete Book'))

                self.cm.place(x=50,y=100)
                self.cm.pack_propagate(0)


                self.cm.bind("<<ComboboxSelected>>",self.combo)
                self.cm.selection_clear()
            else:
                messagebox.showinfo("Error","Data not found")



        else:
            messagebox.showinfo("Error","Search field cannot be empty.")


    def combo(self,event):
        self.var_Selected = self.cm.current()
        if self.var_Selected==0:
            self.copies(self.var_Selected)
        elif self.var_Selected==1:
            self.copies(self.var_Selected)
        elif self.var_Selected==2:
            self.deleteitem()
    def deleteitem(self):
        try:
            self.curItem = self.trees.focus()

            self.c1=self.trees.item(self.curItem,"values")[0]
            b1=Button(self.f1,text='Update',font='Papyrus 10 bold',width=9,bd=3,command=self.delete2).place(x=500,y=97)

        except:
            messagebox.showinfo("Empty","Please select something.")
    def delete2(self):
        conn=sqlite3.connect('Library.db')
        cd=conn.execute("select * from book_issued where BOOK_ID=?",(self.c1,))
        ab=cd.fetchall()
        if ab==[]:
            conn.execute("DELETE FROM book_info where ID=?",(self.c1,));
            conn.commit()
            messagebox.showinfo("Successful","Book Deleted sucessfully.")
            self.trees.delete(self.curItem)
        else:
            messagebox.showinfo("Error","Book is Issued.\nBook cannot be deleted.")
        conn.commit()
        conn.close()


    def copies(self,varr):
        try:
            curItem = self.trees.focus()
            self.c1=self.trees.item(curItem,"values")[0]
            self.c2=self.trees.item(curItem,"values")[4]
            self.scop=IntVar()
            self.e5=Entry(self.f1,width=20,textvariable=self.scop)
            self.e5.place(x=310,y=100)
            if varr==0:
                b5=Button(self.f1,text='Update',font='Papyrus 10 bold',bg='orange',fg='black',width=9,bd=3,command=self.copiesadd).place(x=500,y=97)
            if varr==1:
                b6=Button(self.f1,text='Update',font='Papyrus 10 bold',bg='orange',fg='black',width=9,bd=3,command=self.copiesdelete).place(x=500,y=97)
        except:
            messagebox.showinfo("Empty","Please select something.")

    def copiesadd(self):
        goahed=True
        try:
            no=self.e5.get()
        except:
            messagebox.showinfo("Error","Number of copies cannot be characters.")
            goahed=False
        
        if goahed==True:
            if int(no)>=0:

                conn=sqlite3.connect('Library.db')

                conn.execute("update book_info set COPIES=COPIES+? where ID=?",(no,self.c1,))
                conn.commit()

                messagebox.showinfo("Updated","Copies added sucessfully.")
                self.serch1()
                conn.close()

            else:
                messagebox.showinfo("Error","No. of copies cannot be negative.")

    def copiesdelete(self):
        goahed=True
        try:
            no1=self.e5.get()
        except:
            messagebox.showinfo("Error","Number of copies cannot be characters.")
            goahed=False
        
        if goahed==True:
            if int(no1)>=0:
                if int(no1)<=int(self.c2):
                    conn=sqlite3.connect('Library.db')

                    conn.execute("update book_info set COPIES=COPIES-? where ID=?",(no1,self.c1,))
                    conn.commit()
                    conn.close()

                    messagebox.showinfo("Updated","Deleted sucessfully")
                    self.serch1()

                else:
                    messagebox.showinfo("Maximum","No. of copies to delete exceed available copies.")
            else:
                messagebox.showinfo("Error","No. of copies cannot be negative.")

    def all(self):
        self.f1=Frame(self.a,height=500,width=650,bg='black')
        self.f1.place(x=380,y=30)
        b1=Button(self.f1,text='Back',bg='orange' ,fg='black',width=10,bd=3,command=self.rm).place(x=250,y=400)
        conn=sqlite3.connect('Library.db')
        self.list3=("BOOK ID","TITLE","AUTHOR","GENRE","COPIES","LOCATION")
        self.treess=self.create_tree(self.f1,self.list3)
        self.treess.place(x=25,y=50)

        c=conn.execute("select * from book_info")
        g=c.fetchall()
        if len(g)!=0:
            for row in g:
                self.treess.insert('',END,values=row)
        conn.commit()
        conn.close()


    def bar_graph(self):
        conn=sqlite3.connect('Library.db')
        c=conn.execute("select Genre, sum(TIMES_ISSUED) from book_info group by Genre")
        g=c.fetchall()
        dist_genre=[]
        issued_times=[]
        for x in g:
            dist_genre=dist_genre+[x[0]]
            issued_times=issued_times+[x[1]]
        Library_features.make_graph(dist_genre,issued_times)

    def User(self):
        self.a.destroy()
        self.a=self.canvases(image3,200,200)
        l1=Button(self.a,text='Issue book',font='Papyrus 22 bold',fg='black',bg='yellow',width=15,padx=10,command=self.issue).place(x=10,y=30)
        l2=Button(self.a,text='Return Book',font='Papyrus 22 bold',fg='black',bg='yellow',width=15,padx=10,command=self.returnn).place(x=10,y=130)
        l3=Button(self.a,text='View Issued books',font='Papyrus 22 bold',fg='black',bg='yellow',width=15,padx=10,command=self.activity).place(x=10,y=230)
        l4=Button(self.a,text='Add User',font='Papyrus 22 bold',fg='black',bg='yellow',width=15,padx=10,command=self.adduser).place(x=10,y=330)
        l4=Button(self.a,text='View Users',font='Papyrus 22 bold',fg='black',bg='yellow',width=15,padx=10,command=self.viewuser).place(x=10,y=430)
        l5=Button(self.a,text='<< Main Menu',font='Papyrus 22 bold',fg='black',bg='yellow',width=15,padx=10,command=self.mainmenu).place(x=10,y=600)



    def cnfissuedbook(self):
        bookid=self.aidd.get()
        Userid=self.aUsert.get()
        conn=sqlite3.connect('Library.db')
        try:
            current_date=datetime.datetime.today()
            due_date=datetime.datetime.today() + datetime.timedelta(7)
            conn.execute("insert into book_issued \
            values (?,?,?,?)",(bookid,Userid,current_date.strftime("%x"),due_date.strftime("%x"),))
            conn.commit()
            conn.execute("update book_info set COPIES=COPIES-1, TIMES_ISSUED=TIMES_ISSUED+1 where ID=?",(bookid,))
            conn.commit()
            conn.close()

            conn=sqlite3.connect('Library.db')
            c=conn.execute("select TITLE from book_info Where ID=?",(bookid,))
            g=c.fetchall()
            bname=[x[0] for x in g]

            c=conn.execute("select FNAME,LNAME,EMAIL_ID from user_info Where ID=?",(Userid,))
            g=c.fetchall()
            fname=[x[0] for x in g]
            lname=[x[1] for x in g]
            to_id=[x[2] for x in g]

            c=conn.execute("SELECT usermailid,password FROM login where mem_id=?",(mem_id,))
            g=c.fetchall()
            from_id=[x[0] for x in g]
            password=[x[1] for x in g]

            conn.close()

            Library_features.issue_mail(fname[0],lname[0],bname[0],due_date.strftime("%x"),from_id[0],to_id[0],password[0])
            messagebox.showinfo("Updated","Book Issued sucessfully.")
        except:
            messagebox.showinfo("Error","Book is already issued by User.")



    def issue(self):
        self.aidd=StringVar()
        self.aUsert=StringVar()
        self.Username=StringVar()
        self.f1=Frame(self.a,height=500,width=650,bg='black')
        self.f1.place(x=380,y=30)
        """ self.f1=Frame(self.a,height=550,width=500,bg='black')
        self.f1.place(x=380,y=30) """
        l1=Label(self.f1,text='Book ID : ',font='papyrus 15 bold',bg='black',fg='orange').place(x=50,y=150)
        e1=Entry(self.f1,width=25,bd=4,bg='orange',textvariable=self.aidd).place(x=180,y=150)
        l2=Label(self.f1,text='User Id : ',font='papyrus 15 bold',bg='black',fg='orange').place(x=50,y=200)
        e2=Entry(self.f1,width=25,bd=4,bg='orange',textvariable=self.aUsert).place(x=180,y=200)
        b1=Button(self.f1,text='Back',font='Papyrus 10 bold',fg='black',bg='orange',width=10,bd=3,command=self.rm).place(x=70,y=250)
        b1=Button(self.f1,text='Procced',font='Papyrus 10 bold',fg='black',bg='orange',width=10,bd=3,command=self.issuedbook).place(x=220,y=250)

    def issuedbook(self):
        plc=self.f1
        bookid=self.aidd.get()
        Userid=self.aUsert.get()
        conn=sqlite3.connect('Library.db')
        cursor=conn.cursor()
        cursor.execute("select ID,COPIES from book_info where ID=?",(bookid,))
        an=cursor.fetchall()
        cursor.execute("select ID from user_info where ID=?",(Userid,))
        au=cursor.fetchall()
        if (bookid and Userid!=""):
            if au!=[]:
                if an!=[]:

                    l2=Label(self.f1,text='User Info : ',font='papyrus 15 bold',bg='black',fg='orange').place(x=400,y=120)
                    lists=["First Name","Last Name"]
                    self.tree=ttk.Treeview(plc,height=1,column=(lists),show='headings')
                    n=0
                    while n is not len(lists):
                        self.tree.heading("#"+str(n+1),text=lists[n])
                        self.tree.column(""+lists[n],width=100)
                        n=n+1
                    c=conn.execute("select FNAME,LNAME from user_info Where ID=?",(Userid,))
                    g=c.fetchall()
                    if len(g)!=0:
                        for row in g:
                            self.tree.insert('',END,values=row)
                    self.tree.place(x=400,y=150)
                    

                    l1=Label(self.f1,text='Book Info : ',font='papyrus 15 bold',bg='black',fg='orange').place(x=400,y=220)
                    lists=["Title","Author"]
                    self.tree=ttk.Treeview(plc,height=1,column=(lists),show='headings')
                    n=0
                    while n is not len(lists):
                        self.tree.heading("#"+str(n+1),text=lists[n])
                        self.tree.column(""+lists[n],width=100)
                        n=n+1
                    c=conn.execute("select TITLE,AUTHOR from book_info Where ID=?",(bookid,))
                    g=c.fetchall()
                    if len(g)!=0:
                        for row in g:
                            self.tree.insert('',END,values=row)
                    self.tree.place(x=400,y=250)

                    conn.close()

                    for i in an:
                        if i[1]>0:
                            b1=Button(self.f1,text='Issue',font='Papyrus 10 bold',fg='black',bg='orange',width=10,bd=3,command=self.cnfissuedbook).place(x=450,y=320)

                        else:
                            messagebox.showinfo("Unavailable","Book unavailable.\nThere are 0 copies of the book.")
                else:
                    messagebox.showinfo("Error","No such Book in Database.")
            else:
                messagebox.showinfo("Error","No such User in Database.")
        else:
            messagebox.showinfo("Error","Fields cannot be blank.")

    def returnn(self):
        self.aidd=StringVar()
        self.aUsert=StringVar()

        self.f1=Frame(self.a,height=500,width=650,bg='black')
        self.f1.place(x=380,y=30)
        """ self.f1=Frame(self.a,height=550,width=500,bg='black')
        self.f1.place(x=380,y=30) """
        l1=Label(self.f1,text='Book ID : ',font='papyrus 15 bold',fg='orange', bg='black').place(x=50,y=150)
        e1=Entry(self.f1,width=25,bd=4,bg='orange',textvariable=self.aidd).place(x=180,y=150)
        l2=Label(self.f1,text='User Id : ',font='papyrus 15 bold',fg='orange', bg='black').place(x=50,y=200)
        e2=Entry(self.f1,width=25,bd=4,bg='orange',textvariable=self.aUsert).place(x=180,y=200)
        b1=Button(self.f1,text='Back',font='Papyrus 10 bold',bg='orange',fg='black',width=10,bd=3,command=self.rm).place(x=70,y=250)
        b1=Button(self.f1,text='Procced',font='Papyrus 10 bold',bg='orange',fg='black',width=10,bd=3,command=self.returnbook).place(x=220,y=250)
        self.f1.grid_propagate(0)

    def cnfreturnbook(self):
        bookid=self.aidd.get()
        Userid=self.aUsert.get()
        conn=sqlite3.connect('Library.db')
        conn.execute("DELETE FROM book_issued where BOOK_ID=? and USER_ID=?",(bookid,Userid,))
        conn.commit()
        conn.execute("update book_info set COPIES=COPIES+1 where ID=?",(bookid,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success","Book Returned sucessfully.")

    def returnbook(self):
        bookid=self.aidd.get()
        Userid=self.aUsert.get()
        plc = self.f1

        conn=sqlite3.connect('Library.db')
        cursor = conn.cursor()
        cursor.execute("select ID,COPIES from book_info where ID=?",(bookid,))
        an=cursor.fetchall()
        cursor.execute("select ID from user_info where ID=?",(Userid,))
        au=cursor.fetchall()
        if (bookid and Userid!=""):
            if au!=[]:
                if an!=[]:
                    c=conn.execute("select * from book_issued where BOOK_ID=? and USER_ID=?",(bookid,Userid,))
                    d=c.fetchall()
                    conn.commit()
                    if d!=[]:
                        l2=Label(self.f1,text='User Info : ',font='papyrus 15 bold',bg='black',fg='orange').place(x=400,y=120)
                        lists=["First Name","Last Name"]
                        self.tree=ttk.Treeview(plc,height=1,column=(lists),show='headings')
                        n=0
                        while n is not len(lists):
                            self.tree.heading("#"+str(n+1),text=lists[n])
                            self.tree.column(""+lists[n],width=100)
                            n=n+1
                        c=conn.execute("select FNAME,LNAME from user_info Where ID=?",(Userid,))
                        g=c.fetchall()
                        if len(g)!=0:
                            for row in g:
                                self.tree.insert('',END,values=row)
                        self.tree.place(x=400,y=150)
                        

                        l1=Label(self.f1,text='Book Info : ',font='papyrus 15 bold',bg='black',fg='orange').place(x=400,y=220)
                        lists=["Title","Author"]
                        self.tree=ttk.Treeview(plc,height=1,column=(lists),show='headings')
                        n=0
                        while n is not len(lists):
                            self.tree.heading("#"+str(n+1),text=lists[n])
                            self.tree.column(""+lists[n],width=100)
                            n=n+1
                        c=conn.execute("select TITLE,AUTHOR from book_info Where ID=?",(bookid,))
                        g=c.fetchall()
                        if len(g)!=0:
                            for row in g:
                                self.tree.insert('',END,values=row)
                        self.tree.place(x=400,y=250)
                        conn.close()
                        b1=Button(self.f1,text='Return',font='Papyrus 10 bold',fg='black',bg='orange',width=10,bd=3,command=self.cnfreturnbook).place(x=450,y=320)

                    else:
                        messagebox.showinfo("Error","Data not found.")
                else:
                    messagebox.showinfo("Error","No such Book in Database.")
            else:
                messagebox.showinfo("Error","No such User in Database.")
        else:
            messagebox.showinfo("Error","Fields cannot be blank.")

    def activity(self):
        self.aidd=StringVar()
        self.aUsert=StringVar()
        self.f1=Frame(self.a,height=500,width=650,bg='black')
        self.f1.place(x=380,y=30)
        """ self.f1=Frame(self.a,height=550,width=500,bg='black')
        self.f1.place(x=380,y=30) """
        self.list2=("BOOK ID","User ID","ISSUE DATE","RETURN DATE")
        self.trees=self.create_tree(self.f1,self.list2)
        self.trees.place(x=50,y=150)


        l1=Label(self.f1,text='Book/User ID : ',font='Papyrus 15 bold',fg='Orange',bg='black').place(x=50,y=30)
        e1=Entry(self.f1,width=20,bd=4,bg='orange',textvariable=self.aidd).place(x=280,y=35)
        #l2=Label(self.f1,text='User Id : ',font='papyrus 15 bold',fg='orange',bg='black').place(x=50,y=80)
        #e2=Entry(self.f1,width=20,bd=4,bg='orange',textvariable=self.aUsert).place(x=180,y=80)
        b1=Button(self.f1,text='Back',bg='orange',font='Papyrus 10 bold',width=10,bd=3,command=self.rm).place(x=340,y=450)
        b1=Button(self.f1,text='Search',bg='orange',font='Papyrus 10 bold',width=10,bd=3,command=self.searchact).place(x=40,y=450)
        b1=Button(self.f1,text='All',bg='orange',font='Papyrus 10 bold',width=10,bd=3,command=self.searchall).place(x=190,y=450)
        self.f1.grid_propagate(0)

    def searchact(self):
        self.list2=("BOOK ID","USER ID","ISSUE DATE","RETURN DATE")
        self.trees=self.create_tree(self.f1,self.list2)
        self.trees.place(x=50,y=150)
        conn=sqlite3.connect('Library.db')
        bid=self.aidd.get()
        try:
            c=conn.execute("select * from book_issued where BOOK_ID=? or USER_ID=?",(bid,bid,))
            d=c.fetchall()
            if len(d)!=0:
                for row in d:
                    self.trees.insert("",END,values=row)
            else:
                messagebox.showinfo("Error","Data not found.")
            conn.commit()

        except Exception as e:
            messagebox.showinfo(e)
        conn.close()

    def searchall(self):
        self.list2=("BOOK ID","USER ID","ISSUE DATE","RETURN DATE")
        self.trees=self.create_tree(self.f1,self.list2)
        self.trees.place(x=50,y=150)
        conn=sqlite3.connect('Library.db')
        try:
            c=conn.execute("select * from book_issued")
            d=c.fetchall()
            for row in d:
                self.trees.insert("",END,values=row)

            conn.commit()

        except Exception as e:
            messagebox.showinfo(e)
        conn.close()

    def adduser(self):
        self.fname=StringVar()
        self.lname=StringVar()
        self.phone=IntVar()
        self.email=StringVar()
        self.f1=Frame(self.a,height=500,width=650,bg='black')
        self.f1.place(x=380,y=30)
        l1=Label(self.f1,text='First Name : ',font='Papyrus 15 bold',fg='Orange',bg='Black').place(x=50,y=50)
        e1=Entry(self.f1,width=45,bd=4,bg='orange',fg='black',textvariable=self.fname).place(x=175,y=50)
        l2=Label(self.f1,text='Last Name : ',font='Papyrus 15 bold',fg='Orange',bg='Black').place(x=50,y=100)
        e2=Entry(self.f1,width=45,bd=4,bg='orange',fg='black',textvariable=self.lname).place(x=175,y=100)
        l4=Label(self.f1,text='Phone No.: ',font='Papyrus 15 bold',fg='orange',bg='Black').place(x=50,y=150)
        e2=Entry(self.f1,width=45,bd=4,bg='orange',fg='black',textvariable=self.phone).place(x=175,y=150)
        l4=Label(self.f1,text='MailID : ',font='Papyrus 15 bold',fg='orange',bg='Black').place(x=50,y=200)
        e2=Entry(self.f1,width=45,bd=4,bg='orange',fg='black',textvariable=self.email).place(x=175,y=200)
        self.f1.grid_propagate(0)
        b1=Button(self.f1,text='Add',font='Papyrus 10 bold',fg='black',bg='orange',width=15,bd=3,command=self.adduserdata).place(x=150,y=400)
        b2=Button(self.f1,text='Back',font='Papyrus 10 bold',fg='black',bg='orange',width=15,bd=3,command=self.rm).place(x=350,y=400)

    def adduserdata(self):
        a=self.fname.get()
        b=self.lname.get()
        d=self.email.get()
        conn=sqlite3.connect('Library.db')
        goahed=True
        try:
            c=self.phone.get()
        except:
            messagebox.showinfo("Error","Phone Number cannot be characters.")
            goahed=False
        
        if goahed==True:
            if len(c)==10:
                try:
                    if (a and b and d )=="":
                        messagebox.showinfo("Error","Fields cannot be empty.")
                    else:
                        cursor=conn.cursor()
                        cursor.execute("select ID from user_info where EMAIL_ID= (?)",(d,))
                        au=cursor.fetchall()
                        if au!=[]: 
                            messagebox.showinfo("Error","Mail ID already in use.")
                        else:
                            conn.execute("insert into user_info (FNAME, LNAME, PHONE, EMAIL_ID)\
                            values (?,?,?,?)",(a.capitalize(),b.capitalize(),c,d,));
                            conn.commit()
                            messagebox.showinfo("Success","User added successfully")
                        
                except sqlite3.IntegrityError:
                    messagebox.showinfo("Error","User is already present.")
            else:
                messagebox.showinfo("Error","More or less then 10 digits entered!")

        conn.close()

    def delete_user(self):
        conn=sqlite3.connect('Library.db')
        cd=conn.execute("select * from book_issued where USER_ID=?",(self.c1,))
        ab=cd.fetchall()
        if ab==[]:
            conn.execute("DELETE FROM user_info where ID=?",(self.c1,))
            conn.commit()
            messagebox.showinfo("Successful","User Deleted sucessfully.")
            self.trees.delete(self.curItem)
        else:
            messagebox.showinfo("Error","User has an Issued book.\nUser cannot be deleted.")
        conn.commit()
        conn.close()

    def update_mail(self):
        mail=self.e5.get()

        conn=sqlite3.connect('Library.db')
        conn.execute("update user_info set EMAIL_ID=? where ID=?",(mail,self.c1,))
        conn.commit()

        messagebox.showinfo("Updated","Mail ID changed sucessfully.")
        self.serchuser()
        conn.close()


    def update_phone(self):
        
        goahed=True
        try:
            no=self.e5.get()
        except:
            messagebox.showinfo("Error","Phone Number cannot be characters.")
            goahed=False
        
        if goahed==True:
            if len(no)==10:

                conn=sqlite3.connect('Library.db')

                conn.execute("update user_info set PHONE=? where ID=?",(no,self.c1,))
                conn.commit()

                messagebox.showinfo("Updated","Phone Number changed sucessfully.")
                self.serchuser()
                conn.close()

            else:
                messagebox.showinfo("Error","More or less then 10 digits entered!")
        

    def updateuser(self,event):
        self.var_Selected = self.cm.current()
        
        try:
            curItem = self.trees.focus()
            self.c1=self.trees.item(curItem,"values")[0]
            self.c2=self.trees.item(curItem,"values")[4]
            if self.var_Selected!=2:
                self.scop=IntVar()
                self.nmail=StringVar()
                if self.var_Selected==0:
                    self.e5=Entry(self.f1,width=20,textvariable=self.scop)
                    self.e5.place(x=310,y=100)
                    b5=Button(self.f1,text='Update',font='Papyrus 10 bold',bg='orange',fg='black',width=9,bd=3,command=self.update_phone).place(x=500,y=97)
                elif self.var_Selected==1:
                    self.e5=Entry(self.f1,width=20,textvariable=self.nmail)
                    self.e5.place(x=310,y=100)
                    b6=Button(self.f1,text='Update',font='Papyrus 10 bold',bg='orange',fg='black',width=9,bd=3,command=self.update_mail).place(x=500,y=97)
            elif self.var_Selected==2:
                self.curItem = self.trees.focus()
                self.c1=self.trees.item(self.curItem,"values")[0]
                b1=Button(self.f1,text='Update',font='Papyrus 10 bold',width=9,bd=3,command=self.delete_user).place(x=500,y=97)
        except:
            messagebox.showinfo("Empty","Please select something.")


    def serchuser(self):
        k=self.sid.get()
        if k!="":
            self.list4=("USER ID","FIRST NAME","LAST NAME","PHONE","EMAIL_ID")
            self.trees=self.create_tree(self.f1,self.list4)
            self.trees.place(x=25,y=150)
            conn=sqlite3.connect('Library.db')

            c=conn.execute("select * from user_info where ID=? OR Fname=? OR Lname=? OR EMAIL_ID=?",(k.capitalize(),k.capitalize(),k.capitalize(),k.capitalize(),))
            a=c.fetchall()
            if len(a)!=0:
                for row in a:

                    self.trees.insert("",END,values=row)
                conn.commit()
                conn.close()
                self.trees.bind('<<TreeviewSelect>>')
                self.variable = StringVar(self.f1)
                self.variable.set("Select Action:")


                self.cm =ttk.Combobox(self.f1,textvariable=self.variable ,state='readonly',font='Papyrus 15 bold',height=50,width=15,)
                self.cm.config(values =('Update Phone No.', 'Update Mail_ID', 'Delete User'))

                self.cm.place(x=50,y=100)
                self.cm.pack_propagate(0)


                self.cm.bind("<<ComboboxSelected>>",self.updateuser)
                self.cm.selection_clear()
            else:
                messagebox.showinfo("Error","Data not found")



        else:
            messagebox.showinfo("Error","Search field cannot be empty.")

    def viewuser(self):
        self.sid=StringVar()
        self.f1=Frame(self.a,height=500,width=650,bg='black')
        self.f1.place(x=380,y=30)
        l1=Label(self.f1,text='User ID/Fname/Lname/Mail Id: ',font=('Papyrus 10 bold'),bd=2, fg='orange',bg='black').place(x=20,y=40)
        e1=Entry(self.f1,width=25,bd=5,bg='orange',fg='black',textvariable=self.sid).place(x=260,y=40)
        b1=Button(self.f1,text='Search',bg='orange',font='Papyrus 10 bold',width=9,bd=2,command=self.serchuser).place(x=500,y=37)
        b1=Button(self.f1,text='Back',bg='orange',font='Papyrus 10 bold',width=10,bd=2,command=self.rm).place(x=250,y=450)
        conn=sqlite3.connect('Library.db')
        self.list3=("USER ID","FIRST NAME","LAST NAME","PHONE","EMAIL_ID")
        self.treess=self.create_tree(self.f1,self.list3)
        self.treess.place(x=25,y=150)

        c=conn.execute("select * from user_info")
        g=c.fetchall()
        if len(g)!=0:
            for row in g:
                self.treess.insert('',END,values=row)
        conn.commit()
        conn.close()
#===================START=======================
def canvases(images,w,h):
    photo=Image.open(images)
    photo1=photo.resize((w,h),Image.ANTIALIAS)
    photo2=ImageTk.PhotoImage(photo1)

#photo2 = ImageTk.PhotoImage(Image.open(images).resize((w, h)),Image.ANTIALIAS)
    canvas = Canvas(root, width='%d'%w, height='%d'%h)
    canvas.grid(row = 0, column = 0)
    canvas.grid_propagate(0)
    canvas.create_image(0, 0, anchor = NW, image=photo2)
    canvas.image=photo2
    return canvas
root = Tk()
root.title("LOGIN")
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
canvas=canvases(image4,int(w/2),int(h/2))

def automail():
    def sendmail():
        due_date=datetime.datetime.today() + datetime.timedelta(1)
        due_date=due_date.strftime("%x")
        conn=sqlite3.connect('Library.db')
        cursor=conn.cursor()
        cursor.execute("select BOOK_ID,USER_ID,RETURN_DATE from book_issued ")
        issue_info=cursor.fetchall()
        for i in issue_info:
            ret_date=i[2]
            if (ret_date==due_date):
                bookid=i[0]
                c=conn.execute("select TITLE from book_info Where ID=?",(bookid,))
                g=c.fetchall()
                bname=[x[0] for x in g]

                Userid=i[1]
                c=conn.execute("select FNAME,LNAME,EMAIL_ID from user_info Where ID=?",(Userid,))
                g=c.fetchall()
                fname=[x[0] for x in g]
                lname=[x[1] for x in g]
                to_id=[x[2] for x in g]

                c=conn.execute("SELECT usermailid,password FROM login where mem_id=?",(mem_id,))
                g=c.fetchall()
                from_id=[x[0] for x in g]
                password=[x[1] for x in g]

                conn.close()

                Library_features.remainder_mail(fname[0],lname[0],bname[0],due_date,from_id[0],to_id[0],password[0])    
    

    current_time=datetime.datetime.now()
    if(current_time.strftime("%H:%M")=="15:12"):
        sendmail()
    root.after(60000,automail)
#==============================METHODS========================================
def Database():
    global conn, cursor
    conn = sqlite3.connect("Library.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `login` (mem_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, usermailid TEXT, password TEXT)")
    cursor.execute("SELECT * FROM `login` WHERE `usermailid` = 'admin' AND `password` = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `login` (usermailid, password) VALUES('admin', 'admin')")
        conn.commit()

def Login(event=None):
    Database()
    global mem_id

    if USERNAME.get() == "" or PASSWORD.get() == "":
        messagebox.showinfo("Error","Please complete the required field!")
        lbl_text.config(text="Please complete the required field!", fg="red")
    else:
        c=conn.execute("SELECT * FROM `login` WHERE `usermailid` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
        g=c.fetchall()
        if g != []:
            member_id=[x[0] for x in g]
            mem_id=member_id[0]
            root.destroy()
            automail()
            a=menu()
        else:
            messagebox.showinfo("Error","Invalid mailID or password.")
            USERNAME.set("")
            PASSWORD.set("")
    cursor.close()
    conn.close()


#==============================VARIABLES======================================
USERNAME = StringVar()
PASSWORD = StringVar()

#==============================LABELS=========================================
lbl_title = Label(canvas, text = " ADMIN LOGIN :", font=('Papyrus', 30,'bold', ),bg='white', fg='black')
lbl_title.place(x=275,y=80)
lbl_username = Label(canvas, text = "Mail ID :", font=('Papyrus', 15,'bold'),bd=4,bg='orange', fg='black')
lbl_username.place(x=300,y=230)
lbl_password = Label(canvas, text = "Password :", font=('Papyrus', 15,'bold'),bd=3, bg='orange', fg='black')
lbl_password.place(x=300, y=330)
lbl_text = Label(canvas)
lbl_text.place(x=200,y=500)
lbl_text.grid_propagate(0)

#==============================ENTRY WIDGETS==================================
username = Entry(canvas, textvariable=USERNAME, cursor="xterm white",font=(14), bg='black', fg='orange',bd=6)
username.place(x=450, y=230,)
password = Entry(canvas, textvariable=PASSWORD, cursor="xterm white",show="*", font=(14),bg='black', fg='orange',bd=6)
password.place(x=450, y=330)

#==============================BUTTON WIDGETS=================================
btn_login = Button(canvas, text="LOGIN", font=('Papyrus 15 bold'),width=10,command=Login, bg='#abc123', fg='black')
btn_login.place(x=380,y=420)
btn_login.bind('<Return>', Login)
root.mainloop()
