import { updateElement } from './updateElement.js';

export async function loadMetricsForServer(server) {
    let APIServer = "http://localhost:5000"
    let response;
    let data;
    try {
        response = await fetch(APIServer + `/api/metrics?server=${encodeURIComponent(server)}`);
        data = await response.json();
    } catch (err) {
        // Handle error if needed
    }
    if (data.status == 'Active') {
        try {
            document.getElementById(`status-${server}-parent`).classList.add('active');
            document.getElementById(`status-${server}-parent`).classList.remove('inactive');
        } catch (err) {
            // Handle error if needed
        }
    } else {
        try {
            document.getElementById(`status-${server}-parent`).classList.add('inactive');
            document.getElementById(`status-${server}-parent`).classList.remove('active');

        } catch (err) {
            // Handle error if needed
        }
    }
    updateElement(`uptime-${server}`, data.uptime);
    updateElement(`cpu-${server}`, data.cpu_percent);
    updateElement(`ram-${server}`, data.memory_percent);
    updateElement(`disk-${server}`, data.disk_percent);

}