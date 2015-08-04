from pyramid.view import view_config
from spinalcordweb.models import models
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
import os
from ..forms import form_render
from cornice import Service
from cornice.resource import resource, view
from ..cfg import FILE_REP_TMP
import gzip
from pyramid.httpexceptions import HTTPFound
import shutil

'''
Getter:
->Collection of files for an user
->The path for a specific file
Post:
->Add a file for an user
Delete:
->Delete a specific file
?Get:
->Show a file into the viewer?
'''
@resource(collection_path='/users/{user_id}/files', path='/users/{user_id}/files/{file_id}')
class File(object):

    def __init__(self, request):
        self.request = request

    @view(renderer='myfiles.mako')
    def collection_get(self):
        userid = self.request.matchdict['user_id']
        session = self.request.db
        return {'user':session.query(models.File).filter(models.File.user_id==userid).all()}

    @view(renderer='json')
    def get(self):
        userid = self.request.matchdict['user_id']
        fileid = self.request.matchdict['file_id']
        session = self.request.db
        #@TODO: launch Brainbrowser here? or use this functiton to call brainbrowser somewhere else
        return {'file_path':session.query(models.File).filter(models.File.user_id==userid).filter_by(id=fileid).first().localpath}

    @view(renderer='myfiles.mako')
    def delete(self):
        session = self.request.db
        userid = self.request.matchdict['user_id']
        fileid = self.request.matchdict['file_id']
        #Find the file in the database
        file_to_delete = session.query(models.File).filter_by(id=fileid).first()
        #Delete the entry
        session.delete(file_to_delete)
        session.commit()
        return {'user':session.query(models.File).filter(models.File.user_id==userid).all()}


@view_config(route_name='myfiles', renderer='myfiles.mako',
             permission='user')
def list_files(context, request):
    session = request.db
    userid = request.unauthenticated_userid #return the user.id without doing again the identification process
    return {'user':session.query(models.File).filter(models.File.user_id==userid).all()}


@view_config(route_name='displayFile', renderer='brainbrowser.mako',request_method='POST',
             permission='user')
def display_file(context,request):
    return {'form':form_render,'file_path':request.POST['go_viewer']}

@view_config(route_name='deleteFile', renderer='myfiles.mako',request_method='POST',
             permission='user')
def delete_file(context,request):
    #request a new session
    session = request.db
    userid = request.unauthenticated_userid #return the user.id without doing again the identification process
    #Find the file in the database
    file_to_delete = session.query(models.File).filter_by(id=request.POST['delete_file']).first()

    #Delete the file on the server
    # @TODO Write a function to remove the file on the server
    # @TODO Add a tag in the model for 'deleted' and remove the file one week after
    #os.remove(os.path.abspath(file_to_delete.serverpath))

    #Delete the entry
    session.delete(file_to_delete)
    session.commit()
    return {'user':session.query(models.File).filter(models.File.user_id==userid).all()}