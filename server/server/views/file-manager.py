import os, zipfile
import io
from ..cfg import FILE_REP_TMP
from cornice import Service
import jsonpickle
from server.models import models
from pyramid import response
import zlib
#####
# AngularJS - File Tree
#####
tree = Service('tree',
                 '/tree/{uid}',
                 'generate the json for JSTree')

def path_to_db(path,session,tag):
    d = {'text': os.path.basename(path)}
    d['path'] = path #The absolute path, usefull to launch the SCToolbox
    d['rel_path'] = os.path.relpath(path)[7:] #The relative path, usefull to load volumes files into BrainBrowser
    if tag:
        d['parent'] = "#"
    else :
        d['parent'] = os.path.abspath(os.path.join(path, os.pardir))
    if os.path.isdir(path):
        d['type'] = "directory"
        d['children'] = [path_to_db(os.path.join(path,x),session,0) for x in os.listdir(path)]
        d['icon'] = "glyphicon glyphicon-folder-open"
    else:
        d['type'] = "file"
        d['icon'] = "glyphicon glyphicon-file"
        d['children'] = ""

    print (d['parent'])
    u = models.tree(rel_path = d['rel_path'],
            size = 0,
            text = d['text'],
            type = d['type'],
            id = d['path'],
            parent = d['parent'],
            icon = d['icon'])

    session.add(u)
    session.commit()

    return d

@tree.get()
def tree_get(request):
    '''

    :param request:
    :return:
    '''
    uid = request.matchdict['uid']
    session = request.db
    session.query(models.tree).delete()
    files = path_to_db(os.path.abspath(os.path.join(FILE_REP_TMP,uid)),session,1)
    fileTree = session.query(models.tree).all()
    filesT = []
    for file in fileTree:
        #print (jsonpickle.dumps(file))
        fileT = {'id': file.id}
        fileT['parent'] = file.parent
        fileT['icon'] = file.icon
        fileT['type'] = file.type
        fileT['path'] = file.id
        fileT['text'] = file.text
        fileT['rel_path'] = file.rel_path

        filesT.append(fileT)

    return filesT


@tree.post()
def tree_post(request):
    '''
    Post the new file tree and do the modification on the server side
    :param request:
    :return:
    '''
    return {}


download = Service('download',
                 '/download',
                 'Download a file or a folder')

@download.get()
def download_get(request):
    file_id = jsonpickle.loads(request.GET['id'])
    #test if the get argument is in the right format
    if type(file_id)==type([]):
        zip_filename = "isct_download.zip"
        # The zip compressor
        zf = zipfile.ZipFile(zip_filename, "w")
        for fpath in file_id:
            # Add files, rename it and add compression (zipfile.ZIP_DEFLATED)
            zf.write(fpath, arcname=os.path.basename(fpath), compress_type=zipfile.ZIP_DEFLATED)
        # Must close zip for all contents to be written
        zf.close()
        #TODO fix the file response, should have a real file not just the name of the zipfile in the root
        return response.FileResponse("isct_download.zip", request=request, cache_max_age=3000)
    else:
        return {'error':'argument error'}