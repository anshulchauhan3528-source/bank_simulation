from tkinter import Tk,Label,Frame,Button,Entry,messagebox,simpledialog,filedialog
import time
import tablecreator
tablecreator.create()
from datetime import datetime
import generator
import sqlite3
import emailhandler
import re
from PIL import Image,ImageTk
import os

def update_time():
    curdate=time.strftime('%d-%b-%Y %r')
    date.configure(text=curdate)
    date.after(1000,update_time)

def forgot_screen():

    def back():
        frm.destroy()
        existuser_screen()

    def reset_click():
        e_adhar.delete(0,'end')
        e_acn.delete(0,'end')
        e_acn.focus()

    def send_otp():
        gen_otp=generator.generate_otp()
        acn=e_acn.get()
        adhar=e_adhar.get()

        conobj=sqlite3.connect(database='mybank.sqlite')
        curobj=conobj.cursor()
        query='''select name,email,pass from accounts where acn=? and adhar=?'''
        curobj.execute(query,(acn,adhar))
        tup=curobj.fetchone()
        conobj.close()
        if tup==None:
            messagebox.showerror('forgot password','record not found')
        else:
            emailhandler.send_otp(tup[1],tup[0],gen_otp)
            user_otp=simpledialog.askinteger('password recovery','Enter OTP')
            for i in range(3):
                if gen_otp==user_otp:
                    messagebox.showinfo('Passord Recovery',f'Your Password = {tup[2]}')
                    break
                else:
                    messagebox.showerror('Pssword Recovery','Invalid OTP')
                    user_otp=simpledialog.askinteger('password recovery','Enter OTP')
            if(user_otp!=gen_otp):
                otp_btn.configure(text='Resend OTP')

    frm=Frame(root)
    frm.configure(bg='pink',highlightbackground='black',highlightthickness=2)
    frm.place(relx=0,rely=.16,relwidth=1,relheight=.77)

    back_btn=Button(frm,text='Back',font=('arial',20,'bold'),bd=5,command=back)
    back_btn.place(relx=0,rely=0)

    lb1_acn=Label(frm,text='Account',font=('arial',20,'bold'),bg='purple',fg='white',width=8)
    lb1_acn.place(relx=.33,rely=.2)

    e_acn=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_acn.place(relx=.47,rely=.2)
    e_acn.focus()

    lb1_adhar=Label(frm,text='Adhar',font=('arial',20,'bold'),bg='purple',fg='white',width=8)
    lb1_adhar.place(relx=.33,rely=.3)

    e_adhar=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_adhar.place(relx=.47,rely=.3)

    otp_btn=Button(frm,text='Send OTP',font=('arial',20,'bold'),
                       activebackground='purple',activeforeground='black',
                       bd=5,width=10,command=send_otp)
    otp_btn.place(relx=.37,rely=.5)
    
    reset_btn=Button(frm,text='Reset',
                       font=('arial',20,'bold'),
                       activebackground='purple',activeforeground='black',
                       bd=5,width=9,command=reset_click)
    reset_btn.place(relx=.5,rely=.5)

