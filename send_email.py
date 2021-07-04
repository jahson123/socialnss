import smtplib
import random
import string
from email.message import EmailMessage


def email(user_email, uid, name):
    email = smtplib.SMTP('smtp.gmail.com', 587)
    email.starttls()

    email.login("sagerioko4@gmail.com", "wasabi123")

    msg = EmailMessage()
    msg['Subject'] = f'Email Verification for SNS system, {user_email}'
    msg['From'] = "no-replay@mail.SNS.com"
    msg['To'] = user_email
    msg.add_alternative(f"""\
    <!DOCTYPE html>
    <html lang="en">
    <body >
    <div style="background: #e6e6e6; max-height: 100%;">
        <img src="https://firebasestorage.googleapis.com/v0/b/unique-perigee-299514.appspot.com/o/logo%202.png?alt=media" alt="logo"
            style="display: block; padding: 10px; margin: auto;" width=10%" height="10%"/>
        <div class="email_container" style="padding: 15px; background: white; display: block;display: block; margin: auto; max-width: 40%; max-height: 350px;">
            <div class="email_content">
                <h3 style="text-align: center;">SNSS - Account Verification</h3>
                <br>
                <p>Hi {name}, Welcome to the SNSS community</p><br>
                <p>Click here to verify your email.</p>
                <a href="https://socialnss.herokuapp.com/emailverified/{uid}/{name}"><b>Follow this link for account activation</b></a>
                <br><br>
                <p>Thank you, </p>
                <p>The SNSS Team</p>
            </div>
        </div>
    </div>
    </body>
    </html>
    """,subtype='html')
    email.send_message(msg)
    email.quit()
    return user_email, uid, name


def change_pwd_email(user_email, uid):
    pwd_generator = string.ascii_letters + string.digits
    pwd = ''.join(random.choice(pwd_generator) for i in range(10))
    email = smtplib.SMTP('smtp.gmail.com', 587)
    email.starttls()

    email.login("sagerioko4@gmail.com", "wasabi123")

    msg = EmailMessage()
    msg['Subject'] = f'Password Reset for SNSS Account, {user_email}'
    msg['From'] = "no-replay@mail.SNS.com"
    msg['To'] = user_email
    msg.add_alternative(f"""\
        <!DOCTYPE html>
        <html lang="en">
        <body >
        <div style="background: #e6e6e6; max-height: 100%;">
            <img src="https://firebasestorage.googleapis.com/v0/b/unique-perigee-299514.appspot.com/o/logo%202.png?alt=media" alt="logo"
                style="display: block; padding: 10px; margin: auto;" width=10%" height="10%"/>
            <div class="email_container" style="padding: 15px; background: white; display: block;display: block; margin: auto; max-width: 40%; max-height: 350px;">
                <div class="email_content">
                    <h3 style="text-align: center;">SNSS - Password Reset</h3>
                    <br>
                    <a href="http://127.0.0.1:5000/pwdreset/{uid}/{pwd}"><b>Click the following link to reset your account password.</b></a>
                    <p>Your password will be reset to this given after you click the link</p>
                    <h3>{pwd}</h3>
                    <p>Don't reply this email and delete this email after reset your password</p>
                    <br><br>
                    <p>Thank you, </p>
                    <p>The SNSS Team</p>
                </div>
            </div>
        </div>
        </body>
        </html>
        """, subtype='html')
    email.send_message(msg)
    email.quit()
    pass

