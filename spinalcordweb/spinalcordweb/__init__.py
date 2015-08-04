from pyramid.config import Configurator
from pyramid import authentication, authorization

from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from .resource import APIRoot
from .security import get_principals
from .models.models import User
from configparser import ConfigParser
import logging

from .resource import APIRoot
#from .security import get_principals
from .models.models import User
from .controler import PluginUpdater

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .security import SecurityFactory

log = logging.getLogger(__name__)

def db(request):
    """every request will have a session associated with it. and will
    automatically rollback if there's any exception in dealing with
    the request
    """
    maker = request.registry.dbmaker
    session = maker()

    def cleanup(request):
        if request.exception is not None:
            session.rollback()
        else:
            session.commit()
        session.close()

    request.add_finished_callback(cleanup)

    return session

def authenticated_user(request):
    def x():
        return request.db.query(User).filter_by(id=request.authenticated_userid).first()
    return x

def config_static(config):
    config.add_static_view('static', 'static', cache_max_age=3600)


def config_jinja2(config):
    config.include('pyramid_jinja2')
    config.include('pyramid_mako')
    config.add_jinja2_renderer('.html')
    config.add_jinja2_search_path('templates', name='.html')


def config_mailer(config):
    config.include('pyramid_marrowmailer')
    config.include('pyramid_tm')

def config_db(config, settings):
    # configure database with variables sqlalchemy.*
    engine = engine_from_config(settings, prefix="sqlalchemy.")
    config.registry.dbmaker = sessionmaker(bind=engine)

    # add db session to request
    config.add_request_method(db, reify=True)

def config_plugins(config):
    PluginUpdater(config)

def config_routes(config):

    config.add_route('404', '/404')
    config.add_route('403', '/403')
    config.add_route('myfiles','/myfiles',
                 factory='spinalcordweb.security.SecurityFactory')
    config.add_route('displayFile','/display_file',
                 factory='spinalcordweb.security.SecurityFactory')
    config.add_route('deleteFile','/delete_file',
                 factory='spinalcordweb.security.SecurityFactory')
    config.add_route('brainbrowser','/viewer')
    config.add_route('upload','/upload',
                 factory='spinalcordweb.security.SecurityFactory')
    config.add_route('upload_nii','/upload_nii',
                 factory='spinalcordweb.security.SecurityFactory')
    config.add_route('contact','/contact')

    config.add_route('app','/app') #AngularJS test application
    config.add_route('generate_ajax_data', '/ajax_view') #Ajax test request
    config.add_route('homee', '/home') #Ajax test button

    config.add_route('home', '/')
    config.add_route('signin','/signin')
    config.add_route('signout','/signout')
    config.add_route('toolbox','/toolbox')
    config.add_route('signup','/signup')
    config.add_route('auth', '/sign/{action}')
    config.scan()
    config.add_route("api", '/api/*traverse', factory=APIRoot)

def config_auth_policy(config, settings):
    policy = authentication.AuthTktAuthenticationPolicy(settings['auth_secret'], get_principals, cookie_name="spinalcordweb_auth", hashalg="sha512")
    config.set_authentication_policy(policy)
    config.set_authorization_policy(authorization.ACLAuthorizationPolicy())

def config_secrets(settings):
    if "secrets" in settings:
        try:
            config = ConfigParser()
            config.read(settings["secrets"])
            settings.update(config.items("secrets"))
        except:
            log.warn("secrets were specificed in the configuration but could not be read\n\n%s" % settings.get("secrets", ""), exc_info=1)

def main(global_config, **settings):
    config_secrets(settings)
    config = Configurator(settings=settings)
    config_static(config)
    config_jinja2(config)
    config.include("cornice")
    config_db(config, settings)
    config_routes(config)
    config_auth_policy(config, settings)
    config_mailer(config)
    config.add_request_method(authenticated_user, reify=True)
    return config.make_wsgi_app()
