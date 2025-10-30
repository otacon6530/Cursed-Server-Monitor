from flask import Flask
from flask_cors import CORS
from route.get_cpu_usage_history import get_cpu_usage_history
from route.get_metrics import get_metrics
from route.set_metrics import set_metrics
from route.get_servers import get_servers
from route.get_hostname import get_hostname
from route.get_rsnap import get_rsnap

app = Flask(__name__)
CORS(app)

#Add URL rules
#app.add_url_rule("/", view_func=index)
app.add_url_rule('/api/metrics', view_func=get_metrics, methods=['GET'])
app.add_url_rule('/api/cpu-usage', view_func=get_cpu_usage_history, methods=['GET'])
app.add_url_rule('/api/get-servers', view_func=get_servers, methods=['GET'])
app.add_url_rule('/api/hostname', view_func=get_hostname, methods=['GET'])
app.add_url_rule('/api/rsnap', view_func=get_rsnap, methods=['GET'])
app.add_url_rule('/api/metrics', view_func=set_metrics, methods=['POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)