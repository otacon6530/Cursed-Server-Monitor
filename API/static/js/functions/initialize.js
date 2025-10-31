
import { refreshAllServerMetrics } from './refreshAllServerMetrics.js';
import { getServers } from './getServers.js';

export async function initialize() {
    let servers = await getServers();
    setInterval(refreshAllServerMetrics, 5000);
    refreshAllServerMetrics();
}