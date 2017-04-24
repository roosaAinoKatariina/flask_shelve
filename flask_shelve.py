import fcntl
import shelve
import json
import flask
import glob
import os
import traceback

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
    db=shelve.open("shelves/{}".format(collection))
    return db,lockfile

def close_and_unlock_collection(db,lockfile):
    db.close()
    fcntl.lockf(lockfile,fcntl.LOCK_UN) #Release lock
    lockfile.close()

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

@app.route('/set/<collection>/<key>', methods=['GET'])
def set_key(collection,key):
    if flask.request.args.get("value",None) is not None:
        valuejs=flask.request.args.get("value")
        try:
            value=json.loads(valuejs)
        except:
            return flask.abort(400,"could not decode value json")
        db,lockfile=lock_and_open_collection(collection)
        db[key]=value
        close_and_unlock_collection(db,lockfile)
        resp=flask.Response(valuejs,content_type="application/json")
        resp.headers["Access-Control-Allow-Origin"]="*"
        return resp
    else:
        return flask.abort(400,"no value given")

@app.route('/list/<collection>', methods=['GET'])
def list_collection(collection):
    db,lockfile=lock_and_open_collection(collection)
    value=json.dumps(dict(db))
    close_and_unlock_collection(db,lockfile)
    return flask.Response(value,content_type="application/json")

@app.route('/listall', methods=['GET'])
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
