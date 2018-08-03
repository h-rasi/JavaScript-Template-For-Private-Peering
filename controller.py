from flask import Flask, render_template, request, send_from_directory, url_for, redirect, jsonify
import yaml,os,sys,json
from wtforms import Form, FloatField, validators, StringField
from wtforms.validators import DataRequired, Required
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
from subprocess import call, Popen

errordict={
    '1000' :'No Such Interface in Switch',
    '200' :'Wrong VTP Server Address...IT Is in Client Mode...Please Check Again',
    '151':'Not Such IP Address',
    '166' :'VTP Server IP Address is not True'

}

def script(json1):
    with open('../out.json','w') as f:
        conf = json.dump(json1,f,indent=2)
    a = call(["python3", "../PrivatePeering.py"])
    print("return error {}".format(a))
    return a


app = Flask(__name__,static_url_path='/home/hoss/netmiko/python_tests/jinja_temp/static')

@app.route("/")
def hello():
    return "hello world"

@app.route('/viewplain', methods=['GET'])
def send_html():
    return send_from_directory('/home/hoss/netmiko/python_tests/jinja_temp/templates','view_plain.html')


@app.route('/result', methods=['POST'])
def json_form():
    json1 = request.get_json()
    value = script(json1)
    if value != 0:
        return jsonify({
            'status': 'error',
            'message':errordict[str(value)]
            }
        )
    return 'The New Peering Configured succesfully'


if __name__ == '__main__':
    app.run(debug=True,threaded=True)
