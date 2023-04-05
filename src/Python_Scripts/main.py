from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/handle_form_data": {"origins": "*"}}, supports_credentials=True)

@app.route('/handle_form_data', methods=['POST'])
@cross_origin()
def handle_form_data():
    print("starting...")
    login_informatoin = request.form['login_informatoin']
    devices = request.form['devices']
    tool_config_script = request.form['tool_config_script']

    #TODO Convert tool_config_script to plain text commands
    data = config()
    return_data = {
        'success': True,
        'message': "Devices were successfully configured",
        'data': data

    }
    print("returning data")
    return jsonify(return_data)

def config():
    return "success"


if __name__ == '__main__':
    app.run()

