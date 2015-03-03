from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('search', '/search')
    config.add_route('logout', '/logout')
    config.add_route('itinerary', '/itinerary/{id}')
    config.add_route('ajaxAbout', '/ajax/about')
    config.add_route('ajaxPrivacy', '/ajax/privacy')
    config.add_route('ajaxTerms', '/ajax/terms')
    config.add_route('ajaxSettings', '/ajax/settings')
    config.add_route('ajaxProfile', '/ajax/profile')
    config.add_route('ajaxItineraries', '/ajax/itineraries')
    config.add_route('ajaxLogin', '/ajax/login')
    config.add_route('ajaxSignup', '/ajax/signup')
    config.add_route('ajaxContact', '/ajax/contact')
    config.add_route('ajaxHelp', '/ajax/help')
    config.add_route('ajaxShare', '/ajax/share')
    config.add_route('ajaxFormSave', '/ajax/form/save')
    config.add_route('ajaxFormSettings', '/ajax/form/settings')
    config.add_route('ajaxFormDelete', '/ajax/form/delete')
    config.add_route('ajaxFormLogin', '/ajax/form/login')
    config.add_route('ajaxFormSignup', '/ajax/form/signup')
    config.scan()
    return config.make_wsgi_app()
