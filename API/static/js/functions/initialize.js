
import { refreshAllServerMetrics } from './refreshAllServerMetrics.js';
import { getServers } from './getServers.js';
import { renderBoard } from './renderBoard.js';
import { removeWidget } from './removeWidget.js';



export async function initialize() {
    window.servers = await getServers();
    setInterval(refreshAllServerMetrics, 5000);
    refreshAllServerMetrics();
    try {
        renderBoard();
    } catch (err) {
        console.error('Initial render failed:', err);
    }
    // Expose only necessary functions globally
    window.removeWidget = removeWidget;
}