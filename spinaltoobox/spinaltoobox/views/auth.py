from pyramid.view import view_config, forbidden_view_config
from .forms import login_form_render
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from ..models.models import User

@view_config(route_name='signin', renderer='string', request_method='POST')
def signin(request):
    first_name = request.POST.get('first_name')
    session = request.db
    if first_name:
        user = User.by_name(first_name, session)
        print(user.password)
        print(request.POST.get('first_name'))
        print(request.POST.get('password'))
        if user and user.verify_password(request.POST.get('first_name')):
            headers = remember(request, user.first_name)
        else:
            headers = forget(request)
    else:
        headers = forget(request)
    return HTTPFound(location=request.route_url('upload'),
                     headers=headers)

@view_config(route_name='signup', renderer='signup.mako', request_method='POST')
def signup(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    password = request.POST.get('password')

    session = request.db
    new_user = User(first_name=first_name,last_name=last_name,email=email,password=password)
    session.add(new_user)
    session.commit()
    return HTTPFound(location=request.route_url('signin'))

@view_config(route_name='signout', renderer='string')
def sign_out(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('home'),
                     headers=headers)\

@view_config(route_name='signin', renderer='signin.mako')
@forbidden_view_config(renderer='signin.mako')
def signin(context,request):
    return {}