# -*- coding: utf-8 -*-
import hashlib, urllib
import requests
import pyramid.threadlocal
import re
from geopy.geocoders import Nominatim

class ApiError(Exception): pass

class ApiRequest(object):
    def __init__(self, api_url=None):
        registry = pyramid.threadlocal.get_current_registry()
        settings = registry.settings
        if api_url is None:
            self.api_url = settings['apiurl']
        else: self.api_url = api_url
        self.session = requests.Session()

    def r(self, response):
        if response.status_code == 200:
            return response
        raise ApiError('Error %d %s' % (response.status_code, response.text))

    def get(self, path, *args, **kwargs):
        return self.r(self.session.get(self.api_url + path, **kwargs))

    def post(self, path, *args, **kwargs):
        return self.r(self.session.post(self.api_url + path, **kwargs))

    def put(self, path, *args, **kwargs):
        return self.r(self.session.put(self.api_url + path, **kwargs))

    def delete(self, path, *args, **kwargs):
        return self.r(self.session.delete(self.api_url + path, **kwargs))

###############################################################################
# Geolocation

geolocator = Nominatim()

def geocode(address):
    l = geolocator.geocode(address)
    return str(l.latitude) + ',' + str(l.longitude)

def isLatLong(string):
    return re.match('^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$', string) is not None

def geoParams(params):
    if 'departure' in params and not isLatLong(params['departure']):
        params['departure_address'] = params['departure']
        params['departure'] = geocode(params['departure'])
    if 'destination' in params and not isLatLong(params['destination']):
        params['destination_address'] = params['destination']
        params['destination'] = geocode(params['destination'])
    return params

###############################################################################
# Itineraries Endpoint

def getItineraries(username):
    return ApiRequest().get('/itineraries/', params={'owner': username}).json()

def getItinerary(id):
    return ApiRequest().get('/itineraries/' + str(id)).json()

def createItinerary(departure, name=None, destination=None, favorite=None):
    return ApiRequest().post('/itineraries/', data=geoParams({'name': name, 'departure': departure, 'destination': destination, 'favorite': favorite})).json()

def editItinerary(itinerary, departure=None, name=None, favorite=None):
    return ApiRequest().put('/itineraries/' + itinerary, params=geoParams({'name': name, 'departure': departure, 'favorite': favorite})).json()

def addDestination(itinerary, destination):
    return ApiRequest().post('/itineraries/' + itinerary + '/destinations', data=geoParams({'destination': destination})).json()

def editDestination(itinerary, position, destination):
    return ApiRequest().put('/itineraries/' + itinerary + '/destinations/' + position,
                            params=geoParams({'destination': destination})).json()

def deleteDestination(itinerary, position):
    return ApiRequest().delete('/itineraries/' + itinerary + '/destinations/' + position).json()

###############################################################################
# Users Endpoint

def getGravatar(email):
    default = 'retro'
    return ("http://www.gravatar.com/avatar/"
            + hashlib.md5(email.lower()).hexdigest()
            + "?" + urllib.urlencode({ 'd': default, 's': 200 }))

def getUser(username):
    user = ApiRequest().get('/users/' + username + '/').json()
    user['avatar'] = getGravatar(user['email'])
    return user

def createUser(username, password, email):
    data = {'username': username, 'password': password, 'email': email}
    user = ApiRequest().post('/users/', data=data).json()
    user['avatar'] = getGravatar(user['email'])
    return user

###############################################################################
# Tokens Endpoint

def authenticate(username, password):
    return ApiRequest().post('/sessions/', data={'username': username, 'password': password}).json()

def logout(token):
    ApiRequest().delete('/sessions/' + token)
