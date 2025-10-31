import { getServers } from './getServers.js';
import { loadMetricsForServer } from './loadMetricsForServer.js';

export async function refreshAllServerMetrics() {
    let servers = await getServers(); // getServers returns a Promise
    servers.forEach(server => loadMetricsForServer(server));
}