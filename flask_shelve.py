import fcntl
import shelve
import json
import flask
import glob
import os
import traceback
from flask import Flask, abort, request
import urllib.parse

app = flask.Flask(__name__)

def access_allowed(func):
    def wrapped_function(*args, **kwargs):
        resp=flask.make_response(func(*args,**kwargs))
        resp.headers['Access-Control-Allow-Origin']='*'
    return wrapped_function

def lock_and_open_collection(collection):
    for d in ("locks","shelves"):
        try:
            os.mkdir(d)
        except FileExistsError:
            pass
    lockfile=open("locks/{}.lock".format(collection),"w")
    fcntl.lockf(lockfile,fcntl.LOCK_EX) #Acquire lock
    db=shelve.open("shelves/{}".format(collection), writeback=True)
    return db,lockfile

def close_and_unlock_collection(db,lockfile):
    db.close()
    fcntl.lockf(lockfile,fcntl.LOCK_UN) #Release lock
    lockfile.close()

#@app.route('/get/<collection>/<key>', methods=['GET', 'POST'])
@app.route('/get/<collection>/<key>', methods=['GET'])
def get_key(collection,key):
    try:
        db,lockfile=lock_and_open_collection(collection)
        value=db.get(key,flask.request.args.get("default",None))
        close_and_unlock_collection(db,lockfile)
        db=None
        resp=flask.Response(json.dumps(value),content_type="application/json")
        resp.headers["Access-Control-Allow-Origin"]="*"
        return resp
    except:
        return flask.abort(400)
    finally:
        if db is not None:
            close_and_unlock_collection(db,lockfile)


@app.route('/set/<collection>/<key>/<textid>', methods=['POST'])
def set_key(collection,key,textid):

    if not request.json:
        abort(400)
    valuejs = request.json["value"]
    valuejs = urllib.parse.unquote(valuejs)
    valuepy = json.loads(valuejs)

    #open the dictionary
    db,lockfile=lock_and_open_collection(collection)
    if key not in db:
        print('No key yet')
        db[key] = {}
    db[key][textid] = valuepy
    close_and_unlock_collection(db,lockfile)
    resp=flask.Response(valuejs,content_type="application/json")
    resp.headers["Access-Control-Allow-Origin"]="*"
    return resp



@app.route('/list/<collection>', methods=['GET', 'POST'])
#@app.route('./local-new-code', methods=['GET', 'POST'])
def list_collection(collection):
    db,lockfile=lock_and_open_collection(collection)
    value=json.dumps(dict(db))
    close_and_unlock_collection(db,lockfile)
    resp=flask.Response(value,content_type="application/json")
    resp.headers["Access-Control-Allow-Origin"]="*"
    return resp

@app.route('/listall', methods=['GET', 'POST'])
def list_collections():
    collections=set(os.path.splitext(os.path.basename(f))[0] for f in  glob.glob("shelves/*"))
    value={}
    for collection in collections:
        db,lockfile=lock_and_open_collection(collection)
        value[collection]=dict(db)
        close_and_unlock_collection(db,lockfile)
        resp=flask.Response(json.dumps(value),content_type="application/json")
        resp.headers["Access-Control-Allow-Origin"]="*"
        return resp
    resp=flask.Response(json.dumps(value),content_type="application/json")
    resp.headers["Access-Control-Allow-Origin"]="*"
    return resp
   
if __name__ == u'__main__':
    app.run(debug=False)
