import logging
import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.options import define, options
import itertools

import math

import datetime
import time
from time import time
import dateutil
from dateutil.parser import *
import pytz
from pytz import timezone

import os.path

import json
import urllib

import pymongo
import asyncmongo

import base64
import random
from random import randrange
import hashlib

import re

from pprint import pprint

# Pusher client
import hmac

# Import SMTP Client
from tornadomail.message import EmailMessage, EmailMultiAlternatives
from tornadomail.backends.smtp import EmailBackend

# Import reddit
import praw

define("port", default=8888, help="run on the given port", type=int)

# SSH
# ssh-keygen -t rsa -C "info@friidum.com" -f  ~/.ssh/id_rsa_heroku
# ssh-add ~/.ssh/id_rsa_heroku
# heroku keys:add ~/.ssh/id_rsa_heroku.pub

# Mongo console
# mongo linus.mongohq.com:10026/app10999577 -u heroku -p secret

# Pusher credentials

class Application(tornado.web.Application):
    
    def __init__(self, debug = False):
        handlers = [
            # Home page
            (r"/", MainHandler)
        ]
        settings = dict(
            cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/beta",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            facebook_api_key="521121077928184",
            facebook_secret="5a1a030bb5c71b5c702f19f5526b105d",
            debug=debug
        )
        
        # logging.info("Static URL: {}".format(settings['static_path']))
        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    
    response = {}

    root = "http://localhost:8888" if True else "http://thedeckgame.herokuapp.com"
    
    def _async(self, response = False, error = False):
        if error:
            print(error)
    
    def _respond(self):
        self.write(tornado.escape.json_encode(self.response))
        print tornado.escape.json_encode(self.response)
        self.finish()
    
    @property
    def db(self):
        if not hasattr(self, '_db'):
            self._db = asyncmongo.Client(pool_id='test_pool', host='linus.mongohq.com', port=10026, dbuser="heroku", dbpass="secret", dbname="app10999577", maxcached=10, maxconnections=1000)
        return self._db
    
    @property
    def http(self):
        self._http = tornado.httpclient.AsyncHTTPClient()
        return self._http

    @property
    def reddit(self):
    	self._reddit = praw.Reddit('gaysian_front')
    	return self._reddit

    @property
    def subreddit(self):
    	self._sub = self.reddit.get_subreddit('gaysian')
    	return self._sub

    def generate_id(self):
        return hashlib.sha224(str(random.random())).hexdigest()[0:11];

class MainHandler(BaseHandler):
	def get(self):
		self.render("index.html")
            

# Main Runtime
def main():
    tornado.options.parse_command_line()
    logging.info("starting webserver on 0.0.0.0:%d" % tornado.options.options.port)
    print("Web server started again at "+str(datetime.datetime.now()))
    app = Application(debug = (True if options.port==8888 else False))
    app.listen(options.port)
    
    # Create IOLoop
    mainloop = tornado.ioloop.IOLoop

    # Start main loop
    mainloop.instance().start()


if __name__ == "__main__": main()