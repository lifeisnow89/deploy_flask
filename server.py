from flask_app import app
from flask_app.controllers import users
from flask_app.models import user_model
from flask_app.models import wine_model
#import requests



if __name__=="__main__":
    app.run(debug=True)