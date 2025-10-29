from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import platform
import pyodbc
from metric_modules import get_cpu_usage, get_rsnapshots, get_uptime, get_all_services_status, get_service_status
from functions.module1 import get_db_connection

from route.get_cpu_usage_history import get_cpu_usage_history
from route.index import index
from route.get_metrics import get_metrics
from route.set_metrics import set_metrics
from route.get_servers import get_servers
from route.get_hostname import get_hostname
from route.get_rsnap import get_rsnap

app = Flask(__name__)
CORS(app)  # Enable CORS

#Add URL rules
app.add_url_rule("/", view_func=index)
app.add_url_rule('/api/metrics', view_func=get_metrics)
app.add_url_rule('/api/cpu-usage', view_func=get_cpu_usage_history)
app.add_url_rule('/api/get-servers', view_func=get_servers)
app.add_url_rule('/api/hostname', view_func=get_hostname)
app.add_url_rule('/api/rsnap', view_func=get_rsnap)
app.add_url_rule('/api/metrics', view_func=set_metrics)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)