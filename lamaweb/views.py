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
        'username': request.session['auth_user']['username'] if 'auth_user' in request.session else None,
    }

@view_config(context=Exception)
def error_view(exc, request):
    response = render_to_response(('json' if 'ajax' in request.url else 'templates/home.jinja2'), {'error': exc.args[0] if isinstance(exc, api.ApiError) else "Unknown" + ((" ("+ exc.args[0] + ")") if exc.args else "")}, request=request)
    if exc.args and '404' in exc.args[0]:
        response.status_int = 404
    elif exc.args and '400' in exc.args[0]:
        response.status_int = 400
    else:
        response.status_int = 500
    return response

@view_config(route_name='home', renderer='templates/home.jinja2')
def home(request):
    return globalContext(request)

@view_config(route_name='search', renderer='templates/search.jinja2')
def search(request):
    context = globalContext(request)
    if 'departure' in request.POST:
        # create itinerary
        itinerary = api.createItinerary(request,
                                        departure=request.POST['departure'],
                                        destination=(request.POST['destination-0'] if 'destination-0' in request.POST else None))
        # if there's more destinations, add them all
        i = 1
        while ('destination-' + str(i)) in request.POST:
            itinerary = api.addDestination(request, str(itinerary['id']), request.POST['destination-' + str(i)])
            i += 1
        # redirect to the created itinerary
        return HTTPFound(location='/itinerary/' + str(itinerary['id']))
    # return empty search form
    return context

@view_config(route_name='itinerary', renderer='templates/search.jinja2')
def itinerary(request):
    context = globalContext(request)
    # get itinerary
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

    # if a form to edit the form had been submitted
    if ('name' in request.POST and request.POST['name']) or 'favorite' in request.POST or 'removefavorite' in request.POST:
        # edit name or favorite
        itinerary = api.editItinerary(request,
                                      itinerary=str(itinerary['id']),
                                      favorite=('true' if 'favorite' in request.POST else ('false' if 'removefavorite' in request.POST else None)),
                                      name=(request.POST['name'] if 'name' in request.POST and request.POST['name'] else None))
    elif 'delete' in request.POST:
        # delete itinerary
        api.deleteItinerary(request, itinerary=str(itinerary['id']))
        # redirect to homepage after itinerary deleted
        return HTTPFound('/')
    # return itinerary
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

@view_config(route_name='ajaxSponsors', renderer='templates/ajax/users.jinja2')
def ajaxSponsors(request):
    context = globalContext(request)
    context['title'] = 'Lama Urbain Sponsors'
    context['flaticon'] = 'flag'
    context['users'] = api.getUsers(request, sponsored='true')
    return context

@view_config(route_name='ajaxUser', renderer='templates/ajax/itineraries.jinja2')
def ajaxUser(request):
    username = request.matchdict.get("username", None)
    if not username:
        request.response.status = 400
        return { 'error': 'Invalid User' }
    context = globalContext(request)
    context['user'] = api.getUser(request, username=username)
    context['itineraries'] = api.getItineraries(request, username=username, favorite='true')
    return context

@view_config(route_name='ajaxSettings', renderer='templates/ajax/settings.jinja2')
def ajaxSettings(request):
    return globalContext(request)

@view_config(route_name='ajaxProfile', renderer='templates/ajax/profile.jinja2')
def ajaxProfile(request):
    return { 'user': request.session['auth_user'] }

@view_config(route_name='ajaxItineraries', renderer='templates/ajax/itineraries.jinja2')
def ajaxItineraries(request):
    # search itineraries that are favorited by the user
    itineraries = api.getItineraries(request, username=request.session['auth_user']['username'], favorite='true')
    return { 'itineraries': itineraries }

@view_config(route_name='ajaxHistory', renderer='templates/ajax/itineraries.jinja2')
def ajaxHistory(request):
    # show the history of all the itineraries searched by the user (regardless favorites)
    itineraries = api.getItineraries(request, username=request.session['auth_user']['username'])
    return { 'itineraries': itineraries, 'history': True }

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

@view_config(route_name='ajaxFormSettings', renderer='json')
def ajaxFormSettings(request):
    if ('password' in request.POST and request.POST['password']) or ('email' in request.POST and request.POST['email']):
        user = api.editUser(request, request.session['auth_user']['username'],
                            password=request.POST.get('password', None),
                            email=request.POST.get('email', None))
        request.session['auth_user'] = user
        return {}
    request.response.status = 400
    return { 'error': 'Missing password or email' }

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
    # add a destination to an existing itinerary
    if 'destination' in request.POST and 'itinerary' in request.POST:
        return api.addDestination(request, itinerary=request.POST['itinerary'], destination=request.POST['destination'])
    request.response.status = 400
    return { 'error': 'Missing parameter' }

@view_config(route_name='ajaxEditDestination', renderer='json')
def ajaxFormEditDestination(request):
    # edit an existing destination in an existing itinerary
    if 'itinerary' in request.POST and 'destination' in request.POST and 'position' in request.POST:
        return api.editDestination(request, itinerary=request.POST['itinerary'],
                                   destination=request.POST['destination'],
                                   position=request.POST['position'])
    request.response.status = 400
    return { 'error': 'Missing parameter' }

@view_config(route_name='ajaxDeleteDestination', renderer='json')
def ajaxFormDeleteDestination(request):
    # delete a destination in an itinerary
    if 'itinerary' in request.POST and 'position' in request.POST:
        return api.deleteDestination(request, itinerary=request.POST['itinerary'],
                                     position=request.POST['position'])
    request.response.status = 400
    return { 'error': 'Missing parameter' }

@view_config(route_name='ajaxEditItinerary', renderer='json')
def ajaxEditItinerary(request):
    # edit the departure in an existing itinerary
    if 'itinerary' in request.POST and 'departure' in request.POST:
        return api.editItinerary(request, itinerary=request.POST['itinerary'], departure=request.POST['departure'])

@view_config(route_name='ajaxDeleteItinerary', renderer='json')
def ajaxDeleteItinerary(request):
    # delete an itinerary (from list of itineraries)
    if 'itinerary' in request.POST:
        api.deleteItinerary(request, itinerary=request.POST['itinerary'])
    return {}
