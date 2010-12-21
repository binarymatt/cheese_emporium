=================
 Cheese Emporium
=================

A simple application to facilitate the serving of a static python
package index.  It borrows heavily from `BasketWeaver`.

Install
=======

pip install -e git+git://github.com/SurveyMonkey/cheese_emporium.git#egg=cheese_emporium


Running
=======

Configure Nginx
---------------

CheeseEmporium doesn't pretend to be good at serving flat
files. You'll need to configure another server to serve the files and
proxy to the app. We recommend nginx.

See `sample-nginx.conf` and replace `alias cheese_emporium/files;` and
`alias cheese_emporium/static` with your fileroot and static filepath.
`cheesectl` will announce whatever these values are on start::

 $ cheesectl -d
 FILE ROOT: /Users/whit/dev/hwler.build/var/emporium
 STATIC: /Users/whit/dev/hwler.build/src/cheese-emporium/cheese_emporium/static
 ...

Running (simple)
----------------

For a ingle threaded py package index::

 $ cheesectl -d


Running (more advanced)
-----------------------

Still single threaded, but configurable! 

 $ EMPORIUM_SETTINGS=./mysetting.py cheesectl


Running (more advanced)
-----------------------

Use pastedeploy to serve something you might use with others::

 $ pip install pastescript pastedeploy paste
 $ cp src/cheese_emporium/example.ini mycheese.ini
 $ vim mycheese.ini # edit as appropriate, save

The config looks like this::

 [app:main]
 use = egg:cheese_emporium
 settings = %(here)s/example-settings.py
 # fileroot = /path/to/root_of_index

 [server:main]
 use = egg:Paste#http
 host = 127.0.0.1
 port = 5000

Now serve with paster::

 $ paster serve mycheese.ini


How to use
==========

CheeseEmporium understand the upload interface of pypi. This means for
python2.6 and better you can setup your ~/.pypirc and then upload to
your emporium as you would pypi::

 [distutils]
    index-servers =
        pypi
        local


 [pypi]
    username:user
    password:secret

 [local]
    # your emporium
    username:user
    password:secret
    repository:http://mycheese


The you can upload a source ala::

  $  cd /myawesome-python-pkg
  $  python setup.py sdist upload -r local

The emporium currently doesn't do anything with the credentials
(patches welcome).

Now your package is available for install from your emporium::

  $ pip install -i http://mycheese/index/ Pylons
