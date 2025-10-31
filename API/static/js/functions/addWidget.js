import { saveWidgetConfig } from './saveWidgetConfig.js';
import { renderBoard } from './renderBoard.js';

export async function addWidget() {
    // Fetch servers if not already loaded
    let servers = window.servers;
    if (!servers || !Array.isArray(servers) || servers.length === 0) {
        try {
            const response = await fetch(APIServer + "/api/get-servers");
            servers = await response.json();
            window.servers = servers;
        } catch (err) {
            alert("Failed to load server list.");
            return;
        }
    }

    // Build server selection prompt
    let serverList = servers.map((s, i) => `${i + 1}: ${s}`).join('\n');
    let serverIdx = parseInt(prompt(`Select a server for this widget:\n${serverList}`, "1"), 10) - 1;
    if (isNaN(serverIdx) || serverIdx < 0 || serverIdx >= servers.length) {
        alert("Invalid server selection.");
        return;
    }
    const server = servers[serverIdx];

    // Widget content can be server name or metrics placeholder
    const content = `Metrics for server: <strong>${server}</strong>`;

    let cols = parseInt(prompt('How many columns should this widget span?', '1'), 10);
    let rows = parseInt(prompt('How many rows should this widget span?', '1'), 10);
    let gridColumnStart = 1;
    let gridRowStart = 1;
    if (isNaN(cols) || cols < 1) cols = 1;
    if (isNaN(rows) || rows < 1) rows = 1;

    const config = getWidgetConfig();
    config.push({
        title: server, // Use server name as widget title
        content,
        server,        // Store server for future use
        cols,
        rows,
        gridColumnStart,
        gridRowStart
    });
    saveWidgetConfig(config);
    renderBoard();
}