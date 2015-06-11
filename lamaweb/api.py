# -*- coding: utf-8 -*-
import hashlib, urllib
import requests
import pyramid.threadlocal

class ApiRequest(object):
    def __init__(self, api_url=None):
        registry = pyramid.threadlocal.get_current_registry()
        settings = registry.settings
        if api_url is None:
            self.api_url = settings['apiurl']
        else: self.api_url = api_url
        self.session = requests.Session()

    def get(self, path, *args, **kwargs):
        return self.session.get(self.api_url + path, **kwargs)

    def post(self, path, *args, **kwargs):
        return self.session.post(self.api_url + path, **kwargs)

    def put(self, path, *args, **kwargs):
        return self.session.put(self.api_url + path, **kwargs)

    def delete(self, path, *args, **kwargs):
        return self.session.delete(self.api_url + path, **kwargs)

###############################################################################
# Itineraries Endpoint

def getItineraries(username):
    return ApiRequest().get('/itineraries/', params={'owner': username}).json()

def getItinerary(id):
    return ApiRequest().get('/itineraries/' + str(id)).json()

def createItinerary(departure, name=None, destination=None, favorite=None):
    return ApiRequest().post('/itineraries/', data={'name': name, 'departure': departure, 'destination': destination, 'favorite': favorite}).json()

def editItinerary(departure=None, name=None, favorite=None):
    return ApiRequest().put('/itineraries/', data={'name': name, 'departure': departure, 'favorite': favorite})

def addDestination(itinerary, destination):
    return ApiRequest().post('/itineraries/destinations/' + itinerary, data={'destination': destination}).json()

def editDestination(itinerary, position, destination):
    return ApiRequest().put('/itineraries/destinations/' + itinerary + '/' + position,
                            params={'destination': destination}).json()

def deleteDestination(itinerary, position):
    return ApiRequest().delete('/itineraries/' + itinerary + '/destinations/' + position + '/').json()

###############################################################################
# Users Endpoint

def getGravatar(email):
    default = 'retro'
    return ("http://www.gravatar.com/avatar/"
            + hashlib.md5(email.lower()).hexdigest()
            + "?" + urllib.urlencode({ 'd': default, 's': 200 }))

def getUser(username):
    user = ApiRequest(api_url='http://poney.paysdu42.fr/lamaurbain/').get('/users/' + username + '/').json()
    user['avatar'] = getGravatar(user['email'])
    return user

def createUser(username, password, email):
    user = ApiRequest(api_url='http://poney.paysdu42.fr/lamaurbain/').post('/users/', data={'username': username, 'password': password, 'email': email}).json()
    user['avatar'] = getGravatar(user['email'])
    return user

###############################################################################
# Tokens Endpoint

def authenticate(username, password):
    return ApiRequest(api_url='http://poney.paysdu42.fr/lamaurbain/').post('/tokens/', data={'username': username, 'password': password}).json()

def logout(token):
    ApiRequest(api_url='http://poney.paysdu42.fr/lamaurbain/').delete('/tokens/' + token + '/')
