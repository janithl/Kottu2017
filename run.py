from kottu import app
import optparse

# debugger option
parser = optparse.OptionParser()
parser.add_option("--debug", action="store_true", dest="debug", help="Debug Application")
options, _ = parser.parse_args()

app.run(debug=options.debug)
