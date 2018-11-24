# packhack

The best packhack client.
We ([@randombenj](https://github.com/randombenj) and [@fliiiix](https://github.com/fliiiix))
made third place with this bot. Special thanks to [@timofurrer](https://github.com/timofurrer) 🎉
for helping out.


[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

#### You will need...

* a working Python 3.6 development environment ([getting started guide](http://hackercodex.com/guide/python-development-environment-on-mac-osx/))
* experience [deploying Python apps to Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#introduction)
* [pip](https://pip.pypa.io/en/latest/installing.html) to install Python dependencies

## Running the Packhack Locally


1) Clone repo to your development environment:
```
git clone git@github.com:randombenj/packhack.git
```

2) Create a virtualenv
```
virtualenv env
source env/bin/activate
```

3) Install dependencies using [pip](https://pip.pypa.io/en/latest/installing.html):
```
pip install -r requirements.txt
```

4) Run local server:
```
python3 -m app
```

5) Test client in your browser: [http://localhost:8080](http://localhost:8080).

6) Test against other bots
Use [python_local_game](https://github.com/stairch/hslu_18hs_stair_pachack_python_local_game). Hints start this app fist and then run `python3 capture.py`. Also use the config in
`settings.ini`.

## Deploying to Heroku

1) Create a new Heroku app (On Windows use Commandline or PowerShell):
```
heroku create [APP_NAME] --region eu
```

2) Deploy code to Heroku servers:
```
git push heroku master
```

3) Open Heroku app in browser:
```
heroku open
```
or visit [http://APP_NAME.herokuapp.com](http://APP_NAME.herokuapp.com).

4) View server logs with the `heroku logs` command:
```
heroku logs --tail
```
