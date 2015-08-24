__author__ = 'willispinaud'

from pyramid.view import view_config
from ..models import models
from cornice.resource import resource, view
from cornice import Service
from .. import cfg
from .. import controler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import jsonpickle
import importlib
import logging
import os
import pkgutil
import psutil
import platform
import queue
import shutil
import subprocess
import signal
import sys
import time
import threading
import json
import pickle

sctoolbox = Service('sctoolbox',
                 '/sctoolbox',
                 'communication with the toolbox')

@sctoolbox.get(renderer='string')
def sctoolbox_get(request):
    '''
    :param request:
    :return: Return a list of all the sctools which have a get_parser
    '''
    logging.basicConfig(level=logging.DEBUG)
    session = request.db
    #PluginUpdater(session=session, script_path="/Users/willispinaud/Dropbox/Amerique/Montreal/spinalcordtoolbox/scripts", reload=True)
    rt = session.query(models.RegisteredTool).all()
    # rt = session.query(models.RegisteredTool).first() #DEBUG !!!
    return jsonpickle.dumps(rt)

@sctoolbox.post()
def sctoolbox_post(request):
    '''
    :param request.inputs: I guess it's a useless field
    :param request.args: Args selected by the usergit pull
    :param request.tool_name: the tool selected by the user
    :return:
    '''

    session=request.db

    plugins_path = cfg.SPINALCORD_BIN


    try:
        inputs = request.json_body['inputs']
        options = request.json_body['args']
        tool_name = request.json_body['tool_name']

        rt = session.query(models.RegisteredTool).filter(models.RegisteredTool.name == tool_name).first()

        # update the RT object with user value
        for o in rt.options.values():
            for i in options:
                if o.get("order") == int(i):
                    o["value"] = options[i]

    except KeyError:
        rt = jsonpickle.loads(request.body.decode('utf-8'))




    if rt:

        tbr = controler.ToolboxRunner(
        controler.SCTExec(registered_tool=rt),
        plugins_path, 1)

    tbr.run()
    return {}






# pu._load_plugins(None, "/home/poquirion/neuropoly/spinalcordtoolbox/scripts")





