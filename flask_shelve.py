import fcntl
import shelve
import json
import flask
import glob
import os

app = flask.Flask(__name__)

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
        return flask.Response(json.dumps(value),content_type="application/json")
    except:
        return flask.abort(400)
    finally:
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
        return flask.Response(valuejs,content_type="application/json")
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
    return flask.Response(json.dumps(value),content_type="application/json")
   
if __name__ == u'__main__':
    app.run(debug=False)
