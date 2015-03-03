from pyramid.view import view_config

@view_config(route_name='home', renderer='templates/home.jinja2')
def home(request):
    return {'project': 'LamaWeb'}

@view_config(route_name='search', renderer='templates/search.jinja2')
def search(request):
    return {'project': 'LamaWeb'}