def welcome_screen(acn=None):

    def logout():
        frm.destroy()
        main_screen()

    def check_screen():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.8)

        title_lb1=Label(ifrm,text='This is check Details screen',
                        font=('arial',20,'bold'),bg='white',fg='purple')
        title_lb1.pack()

        conobj=sqlite3.connect(database='mybank.sqlite')
        curobj=conobj.cursor()
        query='''select acn,bal,adhar,email,opendate from accounts where acn=?'''
        curobj.execute(query,(acn,))
        tup=curobj.fetchone()
        conobj.close()

        details=f'''
Account No = {tup[0]}\n
Account Balance = {tup[1]}\n
Account Adhar = {tup[2]}\n
Account emial = {tup[3]}\n
Account Opendate = {tup[4]}\n
'''

        lbl_details=Label(ifrm,text=details,bg='white',fg='purple',font=('arial',15,'bold'))
        lbl_details.place(relx=.3,rely=.2)

    def update_screen():

        def update_db():
            name=e_name.get()
            mob=e_mobile.get()
            email=e_email.get()
            pwd=e_pass.get()

            conobj=sqlite3.connect(database='mybank.sqlite')
            curobj=conobj.cursor()
            query='''update accounts set name=?,mob=?,email=?,pass=? where acn=?'''
            curobj.execute(query,(name,mob,email,pwd,acn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo('Update Screen','Details Updated Succesfully')
            welcome_screen(acn)

        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.8)

        title_lb1=Label(ifrm,text='This is update Details screen',
                        font=('arial',20,'bold'),bg='white',fg='purple')
        title_lb1.pack()

        conobj=sqlite3.connect(database='mybank.sqlite')
        curobj=conobj.cursor()
        query='''select name,email,pass,mob from accounts where acn=?'''
        curobj.execute(query,(acn,))
        tup=curobj.fetchone()
        conobj.close()


        lb1_name=Label(ifrm,text='Name',font=('arial',20,'bold'),bg='purple',fg='white',width=6)
        lb1_name.place(relx=.08,rely=.2)

        e_name=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_name.place(relx=.2,rely=.2)
        e_name.focus()

        lb1_email=Label(ifrm,text='Email',font=('arial',20,'bold'),bg='purple',fg='white',width=6)
        lb1_email.place(relx=.08,rely=.4)

        e_email=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_email.place(relx=.2,rely=.4)

        lb1_mobile=Label(ifrm,text='Mobile',font=('arial',20,'bold'),bg='purple',fg='white',width=6)
        lb1_mobile.place(relx=.52,rely=.2)

        e_mobile=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_mobile.place(relx=.65,rely=.2)

        lb1_pass=Label(ifrm,text='Pass',font=('arial',20,'bold'),bg='purple',fg='white',width=6)
        lb1_pass.place(relx=.52,rely=.4)

        e_pass=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_pass.place(relx=.65,rely=.4)

        e_name.insert(0,tup[0])
        e_email.insert(0,tup[1])
        e_mobile.insert(0,tup[3])
        e_pass.insert(0,tup[2])

        submit_btn=Button(ifrm,text='Submit',font=('arial',20,'bold'),
                        activebackground='purple',activeforeground='black',
                        bd=5,width=7,command=update_db)
        submit_btn.place(relx=.45,rely=.6)

    def deposit_screen():

        def deposit_db():
            amt=float(e_deposit.get())
            conobj=sqlite3.connect(database='mybank.sqlite')
            curobj=conobj.cursor()
            query='''update accounts set bal=bal+? where acn=?'''
            curobj.execute(query,(amt,acn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo('Deposit screen',f'{amt} Deposited succesfully')
            e_deposit.delete(0,'end')
            e_deposit.focus()


        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.8)

        title_lb1=Label(ifrm,text='This is deposit Details screen',
                        font=('arial',20,'bold'),bg='white',fg='purple')
        title_lb1.pack()

        lb1_deposit=Label(ifrm,text='Deposit Amt',font=('arial',20,'bold'),bg='purple',fg='white',width=10)
        lb1_deposit.place(relx=.2,rely=.3)

        e_deposit=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_deposit.place(relx=.4,rely=.3)
        e_deposit.focus()

        deposit_btn=Button(ifrm,text='Deposit',font=('arial',20,'bold'),
                        activebackground='purple',activeforeground='black',
                        bd=5,width=7,command=deposit_db)
        deposit_btn.place(relx=.4,rely=.6)

    def widthdraw_screen():

        def withdraw_db():
            amt=float(e_withdraw.get())
            conobj=sqlite3.connect(database='mybank.sqlite')
            curobj=conobj.cursor()
            query='''select bal,email,name from accounts where acn=?'''
            curobj.execute(query,(acn,))
            tup=curobj.fetchone()
            conobj.close()

            if tup[0]>=amt:
                gen_otp=generator.generate_otp()
                emailhandler.send_otp_withdraw(tup[1],tup[2],gen_otp,amt)
                user_otp=simpledialog.askinteger('withdraw OTP','OTP')
                if gen_otp==user_otp:
                    conobj=sqlite3.connect(database='mybank.sqlite')
                    curobj=conobj.cursor()
                    query='''update accounts set bal=bal-? where acn=?'''
                    curobj.execute(query,(amt,acn))
                    conobj.commit()
                    conobj.close()
                    messagebox.showinfo('withdraw Screen',f'{amt} withdrawn successfully')
                    e_withdraw.delete(0,'end')
                    e_withdraw.focus()
                else:
                    messagebox.showerror('Withdraw Screen','Invalid OTP')
                    withdraw_btn.configure(text='Resend OTP')
            else:
                messagebox.showerror('withdraw screen',f'{(tup[0])} Insufficient balance')


        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.8)

        title_lb1=Label(ifrm,text='This is withdraw Details screen',
                        font=('arial',20,'bold'),bg='white',fg='purple')
        title_lb1.pack()

        lb1_withdraw=Label(ifrm,text='withdraw Amt',font=('arial',20,'bold'),bg='purple',fg='white',width=13)
        lb1_withdraw.place(relx=.2,rely=.3)

        e_withdraw=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_withdraw.place(relx=.45,rely=.3)
        e_withdraw.focus()

        withdraw_btn=Button(ifrm,text='withdraw',font=('arial',20,'bold'),
                        activebackground='purple',activeforeground='black',
                        bd=5,width=10,command=withdraw_db)
        withdraw_btn.place(relx=.4,rely=.6)

    def transfer_screen():

        def transfer_db():
            to_acn=int(e_to.get())
            amt=float(e_transfer.get())

            conobj=sqlite3.connect(database='mybank.sqlite')
            curobj=conobj.cursor()
            query='''select * from accounts where acn=?'''
            curobj.execute(query,(to_acn,))
            tup=curobj.fetchone()
            conobj.close()

            if tup==None:
                messagebox.showerror('Transfer screen','Invalid to ACN')
                return

            conobj=sqlite3.connect(database='mybank.sqlite')
            curobj=conobj.cursor()
            query='''select bal,email,name from accounts where acn=?'''
            curobj.execute(query,(acn,))
            tup=curobj.fetchone()
            conobj.close()

            if tup[0]>=amt:
                gen_otp=generator.generate_otp()
                emailhandler.send_otp_transfer(tup[1],tup[2],gen_otp,amt,to_acn)
                user_otp=simpledialog.askinteger('Transfer OTP','OTP')
                
                if gen_otp==user_otp:
                    conobj=sqlite3.connect(database='mybank.sqlite')
                    curobj=conobj.cursor()

                    query1='''update accounts set bal=bal-? where acn=?'''
                    query2='''update accounts set bal=bal+? where acn=?'''
                    
                    curobj.execute(query1,(amt,acn))
                    curobj.execute(query2,(amt,to_acn))
                    conobj.commit()
                    conobj.close()
                    messagebox.showinfo('Transfer screen',f'{amt} transfered successfully')
                    e_transfer.delete(0,'end')
                    e_transfer.focus()
                else:
                    messagebox.showerror('Transfer screen','Invalid OTP')
                    transfer_btn.configure(text='Resend OTP')
            else:
                messagebox.showwarning('Transfer screen',f'Insufficient bal: {tup[0]}')


        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.8)

        title_lb1=Label(ifrm,text='This is transfer Details screen',
                        font=('arial',20,'bold'),bg='white',fg='purple')
        title_lb1.pack()

        lb1_to=Label(ifrm,text='To Account',font=('arial',20,'bold'),bg='purple',fg='white',width=13)
        lb1_to.place(relx=.2,rely=.25)

        e_to=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_to.place(relx=.45,rely=.25)
        e_to.focus()

        lb1_transfer=Label(ifrm,text='Transfer Amt',font=('arial',20,'bold'),bg='purple',fg='white',width=13)
        lb1_transfer.place(relx=.2,rely=.4)

        e_transfer=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_transfer.place(relx=.45,rely=.4)
    
        transfer_btn=Button(ifrm,text='Transfer',font=('arial',20,'bold'),
                        activebackground='purple',activeforeground='black',
                        bd=5,width=10,command=transfer_db)
        transfer_btn.place(relx=.4,rely=.7)

    conobj=sqlite3.connect(database='mybank.sqlite')
    curobj=conobj.cursor()
    query='''select name from accounts where acn=?'''
    curobj.execute(query,(acn,))
    tup=curobj.fetchone()
    conobj.close()

    frm=Frame(root)
    frm.configure(bg='pink',highlightbackground='black',highlightthickness=2)
    frm.place(relx=0,rely=.16,relwidth=1,relheight=.77)

    logout_btn=Button(frm,text='logout',font=('arial',20,'bold'),bd=5,command=logout)
    logout_btn.place(relx=0.92,rely=0)

    lb1_welcome=Label(frm,text=f'Welcome,{tup[0]}',font=('arial',20,'bold'),bg='purple',fg='white')
    lb1_welcome.place(relx=.001,rely=.0)

    def update_pic():
        name=filedialog.askopenfilename()
        os.rename(name,f'{acn}.jpg')
        img_profile=Image.open(f'{acn}.jpg').resize((255,125))
        imgtk_profile=ImageTk.PhotoImage(img_profile,master=root)
        lbl_img_profile=Label(frm,image=imgtk_profile)
        lbl_img_profile.place(relx=.001,rely=0.068)
        lbl_img_profile.im=imgtk_profile

    if os.path.exists(f'{acn}.jpg'):
        img_profile=Image.open(f'{acn}.jpg').resize((255,125))
    else:
        img_profile=Image.open('default.jpg').resize((255,125))

    imgtk_profile=ImageTk.PhotoImage(img_profile,master=root)

    lbl_img_profile=Label(frm,image=imgtk_profile)
    lbl_img_profile.place(relx=.001,rely=0.068)
    lbl_img_profile.image=imgtk_profile

    profile_btn=Button(frm,text='Update profile',font=('arial',20,'bold'),bd=5,width=15,command=update_pic)
    profile_btn.place(relx=0.001,rely=0.28)

    check_btn=Button(frm,text='Check Details',font=('arial',20,'bold'),bd=5,width=15,command=check_screen)
    check_btn.place(relx=0.001,rely=0.40)

    update_btn=Button(frm,text='Update Details',font=('arial',20,'bold'),bd=5,width=15,command=update_screen)
    update_btn.place(relx=0.001,rely=0.52)

    deposit_btn=Button(frm,text='Deposit Amount',font=('arial',20,'bold'),bd=5,width=15,bg='green',fg='white',command=deposit_screen)
    deposit_btn.place(relx=0.001,rely=0.64)

    widthdraw_btn=Button(frm,text='withdraw Amount',font=('arial',20,'bold'),bd=5,width=15,bg='red',command=widthdraw_screen)
    widthdraw_btn.place(relx=0.001,rely=0.76)

    transfer_btn=Button(frm,text='Transfer Amount',font=('arial',20,'bold'),bd=5,width=15,bg='red',command=transfer_screen)
    transfer_btn.place(relx=0.001,rely=0.88)


