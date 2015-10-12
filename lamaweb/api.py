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
        print 'response: ',
        print response.text
        if response.status_code == 200:
            return response
        raise ApiError('Error %d %s' % (response.status_code, response.text))

    def get(self, path, *args, **kwargs):
        print '------- request'
        print 'GET ' + self.api_url + path
        print 'params: ',
        print kwargs.get('params', None)
        print 'GET ' + self.api_url + path
        r = self.r(self.session.get(self.api_url + path, **kwargs))
        print '/----'
        return r

    def post(self, path, *args, **kwargs):
        print '------- request'
        print 'POST ' + self.api_url + path
        print 'params: ',
        print kwargs.get('data', None)
        r = self.r(self.session.post(self.api_url + path, **kwargs))
        print '/----'
        return r

    def put(self, path, *args, **kwargs):
        print '------- request'
        print 'PUT ' + self.api_url + path
        print 'params: ',
        print kwargs.get('params', None)
        print 'PUT ' + self.api_url + path
        r = self.r(self.session.put(self.api_url + path, **kwargs))
        print '/----'
        return r

    def delete(self, path, *args, **kwargs):
        print 'DELETE ' + self.api_url + path
        return self.r(self.session.delete(self.api_url + path, **kwargs))

###############################################################################
# Geolocation

geolocator = Nominatim()

def geocode(address):
    l = geolocator.geocode(address)
    if l is not None:
        return (str(l.latitude) + ',' + str(l.longitude), l.address)
    raise ApiError('Invalid Location ' + address)

def isLatLong(string):
    return re.match('^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$', string) is not None

###############################################################################
# Parameters wrapper to handle authentication & geocoding

def prepareParams(request, params={}, token=False):
    if token and 'auth_token' in request.session:
        params['token'] = str(request.session['auth_token'])
    if 'departure' in params and params['departure'] and not isLatLong(params['departure']):
        params['departure'], params['departure_address'] = geocode(params['departure'])
    if 'destination' in params and params['destination'] and not isLatLong(params['destination']):
        params['destination'], params['destination_address'] = geocode(params['destination'])
    return params

###############################################################################
# Itineraries Endpoint

def getItineraries(request, username, favorite=None):
    return ApiRequest().get('/itineraries/', params=prepareParams(request, {'owner': username, 'favorite': favorite})).json()

def getItinerary(request, id):
    return ApiRequest().get('/itineraries/' + str(id), params=prepareParams(request)).json()

def createItinerary(request, departure, destination=None):
    return ApiRequest().post('/itineraries/', data=prepareParams(request, {'departure': departure, 'destination': destination}, token=True)).json()

def editItinerary(request, itinerary, departure=None, name=None, favorite=None):
    return ApiRequest().put('/itineraries/' + itinerary, params=prepareParams(request, {'name': name, 'departure': departure, 'favorite': favorite}, token=True)).json()

def addDestination(request, itinerary, destination):
    return ApiRequest().post('/itineraries/' + itinerary + '/destinations', data=prepareParams(request, {'destination': destination}, token=True)).json()

def editDestination(request, itinerary, position, destination):
    return ApiRequest().put('/itineraries/' + itinerary + '/destinations/' + position,
                            params=prepareParams(request, {'destination': destination}, token=True)).json()

def deleteDestination(request, itinerary, position):
    return ApiRequest().delete('/itineraries/' + itinerary + '/destinations/' + position, params=prepareParams(request, token=True)).json()

def deleteItinerary(request, itinerary):
    ApiRequest().delete('/itineraries/' + itinerary, params=prepareParams(request, token=True))

###############################################################################
# Users Endpoint

def getGravatar(email):
    default = 'retro'
    return ("http://www.gravatar.com/avatar/"
            + hashlib.md5(email.lower()).hexdigest()
            + "?" + urllib.urlencode({ 'd': default, 's': 200 }))

def getUser(request, username):
    user = ApiRequest().get('/users/' + username, params=prepareParams(request)).json()
    user['avatar'] = getGravatar(user['email'])
    return user

def getUsers(request, search=None, sponsored=None):
    users = ApiRequest().get('/users/', params=prepareParams(request, {'search': search, 'sponsored': sponsored})).json()
    for user in users:
        user['avatar'] = getGravatar(user['email'])
    return users

def createUser(request, username, password, email):
    user = ApiRequest().post('/users/', data=prepareParams(request, {'username': username, 'password': password, 'email': email})).json()
    user['avatar'] = getGravatar(user['email'])
    return user

def editUser(request, username, password=None, email=None, sponsor=None):
    user = ApiRequest().put('/users/' + username, params=prepareParams(request, {'password': password, 'email': email}, token=True)).json()
    user['avatar'] = getGravatar(user['email'])
    return user

def deleteUser(request, username):
    ApiRequest().delete('/users/' + username, params=prepareParams(request, {}, token=True))

###############################################################################
# Tokens Endpoint

def authenticate(request, username, password):
    return ApiRequest().post('/sessions/', data=prepareParams(request, {'username': username, 'password': password})).json()

def logout(request):
    if 'auth_token' in request.session:
        ApiRequest().delete('/sessions/' + request.session['auth_token'], params=prepareParams(request))
