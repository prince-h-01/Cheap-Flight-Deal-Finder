import smtplib

MY_EMAIL = "francesco.m.felix@gmail.com"
MY_PASSWORD = "webdjkrgzhveazwf"
RECIPIENT_EMAIL = MY_EMAIL


class NotificationManager:
    def send_email(self, contents):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=RECIPIENT_EMAIL,
                                msg=f"Subject:Air ticket price drop!\n\n{contents}")