def existuser_screen():

    def back():
        frm.destroy()
        main_screen()
    
    def fp_click():
        frm.destroy()
        forgot_screen()

    def reset_click():
        e_acn.delete(0,'end')
        e_pass.delete(0,'end')
        e_acn.focus()

    def submit_click():
        acn=e_acn.get()
        pwd=e_pass.get()

        conobj=sqlite3.connect(database='mybank.sqlite')
        curobj=conobj.cursor()
        query='''select * from accounts where acn=? and pass=?'''
        curobj.execute(query,(acn,pwd))
        tup=curobj.fetchone()
        conobj.close()
        if tup==None:
            messagebox.showerror('Login','Invalid Credentials')
        else:
            tup=[0]
            frm.destroy()
            welcome_screen(acn)

    frm=Frame(root)
    frm.configure(bg='pink',highlightbackground='black',highlightthickness=2)
    frm.place(relx=0,rely=.16,relwidth=1,relheight=.77)

    back_btn=Button(frm,text='Back',font=('arial',20,'bold'),bd=5,command=back)
    back_btn.place(relx=0,rely=0)

    lb1_acn=Label(frm,text='Account',font=('arial',20,'bold'),bg='purple',fg='white',width=8)
    lb1_acn.place(relx=.33,rely=.2)

    e_acn=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_acn.place(relx=.47,rely=.2)
    e_acn.focus()

    lb1_pass=Label(frm,text='Password',font=('arial',20,'bold'),bg='purple',fg='white',width=8)
    lb1_pass.place(relx=.33,rely=.3)

    e_pass=Entry(frm,font=('arial',20,'bold'),bd=5,show='*')
    e_pass.place(relx=.47,rely=.3)

    submit_btn=Button(frm,text='Submit',font=('arial',20,'bold'),
                       activebackground='purple',activeforeground='black',
                       bd=5,width=7,
                       command=submit_click)
    submit_btn.place(relx=.37,rely=.5)
    
    reset_btn=Button(frm,text='Reset',
                       font=('arial',20,'bold'),
                       activebackground='purple',activeforeground='black',
                       bd=5,width=7,command=reset_click)
    reset_btn.place(relx=.48,rely=.5)

    fp_btn=Button(frm,text='Forgot Password',
                       font=('arial',20,'bold'),
                       activebackground='purple',activeforeground='black',
                       bd=5,width=15,command=fp_click)
    fp_btn.place(relx=.38,rely=.67)

