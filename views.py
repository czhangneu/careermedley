__author__ = 'onyekaigabari'


# import modules
import os
from flask import (Flask, render_template, request, redirect, session, g,
                   flash, send_from_directory, abort)
from flask_bootstrap3 import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

# custom static directories
STATIC_DIRS = (
    os.path.join(ROOT_DIR, 'static/assets'),
    #os.path.join(ROOT_DIR, 'static/js'),
)

# view response functions
@app.route('/')
def index():
    return render_template('main.html')

@app.route('/<path:filename>')
def send_file(filename):
    print 'got message, root-dir: %s, file: %s' % (ROOT_DIR, filename)
    for directory in STATIC_DIRS:
        if os.path.isfile(os.path.join(directory, filename)):
            return send_from_directory(directory, filename)

if __name__ == '__main__':
    app.run(debug=True)

