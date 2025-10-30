from flask import jsonify
import platform

def get_hostname():
    data = {
        'hostname': platform.node(),
    }
    return jsonify(data)