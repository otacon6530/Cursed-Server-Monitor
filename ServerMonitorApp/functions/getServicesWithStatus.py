import psutil
import platform
import subprocess

def getServicesWithStatus():
    """
    Returns a list of dicts: [{'name': <service_name>, 'status': <status>}]
    Cross-platform: uses systemctl on Linux, psutil on Windows.
    """
    services = []
    try:
        if platform.system().lower() == "windows":
            # Use psutil for Windows services
            for service in psutil.win_service_iter():
                info = service.as_dict()
                services.append({'name': info['name'], 'status': info['status']})
        elif platform.system().lower() == "linux":
            SYSTEMCTL = "/usr/bin/systemctl"
            result = subprocess.run(
                [SYSTEMCTL, 'list-units', '--type=service', '--all', '--no-pager', '--no-legend'],
                capture_output=True,
                text=True
            )
            for line in result.stdout.strip().split('\n'):
                if not line.strip():
                    continue
                parts = line.split()
                if len(parts) >= 4:
                    name = parts[0]
                    status = parts[3]
                    services.append({'name': name, 'status': status})
        else:
            services.append({'name': '[EXCEPTION]', 'status': 'Unsupported platform'})
    except Exception as e:
        services.append({'name': '[EXCEPTION]', 'status': str(e)})
    return services
