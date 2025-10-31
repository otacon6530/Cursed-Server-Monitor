
import { loadMetricsForServer } from './loadMetricsForServer.js';

export async function renderServerBoxes() {
    const response = await fetch(APIServer + "/api/get-servers");
    servers = await response.json();
    const container = document.querySelector(".board-container");
    container.innerHTML = ""; // Clear existing boxes

    servers.forEach(server => {

        loadMetricsForServer(server);
    });
}