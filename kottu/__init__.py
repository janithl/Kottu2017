from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('kottu.cfg')

import kottu.utils
import kottu.database
import kottu.models
import kottu.views
import kottu.cli