def newuser_screen():

    def back():
        frm.destroy()
        main_screen()

    def reset_click():
        e_adhar.delete(0,'end')
        e_name.delete(0,'end')
        e_email.delete(0,'end')
        e_mobile.delete(0,'end')
        e_name.focus()

    def createacn_db():
        name=e_name.get()
        email=e_email.get()
        mob=e_mobile.get()
        adhar=e_adhar.get()

        if len(name)==0 or len(email)==0 or len(mob)==0 or len(adhar)==0:
            messagebox.showwarning('New user','Empty fields are not allowed')
            return

        match=re.fullmatch(r'[a-zA-Z0-9_.]+@[a-zA-Z]+\.[a-zA-Z]+',email)
        if match==None:
            messagebox.showwarning('New user','Invalid email')
            return
        
        match=re.fullmatch(r'[6-9][0-9]{9}',mob)
        if match==None:
            messagebox.showwarning('New user','Invalid mobile')
            return
        
        match=re.fullmatch(r'[0-9]{12}',adhar)
        if match==None:
            messagebox.showwarning('New user','Invalid adhar')
            return

        bal=0
        opendate=datetime.now()
        pwd=generator.generate_pass()
        query='''insert into accounts values(?,?,?,?,?,?,?,?)'''
        conobj=sqlite3.connect(database='mybank.sqlite')
        curobj=conobj.cursor()
        curobj.execute(query,(None,name,pwd,mob,email,adhar,bal,opendate))
        conobj.commit()
        conobj.close()

        conobj=sqlite3.connect(database='mybank.sqlite')
        curobj=conobj.cursor()
        query='''select max(acn) from accounts'''
        curobj.execute(query)
        tup=curobj.fetchone()
        conobj.close()
        
        emailhandler.send_credentials(email,name,tup[0],pwd)
        
        messagebox.showinfo('Account creation','Your Account is opened \nwe have mailed your credentails to given email')

    frm=Frame(root)
    frm.configure(bg='pink',highlightbackground='black',highlightthickness=2)
    frm.place(relx=0,rely=.16,relwidth=1,relheight=.77)

    back_btn=Button(frm,text='Back',font=('arial',20,'bold'),bd=5,command=back)
    back_btn.place(relx=0,rely=0)

    lb1_name=Label(frm,text='Name',font=('arial',20,'bold'),bg='purple',fg='white',width=7)
    lb1_name.place(relx=.1,rely=.2)

    e_name=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_name.place(relx=.2,rely=.2)
    e_name.focus()

    lb1_email=Label(frm,text='Email',font=('arial',20,'bold'),bg='purple',fg='white',width=7)
    lb1_email.place(relx=.1,rely=.3)

    e_email=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_email.place(relx=.2,rely=.3)

    lb1_mobile=Label(frm,text='📱Mobile',font=('arial',20,'bold'),bg='purple',fg='white',width=7)
    lb1_mobile.place(relx=.5,rely=.2)

    e_mobile=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_mobile.place(relx=.6,rely=.2)

    lb1_adhar=Label(frm,text='Adhar',font=('arial',20,'bold'),bg='purple',fg='white',width=7)
    lb1_adhar.place(relx=.5,rely=.3)

    e_adhar=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_adhar.place(relx=.6,rely=.3)

    submit_btn=Button(frm,text='Submit',font=('arial',20,'bold'),
                       activebackground='purple',activeforeground='black',
                       bd=5,width=7,command=createacn_db)
    submit_btn.place(relx=.37,rely=.5)
    
    reset_btn=Button(frm,text='Reset',
                       font=('arial',20,'bold'),
                       activebackground='purple',activeforeground='black',
                       bd=5,width=7,command=reset_click)
    reset_btn.place(relx=.48,rely=.5)

