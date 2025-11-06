import { getWidgetConfig } from './getWidgetConfig.js';
import { loadMetricsForServer } from './loadMetricsForServer.js';
import { saveWidgetConfig } from './saveWidgetConfig.js';
//import { getWidgetTemplate } from './getWidgetTemplate.js';

export function renderBoard() {
    const board = document.getElementById('board');
    board.innerHTML = ''; // Clear existing widgets
    const config = getWidgetConfig();
    config.forEach((widget, idx) => {
        const widgetDiv = document.createElement('div');
        widgetDiv.className = 'widget';
        widgetDiv.setAttribute('draggable', 'true');
        widgetDiv.dataset.idx = idx;
        const colSpan = widget.cols || 1;
        const rowSpan = widget.rows || 1;
        const colStart = widget.gridColumnStart || 1;
        const rowStart = widget.gridRowStart || 1;

        // Only apply grid styles if not on small screen
        if (window.innerWidth > 600) {
            widgetDiv.style.gridColumn = `${colStart} / span ${colSpan}`;
            widgetDiv.style.gridRow = `${rowStart} / span ${rowSpan}`;
        } else {
            widgetDiv.style.gridColumn = 'auto';
            widgetDiv.style.gridRow = 'auto';
        }

        //widgetDiv.innerHTML = getWidgetTemplate(widget.title, widget.content, idx);
        board.appendChild(widgetDiv);
        if (widget.server) {
            loadMetricsForServer(widget.server);
        }
    });

    // Drag and drop logic
    let dragIdx = null;
    let dragElem = null;

    board.querySelectorAll('.widget').forEach(widgetDiv => {
        widgetDiv.addEventListener('dragstart', function (e) {
            dragIdx = parseInt(widgetDiv.dataset.idx, 10);
            dragElem = widgetDiv;
            widgetDiv.classList.add('dragging');
            e.dataTransfer.effectAllowed = 'move';
            e.dataTransfer.setData('text/plain', '');
        });
        widgetDiv.addEventListener('dragend', function (e) {
            widgetDiv.classList.remove('dragging');
            dragIdx = null;
            dragElem = null;
        });
    });

    board.addEventListener('dragover', function (e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
    });

    board.addEventListener('drop', function (e) {
        e.preventDefault();
        if (dragIdx === null) return;

        // On small screens, don't reposition widgets
        if (window.innerWidth <= 600) {
            dragIdx = null;
            dragElem = null;
            return;
        }

        // Calculate grid position
        const boardRect = board.getBoundingClientRect();
        const style = window.getComputedStyle(board);
        const paddingLeft = parseInt(style.paddingLeft, 10);
        const paddingTop = parseInt(style.paddingTop, 10);

        const x = e.clientX - boardRect.left - paddingLeft;
        const y = e.clientY - boardRect.top - paddingTop;

        // Calculate column and row based on mouse position
        const col = Math.floor(x / (140 + 16));
        const row = Math.floor(y / (140 + 16)) + 1;

        // Prepare new widget config
        const config = getWidgetConfig();
        const movingWidget = { ...config[dragIdx], gridColumnStart: col, gridRowStart: row };

        // Check for intersection with other widgets
        let intersects = false;
        for (let i = 0; i < config.length; i++) {
            if (i === dragIdx) continue;
            if (widgetsIntersect(movingWidget, config[i])) {
                intersects = true;
                break;
            }
        }

        if (intersects) {
            dragElem.classList.add('intersecting');
            setTimeout(() => dragElem.classList.remove('intersecting'), 600);
            return; // Cancel move
        }

        // Update widget position
        config[dragIdx].gridColumnStart = col;
        config[dragIdx].gridRowStart = row;
        saveWidgetConfig(config);
        renderBoard();
    });
}