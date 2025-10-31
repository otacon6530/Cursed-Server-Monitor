import { refreshAllServerMetrics } from '../functions/refreshAllServerMetrics.js';
import { initialize } from '../functions/initialize.js';
import { addWidget } from '../functions/addWidget.js';
import { renderBoard } from '../functions/renderBoard.js';
export class Dashboard {
    constructor() {
        this.lastWidth = window.innerWidth;
        this.lastHeight = window.innerHeight;
        this.resizeTimeout = null;
        this.initialize = initialize;

        this.initialize();
        this.setupEvents();
        this.startPeriodicRefresh();
    }

    startPeriodicRefresh() {
        setInterval(() => {
            try {
                refreshAllServerMetrics();
            } catch (err) {
                console.error('Metrics refresh failed:', err);
            }
        }, 5000);
    }

    setupEvents() {
        const addWidgetBtn = document.getElementById('add-widget-btn');
        if (addWidgetBtn) {
            addWidgetBtn.onclick = () => {
                try {
                    addWidget();
                } catch (err) {
                    console.error('Add widget failed:', err);
                }
            };
        }

        window.addEventListener('resize', () => {
            clearTimeout(this.resizeTimeout);
            this.resizeTimeout = setTimeout(() => {
                const widthChanged = window.innerWidth !== this.lastWidth;
                const heightChanged = Math.abs(window.innerHeight - this.lastHeight) > 50;
                if (widthChanged || heightChanged) {
                    this.lastWidth = window.innerWidth;
                    this.lastHeight = window.innerHeight;
                    try {
                        renderBoard();
                    } catch (err) {
                        console.error('Render on resize failed:', err);
                    }
                }
            }, 150);
        });
    }
}