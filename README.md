# flask_shelve

Little program for adding multiple-choice annotation capability to HTML, used to annotate UD trees (as a whole, not individual dependencies). If you want to annotate actual dependencies, maybe you want to try [ud-annotatrix](https://github.com/jonorthwash/ud-annotatrix).

# How to test:

    python3 flask_shelve.py

Opens a web app running on your local host which you can query like such:

    http://127.0.0.1:5000/listall

...of course there is nothing in there right now, so you get an empty document. Keep reading.

Open `test.html` in your browser and click around. When you click, the choices turn green, signalling that all went fine. Now when you open `http://127.0.0.1:5000/listall` you see the choices saved.

# How to deploy with your own data

Look at the source of `test.html`. The critical parts are:

## Load the javascript

```
<script type="text/javascript" src="flask_shelve.js"></script>
```

## Encode the choices

You insert into your html `<div>` elements which have the following properties:

* `class="flask_shelve"`
* `fstype="multichoice"`
* `fschoices="choice1|choice2|choice3|..."`
* `fscol="collectionname"` here collection name is a name of some collection of trees, or experiment, or something you need to identify this set of annotations
* `fsid="someid"` A unique annotation is identified by its collection and id within the collection. The ids need to be acceptable as html element identifiers, so do not use anything wild as identifiers.
* `fsmeta="anything else you want to store"`

Here's an example:

```
<div class="flask_shelve" fstype="multichoice" fschoices="Correct|Incorrect" fscol="test4" fsid="b1" fsmeta="mystuff">Yo some text</div>
```

## Create the annotation elements

After you create the '<div>' elements, you just tell `flask_shelve` to turn them into annotation choices like so:

```
<script type="text/javascript">
     APP_ROOT="http://127.0.0.1:5000";
     $(".flask_shelve").each(flask_shelve);
     initialize_values("test4");
</script>
```

Here `APP_ROOT` tells where `flask_shelve` is running and `initialize_values("test4")` tells to read annotation from the collection `test4` once the document is loaded. That way you can reload the document and all annotations will be preserved.

## Fully worked example

Just copy stuff from `test.html` and modify to your needs.

# How to query your annotations

The querying is URL-based and gives you, as json, all the data you have. Then you can do with it whatever you need to. It works like so:

http://127.0.0.1:5000/listall --- gives all data you have
http://127.0.0.1:5000/list/test4 --- all data from collection test4
http://localhost:5000/get/test4/b3 --- get annotation for id `b3` in collection `test4`
http://localhost:5000/set/test4/b3?value={"annotation":"correct"} --- set the annotation remembered for id `b3` in collection `test4`. The annotation can be anything you want, value is json. So you can remember the annotation itself, but in addition you can also store any values you like.

# How do I know it works?

Every time you click on a choice, the choice turns green if all went fine and the choice is stored. If it doesn't turn green, your annotation didn't get saved and you better investigate.

# Where's the data?

In the `shelves` directory. These are Python `shelve` module files. There are also `locks` files to go with every collection.

# Safety of deployment

This is certainly not safe to serve over a public connection because there is no authentication nor description, but should be perfectly fine to run local.

# Integration with UD



