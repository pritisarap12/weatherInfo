# Run a test server.
from app import app
import logging
logging.basicConfig(filename='info.log',level=logging.DEBUG)
app.app.run(host='0.0.0.0', port=8000, debug=True)
