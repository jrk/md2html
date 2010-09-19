#!/usr/bin/env python
# encoding: utf-8
"""
handle_incoming_email.py

Created by Jonathan Ragan-Kelley on 2009-12-23.
Copyright (c) 2009 Jonathan Ragan-Kelley. All rights reserved.
"""

import logging, email
from google.appengine.ext import webapp 
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import mail
import markdown2

import os
def mail_domain():
    app_id = os.environ.get('APPLICATION_ID', '')
    return '%s.appspotmail.com' % app_id

class MsgHandler(InboundMailHandler):
    def receive(self, msg):
        md = dict(msg.bodies())['text/plain'].decode()
        logging.info("Received a message\n"
                     "from: %s\n"
                     "to: %s\n"
                     "subject: %s\n"
                     "date: %s\n"
                     "body (text/plain): %s"
                     % (msg.sender,
                        msg.to,
                        msg.subject,
                        msg.date,
                        md )
                    )
        html = markdown2.markdown( md )
        logging.info( 'md: %s' % html )
        
        reply = mail.EmailMessage(
            sender = 'Render Markdown <md@%s>' % mail_domain(),
            to = msg.sender,
            subject = 'Re: %s' % msg.subject
        )
        reply.body = md
        reply.html = html
        
        reply.send()

def main():
    application = webapp.WSGIApplication([MsgHandler.mapping()],
                                         debug=True)
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
