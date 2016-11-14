# Run a test server.
from app import app
app.app.run(host='192.168.0.7', port=8000, debug=True)
