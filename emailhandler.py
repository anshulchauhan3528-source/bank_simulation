import gmail
def send_credentials(email,name,acn,pwd):
    con=gmail.GMail('anshul.chauhan.3528@gmail.com','isjj rrpg fcmc mnku')
    body=f'''Hello {name},
    Welcome to Anshul Bank,here is your credentaials'
    Account number = {acn}
    Password = {pwd}

    Kindly change your password when you login first time

    Anshul Bank
    malakpur Greater Noida

'''
    msg=gmail.Message(to=email,subject='Your Credentials for operating account',text=body)
    con.send(msg)

def send_otp(email,name,otp):
    con=gmail.GMail('anshul.chauhan.3528@gmail.com','isjj rrpg fcmc mnku')
    body=f'''Hello {name},
    Welcome to Anshul Bank,here is your OTP'

    OTP = {otp}

   
    Anshul Bank
    malakpur Greater Noida

'''
    msg=gmail.Message(to=email,subject='Your OTP for password recovery',text=body)
    con.send(msg)

def send_otp_withdraw(email,name,otp,amt):
    con=gmail.GMail('anshul.chauhan.3528@gmail.com','isjj rrpg fcmc mnku')
    body=f'''Hello {name},
    Welcome to Anshul Bank,here is your OTP to withdraw {amt}'

    OTP = {otp}

   
    Anshul Bank
    malakpur Greater Noida

'''
    msg=gmail.Message(to=email,subject='Your OTP to widraw amount',text=body)
    con.send(msg)


def send_otp_transfer(email,name,otp,amt,to_acn):
    con=gmail.GMail('anshul.chauhan.3528@gmail.com','isjj rrpg fcmc mnku')
    body=f'''Hello {name},
    Welcome to Anshul Bank,here is your OTP to transfer amount : {amt} to ACN : {to_acn}'

    OTP = {otp}

   
    Anshul Bank
    malakpur Greater Noida

'''
    msg=gmail.Message(to=email,subject='Your OTP to Transfer amount',text=body)
    con.send(msg)