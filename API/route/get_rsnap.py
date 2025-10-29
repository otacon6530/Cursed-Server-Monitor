from functions.module1 import get_db_connection
from flask import Flask, jsonify, render_template, request
import platform
import pyodbc
from metric_modules import get_cpu_usage, get_rsnapshots, get_uptime, get_all_services_status, get_service_status

def get_rsnap():
    data = get_rsnapshots()
    return jsonify(data)