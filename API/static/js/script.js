// --- Imports ---
import { refreshAllServerMetrics } from './functions/refreshAllServerMetrics.js';
import { initialize } from './functions/initialize.js';
import { removeWidget } from './functions/removeWidget.js';
import { addWidget } from './functions/addWidget.js';
import { renderBoard } from './functions/renderBoard.js';

// --- Initialization ---
try { 
    initialize();
} catch (err) {
    console.error('Initialization failed:', err);
}

// Expose only necessary functions globally
window.removeWidget = removeWidget;

// --- State ---
let lastWidth = window.innerWidth;
let lastHeight = window.innerHeight;
let resizeTimeout;

// --- Initial Render ---
try {
    renderBoard();
} catch (err) {
    console.error('Initial render failed:', err);
}

// --- Periodic Refresh ---
setInterval(() => {
    try {
        refreshAllServerMetrics();
    } catch (err) {
        console.error('Metrics refresh failed:', err);
    }
}, 5000);

// --- Events ---
document.getElementById('add-widget-btn').onclick = () => {
    try {
        addWidget();
    } catch (err) {
        console.error('Add widget failed:', err);
    }
};

window.addEventListener('resize', function () {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(function () {
        const widthChanged = window.innerWidth !== lastWidth;
        const heightChanged = Math.abs(window.innerHeight - lastHeight) > 50;
        if (widthChanged || heightChanged) {
            lastWidth = window.innerWidth;
            lastHeight = window.innerHeight;
            try {
                renderBoard();
            } catch (err) {
                console.error('Render on resize failed:', err);
            }
        }
    }, 150);
});