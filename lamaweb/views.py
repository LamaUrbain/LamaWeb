from pyramid.view import view_config
import pyramid.threadlocal
from pyramid.httpexceptions import HTTPFound
import json
import api

def globalContext(request):
    return {
        'apiurl': pyramid.threadlocal.get_current_registry().settings['apiurl'],
        'apiitiurl': pyramid.threadlocal.get_current_registry().settings['apiitiurl'],
        'authentified': True if 'auth_token' in request.session else False,
        'user': request.session['auth_user'] if 'auth_user' in request.session else None,
    }

@view_config(route_name='home', renderer='templates/home.jinja2')
def home(request):
    return globalContext(request)

@view_config(route_name='search', renderer='templates/search.jinja2')
def search(request):
    if 'departure' in request.POST:
        itinerary = api.createItinerary(departure=request.POST['departure'],
                                        name=(request.POST['name'] if 'name' in request.POST else None),
                                        destination=(request.POST['arrival'] if 'arrival' in request.POST else None),
                                        favorite=(True if 'name' in request.POST else False))
        return HTTPFound(location='/itinerary/' + context['itinerary']['id'])
    context = globalContext(request)
    return context

@view_config(route_name='itinerary', renderer='templates/search.jinja2')
def itinerary(request):
    context = globalContext(request)
    di = request.matchdict
    id = di.get("id", None)
    if not id or not id.isdigit():
        request.response.status = 400
        return { 'error': 'Invalid Itinerary id' }
    id = int(id)
    itinerary = api.getItinerary(id)
    if not itinerary:
        request.response.status = 404
        return { 'error': 'Itinerary not found' }
    # TODO
    # if 'delete' in request.POST
    # delete itinerary
    # redirect to /
    context['itinerary'] = itinerary
    context['last_destination'] = itinerary['destinations'][-1]
    context['itineraryjson'] = json.dumps(itinerary)
    return context

@view_config(route_name='ajaxAbout', renderer='templates/ajax/about.jinja2')
def ajaxAbout(request):
    return globalContext(request)

@view_config(route_name='ajaxPrivacy', renderer='templates/ajax/privacy.jinja2')
def ajaxPrivacy(request):
    return globalContext(request)

@view_config(route_name='ajaxTerms', renderer='templates/ajax/terms.jinja2')
def ajaxTerms(request):
    return globalContext(request)

@view_config(route_name='ajaxSettings', renderer='templates/ajax/settings.jinja2')
def ajaxSettings(request):
    return globalContext(request)

@view_config(route_name='ajaxProfile', renderer='templates/ajax/profile.jinja2')
def ajaxProfile(request):
    request.user = api.getUser() # should be set automatically when logged in
    return { 'user': request.user }

@view_config(route_name='ajaxItineraries', renderer='templates/ajax/itineraries.jinja2')
def ajaxItineraries(request):
    itineraries = api.getItineraries(api.getUser())
    return { 'itineraries': itineraries }

@view_config(route_name='ajaxLogin', renderer='templates/ajax/login.jinja2')
def ajaxLogin(request):
    return globalContext(request)

@view_config(route_name='ajaxSignup', renderer='templates/ajax/signup.jinja2')
def ajaxSignup(request):
    return globalContext(request)

@view_config(route_name='ajaxContact', renderer='templates/ajax/contact.jinja2')
def ajaxContact(request):
    return globalContext(request)

@view_config(route_name='ajaxHelp', renderer='templates/ajax/help.jinja2')
def ajaxHelp(request):
    return globalContext(request)

@view_config(route_name='ajaxShare', renderer='templates/ajax/share.jinja2')
def ajaxShare(request):
    return globalContext(request)

@view_config(route_name='ajaxFormSave')
def ajaxFormSave(request):
    # TODO
    # save itinerary
    # called on click button save on search.js on existing itinerary
    # handled by jquery on search.js
    # return empty on OK response
    return globalContext(request)

@view_config(route_name='ajaxFormDelete')
def ajaxFormDelete(request):
    # TODO
    # delete itinerary
    # called on click delete on itineraries modal
    # handled by jquery on itineraries.js
    # return empty on OK response
    return globalContext(request)

@view_config(route_name='ajaxFormLogin')
def ajaxFormLogin(request):
    if 'username' in request.POST and 'password' in request.POST:
        # call api to login
        auth = api.authenticate(request.POST['username'], request.POST['password'])
        # add auth token to session
        request.session['auth_token'] = auth['token']
        # get api user
        user = api.getUser(username)
        # add user to session
        request.session['auth_user'] = user
    # redirect to /
    return HTTPFound(location='/')

@view_config(route_name='logout')
def logout(request):
    if 'auth_token' in request.session:
        # call api to invalidate auth token (logout)
        self.logout(request.session['auth_token'])
        # delete auth token from session
        del request.session['auth_token']
        # delete user from session
        del request.session['auth_user']
    # redirect to /
    return HTTPFound(location='/')

@view_config(route_name='ajaxFormSettings')
def ajaxFormSettings(request):
    # TODO
    # call api to save settings
    # called on click save on settings modal
    # handled by jquery on settings.js
    # return empty on OK response
    return globalContext(request)

@view_config(route_name='ajaxFormSignup')
def ajaxFormSignup(request):
    if 'username' in request.POST and 'password' in request.POST and 'email' in request.POST:
        # call api to create user
        user = api.createUser(request.POST['username'], request.POST['password'], request.POST['email'])
        # call api to login
        auth = api.authenticate(request.POST['username'], request.POST['password'])
        # add auth token to session
        request.session['auth_token'] = auth['token']
        # add user to session
        request.session['auth_user'] = user
    # redirect to /
    return HTTPFound(location='/')