def main_screen():

    def newuser_click():
        frm.destroy()
        newuser_screen()

    def existuser_click():
        frm.destroy()
        existuser_screen()

    frm=Frame(root)
    frm.configure(bg='pink',highlightbackground='black',highlightthickness=2)
    frm.place(relx=0,rely=.16,relwidth=1,relheight=.77)

    newuser_btn=Button(frm,text='New User\nCreate Account',
                       font=('arial',20,'bold'),
                       activebackground='purple',activeforeground='black',
                       bd=5,width=12,
                       command=newuser_click)
    newuser_btn.place(relx=.36,rely=.3)

    existuser_btn=Button(frm,text='Existing User\nSign In',
                       font=('arial',20,'bold'),
                       activebackground='purple',activeforeground='black',
                       bd=5,width=12,
                       command=existuser_click)
    existuser_btn.place(relx=.54,rely=.3)

root=Tk()
root.state('zoomed')
root.resizable(width=False,height=False)
root.configure(bg="#0bfbeb")

title=Label(root,text='Banking Simulation',
       font=('arial',50,'bold','underline'),bg="#0bfbeb")
title.pack()


curdate=time.strftime('%d-%b-%Y %r')
date=Label(root,text=curdate,
       font=('arial',20,'bold'),bg="#0bfbeb",fg='blue')
date.pack(pady=15)
update_time()

img=Image.open('logo2.jpg').resize((200,130))
imgtk=ImageTk.PhotoImage(img,master=root)

lbl_img=Label(root,image=imgtk)
lbl_img.place(relx=0,rely=0)

img2=Image.open('logo.jpg').resize((200,130))
imgtk2=ImageTk.PhotoImage(img2,master=root)

lbl_img2=Label(root,image=imgtk2)
lbl_img2.place(relx=.88,rely=0)

footer=Label(root,text='Developed by: Anshul Chauhan\n 📱9311876766',
       font=('arial',18,'bold'),bg="#0bfbeb",fg='blue')
footer.pack(side='bottom')


main_screen()


root.mainloop()