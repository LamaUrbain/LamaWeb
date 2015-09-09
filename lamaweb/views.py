from pyramid.view import view_config
import pyramid.threadlocal
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render_to_response
import json
import api

def globalContext(request):
    return {
        'apiurl': pyramid.threadlocal.get_current_registry().settings['apiurl'],
        'authentified': True if 'auth_token' in request.session else False,
        'user': request.session['auth_user'] if 'auth_user' in request.session else None,
    }

# @view_config(context=Exception)
# def error_view(exc, request):
#     response = render_to_response(('json' if 'ajax' in request.url else 'templates/home.jinja2'), {'error': exc.args[0] if isinstance(exc, api.ApiError) else "Unknown" + ((" ("+ exc.args[0] + ")") if exc.args else "")}, request=request)
#     if exc.args and '404' in exc.args[0]:
#         response.status_int = 404
#     elif exc.args and '400' in exc.args[0]:
#         response.status_int = 400
#     else:
#         response.status_int = 500
#     return response

@view_config(route_name='home', renderer='templates/home.jinja2')
def home(request):
    return globalContext(request)

@view_config(route_name='search', renderer='templates/search.jinja2')
def search(request):
    context = globalContext(request)
    if 'departure' in request.POST:
        itinerary = api.createItinerary(request,
                                        departure=request.POST['departure'],
                                        name=(request.POST['name'] if 'name' in request.POST else None),
                                        destination=(request.POST['destination-0'] if 'destination-0' in request.POST else None),
                                        favorite=(True if 'name' in request.POST else False))
        # i = 1
        # while ('destination-' + str(i)) in request.POST:
        #     itinerary = api.addDestination(request, str(itinerary['id']), request.POST['destination-' + str(i)])
        #     i += 1
        return HTTPFound(location='/itinerary/' + str(itinerary['id']))
    elif 'name' in request.POST or 'favorite' in request.POST or 'removefavorite' in request.POST:
        api.editItinerary()
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
    itinerary = api.getItinerary(request, id)
    if not itinerary:
        request.response.status = 404
        return { 'error': 'Itinerary not found' }
    # TODO
    # if 'delete' in request.POST
    # delete itinerary
    # redirect to /
    context['itinerary'] = itinerary
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
    return { 'user': request.session['auth_user'] }

@view_config(route_name='ajaxItineraries', renderer='templates/ajax/itineraries.jinja2')
def ajaxItineraries(request):
    itineraries = api.getItineraries(request, username=request.session['auth_user']['username'])
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
        auth = api.authenticate(request, username=request.POST['username'], password=request.POST['password'])
        # add auth token to session
        request.session['auth_token'] = auth['token']
        # get api user
        user = api.getUser(request, username=request.POST["username"])
        # add user to session
        request.session['auth_user'] = user
    # redirect to /
    return HTTPFound(location='/#profile')

@view_config(route_name='logout')
def logout(request):
    if 'auth_token' in request.session:
        # call api to invalidate auth token (logout)
        api.logout(request)
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
        user = api.createUser(request, request.POST['username'], request.POST['password'], request.POST['email'])
        # call api to login
        auth = api.authenticate(request, request.POST['username'], request.POST['password'])
        # add auth token to session
        request.session['auth_token'] = auth['token']
        # add user to session
        request.session['auth_user'] = user
    # redirect to /
    return HTTPFound(location='/')

@view_config(route_name='ajaxAddDestination', renderer='json')
def ajaxFormAddDestination(request):
    if 'destination' in request.POST and 'itinerary' in request.POST:
        return api.addDestination(request, itinerary=request.POST['itinerary'], destination=request.POST['destination'])
    request.response.status = 400
    return { 'error': 'Missing parameter' }

@view_config(route_name='ajaxEditDestination', renderer='json')
def ajaxFormEditDestination(request):
    if 'itinerary' in request.POST and 'destination' in request.POST and 'position' in request.POST:
        return api.editDestination(request, itinerary=request.POST['itinerary'],
                                   destination=request.POST['destination'],
                                   position=request.POST['position'])
    request.response.status = 400
    return { 'error': 'Missing parameter' }

@view_config(route_name='ajaxDeleteDestination', renderer='json')
def ajaxFormDeleteDestination(request):
    if 'itinerary' in request.POST and 'position' in request.POST:
        return api.deleteDestination(request, itinerary=request.POST['itinerary'],
                                     position=request.POST['position'])
    request.response.status = 400
    return { 'error': 'Missing parameter' }

@view_config(route_name='ajaxEditItinerary', renderer='json')
def ajaxEditItinerary(request):
    if 'itinerary' in request.POST and 'departure' in request.POST:
        return api.editItinerary(request, itinerary=request.POST['itinerary'], departure=request.POST['departure'])
    if 'itinerary' in request.POST and 'favorite' in request.POST:
        return api.editItinerary(request, itinerary=request.POST['itinerary'], favorite=request.POST['favorite'])

@view_config(route_name='ajaxDeleteItinerary', renderer='json')
def ajaxDeleteItinerary(request):
    if 'itinerary' in request.POST:
        api.deleteItinerary(request, itinerary=request.POST['itinerary'])
    return HTTPFound(location='/#itineraries')
