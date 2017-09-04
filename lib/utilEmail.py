#!/usr/bin/env python3 

import os
import sys 
import time 
import configparser 
import smtplib





class emailConst:
    """ some constants and templates used in the module 
    """

    smtp_server_gmail = "smtp.gmail.com"
    smtp_port_gmail = 587 

    message_template = "From: From {sender_name} <{sender}>\r\n"\
        "To: To {receiver} <{receiver}>\r\n"\
        "MIME-Version: 1.0\r\n"\
        "Content-type: text/html\r\n"\
        "Subject: {topic}\r\n\r\n{message}"



class emailClient: 
    def __init__(self, smtp_server, 
                    login_username, login_password, sender_name=None,
                    smtp_port=25, use_SSL=False, use_TLS=False):
        """
        initialize a class for sending emails 
        """

        self.smtp_server = smtp_server 
        self.smtp_port = smtp_port 
        self.login_username = login_username
        self.login_password = login_password 
        if sender_name is None: 
            self.sender_name = self.login_username 
        else:
            self.sender_name = sender_name 

        self.use_SSL = use_SSL  
        self.use_TLS = use_TLS 
        
        if use_SSL: 
            self.email_server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        else: 
            self.email_server = smtplib.SMTP(smtp_server, smtp_port) 

        if use_TLS: 
            self.email_server.starttls() 


        try: 
            # server.ehlo()
            # server.starttls()   
            self.email_server.login(login_username, login_password)
        except Exception as e: 
            print("failed to initialize email client: {}".format(e), file=sys.stderr) 
            exit(1)



    def send_email(self, message, receiver=None, topic="No topic"):
        if receiver is None:
            assert self.receiver is not None, "please provide receiver email" 
            receiver = self.receiver

        try: 
            self.email_server.sendmail(self.login_username, receiver, 
                            emailConst.message_template.format(sender=self.login_username
                                                             , sender_name=self.sender_name
                                                             , receiver=receiver
                                                             , topic=topic
                                                             , message=message))         

        except Exception as e: 
            print("ERROR: failed to send email {}".format(e), file=sys.stderr)
            exit(1)


    def close(self):
        self.email_server.quit() 

    def __exit__(self):
        self.close() 


class gmailClient(emailClient):
    def __init__(self, login_username, login_password, sender_name=None):
        super(gmailClient, self).__init__(emailConst.smtp_server_gmail, 
                                            login_username, 
                                            login_password, 
                                            sender_name, 
                                            smtp_port=emailConst.smtp_port_gmail, 
                                            use_SSL=False, use_TLS=True)


class defaultEmailClient(emailClient):
    def __init__(self):
        super(defaultEmailClient, self).__init__(emailConst.smtp_server_gmail, 
                                                "notificationSender2017@gmail.com", 
                                                "everyoneKnowsThisPassword", 
                                                sender_name="email_sender", 
                                                smtp_port=emailConst.smtp_port_gmail, 
                                                use_SSL=False, use_TLS=True)


class configEmailClient(emailClient):
    def __init__(self):
        self.config = configClass()
        print(self.config)
        assert self.config.email_service == "gmail", "only gmail is supported for now" 

        if self.config.email_service == "gmail":
            super(configEmailClient, self).__init__(emailConst.smtp_server_gmail, 
                                                    self.config.sender, 
                                                    self.config.sender_pass, 
                                                    sender_name=self.config.sender_name,
                                                    smtp_port=emailConst.smtp_port_gmail, 
                                                    use_SSL=False, use_TLS=True)
        self.receiver = self.config.receiver 


if __name__ == "__main__": 
    client = defaultEmailClient()
    client.send_email("peter.waynechina@gmail.com", sys.argv[1]) 
    client.close() 






