from pyramid.view import view_config
import api

@view_config(route_name='home', renderer='templates/home.jinja2')
def home(request):
    return {}

@view_config(route_name='search', renderer='templates/search.jinja2')
def search(request):
    context = {}
    if 'arrival' in request.GET:
        context['arrival'] = request.GET['arrival']
    if 'departure' in request.GET:
        context['departure'] = request.GET['departure']
    # TODO
    # if 'save' in request.POST
    # create new itinerary
    # redirect to itinerary
    return context

@view_config(route_name='itinerary', renderer='templates/search.jinja2')
def itinerary(request):
    di = request.matchdict
    id = di.get("id", None)
    if not id or not id.isdigit():
        request.response.status = 400
        return { 'error': 'Invalid Itinerary id' }
    id = int(id)
    itinerary = api.getItinerary(api.getUser(), id)
    if not itinerary:
        request.response.status = 404
        return { 'error': 'Itinerary not found' }
    # TODO
    # if 'delete' in request.POST
    # delete itinerary
    # redirect to /
    return {
        'itinerary': itinerary,
        'last_destination': itinerary['destinations'][-1],
    }

@view_config(route_name='ajaxAbout', renderer='templates/ajax/about.jinja2')
def ajaxAbout(request):
    return {}

@view_config(route_name='ajaxPrivacy', renderer='templates/ajax/privacy.jinja2')
def ajaxPrivacy(request):
    return {}

@view_config(route_name='ajaxTerms', renderer='templates/ajax/terms.jinja2')
def ajaxTerms(request):
    return {}

@view_config(route_name='ajaxSettings', renderer='templates/ajax/settings.jinja2')
def ajaxSettings(request):
    return {}

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
    return {}

@view_config(route_name='ajaxSignup', renderer='templates/ajax/signup.jinja2')
def ajaxSignup(request):
    return {}

@view_config(route_name='ajaxContact', renderer='templates/ajax/contact.jinja2')
def ajaxContact(request):
    return {}

@view_config(route_name='ajaxHelp', renderer='templates/ajax/help.jinja2')
def ajaxHelp(request):
    return {}

@view_config(route_name='ajaxShare', renderer='templates/ajax/share.jinja2')
def ajaxShare(request):
    return {}

@view_config(route_name='ajaxFormSave')
def ajaxFormSave(request):
    # TODO
    # save itinerary
    # called on click button save on search.js on existing itinerary
    # handled by jquery on search.js
    # return empty on OK response
    return {}

@view_config(route_name='ajaxFormDelete')
def ajaxFormDelete(request):
    # TODO
    # delete itinerary
    # called on click delete on itineraries modal
    # handled by jquery on itineraries.js
    # return empty on OK response
    return {}

@view_config(route_name='ajaxFormLogin')
def ajaxFormLogin(request):
    # TODO
    # call api to login
    # add auth token to session
    # get api user
    # add user to session
    # redirect to /
    return {}

@view_config(route_name='logout')
def logout(request):
    # TODO
    # call api to invalidate auth token (logout)
    # delete auth token from session
    # delete user from session
    # redirect to /
    return {}

@view_config(route_name='ajaxFormSettings')
def ajaxFormSettings(request):
    # TODO
    # call api to save settings
    # called on click save on settings modal
    # handled by jquery on settings.js
    # return empty on OK response
    return {}

@view_config(route_name='ajaxFormSignup')
def ajaxFormSignup(request):
    # TODO
    # call api to create user
    # call api to login
    # add auth token to session
    # get api user
    # add user to session
    # redirect to /
    return {}
