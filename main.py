from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from __init__ import create_app,db
import logging
# logging.basicConfig(filename="newfile.log",format='%(asctime)s %(message)s',filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.debug("Harmless debug Message")
logger.info("Just an information")
logger.warning("Its a Warning")
logger.error("Did you try to divide by zero")
logger.critical("Internet is down")
main=Blueprint('main',__name__)
@main.route('/')
def index():
    return render_template('index.html')
@main.route('/profile')
def profile():
    return render_template('profile.html')
app=create_app()
if __name__=='__main__':
    with app.app_context():
        db.create_all() #create sql database
    app.run(debug=True)