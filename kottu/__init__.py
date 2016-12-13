from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('kottu.cfg')

import kottu.database
import kottu.models
import kottu.views
