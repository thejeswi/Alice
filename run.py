#!flask/bin/python
from app.models import *

from app.views import *
app.config.from_pyfile('local.cfg')

db.create_all()


settings = [["server-name","Alice"],["adminName","admin"],["password","password"]]


config = Config.query.all()
        
if not config:
    for setting in settings:
        newConfig = Config(setting[0],setting[1])
        db.session.add(newConfig)
    db.session.commit()
    db.session.close()
    config = Config.query.all()
    print "Wrote new config"

app.run()
