
from flask import Flask, jsonify

app = Flask(__name__)

class API:
    logger = None

    @app.route('/api/data', methods=['GET'])
    def data():
        if(API.logger):
            return jsonify(API.logger.data_record)
        return jsonify({})

    def runAPI(self, logger_obj):
        API.logger = logger_obj
        app.run(debug=True, port=5005)
