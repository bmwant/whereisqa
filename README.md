## whereisqa

[![](https://img.shields.io/travis/bmwant/whereisqa.svg)](https://travis-ci.org/bmwant/whereisqa)


Latest updated info about current infrastructure


### Features

* TODO

### Development

Examples of using [Poetry](https://poetry.eustace.io/)

```bash
$ pyenv local 3.7.2
$ poetry init
$ poetry add
$ poetry add --dev tox
$ poetry install
$ poetry update
```

### Deployment

```
$ heroku create
$ heroku buildpacks:add heroku/python
$ heroku buildpacks:add heroku/nodejs
$ heroku config:set AWS_ACCESS_KEY_ID='<your-key-id>'
$ heroku config:set AWS_SECRET_ACCESS_KEY='<your-secret-key'
$ heroku config:set NODE_ENV=test
$ heroku config:set NODE_MODULES_CACHE=false
$ heroku config:set NODE_VERBOSE=true
$ heroku config:set AUTH_USERNAME='<your-secret-username>'
$ heroku config:set AUTH_PASSWORD='<your-secret-password>'
```
and then (do the same for redeploys)
```
$ git push heroku master
```

### Donate

Help Mel Gibson get his son back! [Do it right now!](https://gimmebackmyson.herokuapp.com/)
