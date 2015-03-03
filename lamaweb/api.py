# -*- coding: utf-8 -*-
import hashlib, urllib

# TODO
# all those functions should make API calls instead

def getItineraries(user):
    return [
        {
            'id': 12345,
            'name': u'Buy a wallet',
            'departure': u'Chatelet les Halles, Paris',
            'destinations': [
                u'Pont neuf, Paris',
                u'Gare Montparnasse, Paris',
            ],
        },
        {
            'id': 12346,
            'name': u'Home to school',
            'departure': u'12 rue de la Convention, Le Kremlin-Bicêtre',
            'destinations': [
                u'47 Rue Danton, Le Kremlin-Bicêtre',
            ],
        },
    ]

def getItinerary(user, id):
    itineraries = getItineraries(user)
    for itinerary in itineraries:
        if itinerary['id'] == id:
            return itinerary
    return None

def getGravatar(email):
    default = 'retro'
    return ("http://www.gravatar.com/avatar/"
            + hashlib.md5(email.lower()).hexdigest()
            + "?" + urllib.urlencode({ 'd': default, 's': 200 }))

def getUser():
    user = {
        'email': 'decorne.en@gmail.com',
        'total_itineraries': len(getItineraries('a')),
    }
    user['avatar'] = getGravatar(user['email'])
    return user
