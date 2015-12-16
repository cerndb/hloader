from hloader.backend.api import app



@app.route('/api/v1')
def api_v1():
    return "api_v1"
