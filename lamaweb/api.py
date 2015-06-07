# -*- coding: utf-8 -*-
import hashlib, urllib
import requests
import pyramid.threadlocal

class ApiRequest(object):
    def __init__(self):
        registry = pyramid.threadlocal.get_current_registry()
        settings = registry.settings
        self.api_url = settings['apiurl']
        self.session = requests.Session()

    def get(self, path, *args, **kwargs):
        return self.session.get(self.api_url + path, **kwargs)

    def post(self, path, *args, **kwargs):
        return self.session.post(self.api_url + path, **kwargs).json()

    def delete(self, path, *args, **kwargs):
        return self.session.delete(self.api_url + path, **kwargs).json()

###############################################################################
# Itineraries Endpoint

def getItineraries(username):
    return ApiRequest().get('/itineraries/', params={'owner': username})

def getItinerary(id):
    i = ApiRequest().get('/itineraries/' + str(id) + '/')
    return i.json()

def createItinerary(departure, name=None, destination=None, favorite=False):
    return ApiRequest().post('/itineraries/', params={'name': name, 'departure': departure, 'destination': destination, 'favorite': favorite})

###############################################################################
# Users Endpoint

def getGravatar(email):
    default = 'retro'
    return ("http://www.gravatar.com/avatar/"
            + hashlib.md5(email.lower()).hexdigest()
            + "?" + urllib.urlencode({ 'd': default, 's': 200 }))

def getUser(username):
    return ApiRequest().get('/users/' + username + '/')

def createUser(username, password, email):
    return ApiRequest().post('/users/', params={'username': username, 'password': password, 'email': email})

###############################################################################
# Tokens Endpoint

def authenticate(username, password):
    return ApiRequest().post('/tokens/', params={'username': username, 'password': password})

def logout(token):
    return ApiRequest().delete('/tokens/' + token + '/')
