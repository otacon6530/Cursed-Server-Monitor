
        const APIServer = "http://localhost:5000";


        import { getServers } from './functions/getServers.js';
        let servers = [];

        async function refreshAllServerMetrics() {
            servers = await getServers(); // getServers returns a Promise
            servers.forEach(server => loadMetricsForServer(server));
        }

        async function initialize() {
            servers = await getServers();
            setInterval(refreshAllServerMetrics, 5000);
            refreshAllServerMetrics();
        }

        initialize();

        async function renderServerBoxes() {
            const response = await fetch(APIServer +"/api/get-servers");
            servers = await response.json();
            const container = document.querySelector(".board-container");
            container.innerHTML = ""; // Clear existing boxes

            servers.forEach(server => {

                loadMetricsForServer(server);
            });
        }
        function updateElement(id, newValue, nullValue) {
            try {
                document.getElementById(id).textContent = newValue;
            } catch (err) {
                // Handle error if needed
            }
        }
        async function loadMetricsForServer(server) {
            let response;
            let data;
            try {
                response = await fetch(APIServer +`/api/metrics?server=${encodeURIComponent(server)}`);
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

            servers = getServers();
            setInterval(refreshAllServerMetrics, 5000); // Refresh every 5 seconds
        // Widget configuration stored in localStorage
        function getWidgetConfig() {
            return JSON.parse(localStorage.getItem('widgetBoardConfig') || '[]');
        }
        function saveWidgetConfig(config) {
            localStorage.setItem('widgetBoardConfig', JSON.stringify(config));
        }

        // Helper: check if two widgets overlap in grid
        function widgetsIntersect(a, b) {
            const aColStart = a.gridColumnStart || 1;
            const aColEnd = aColStart + (a.cols || 1) - 1;
            const aRowStart = a.gridRowStart || 1;
            const aRowEnd = aRowStart + (a.rows || 1) - 1;

            const bColStart = b.gridColumnStart || 1;
            const bColEnd = bColStart + (b.cols || 1) - 1;
            const bRowStart = b.gridRowStart || 1;
            const bRowEnd = bRowStart + (b.rows || 1) - 1;

            // Check for overlap
            return !(aColEnd < bColStart || aColStart > bColEnd ||
                aRowEnd < bRowStart || aRowStart > bRowEnd);
        }
        function getWidgetTemplate(title, content, idx) {
            let temp = `
                        <strong><span id = "status-${title}-parent"></span><span>${title}</span><button class="widget-remove" title="Remove" onclick="removeWidget(${idx})">&times;</button></strong> <br />
                        <div class="childcontainer">
                            <div class="childbox" id="uptime-${title}-parent" >Uptime:<br /> <metric id="uptime-${title}"></metric></div>
                            <div class="childbox" id="cpu-${title}-parent">CPU:<br /> <span><metric id="cpu-${title}"></metric>%</span></div>
                            <div class="childbox" id="ram-${title}-parent">Memory:<br /> <span><metric id="ram-${title}"></metric>%</span></div>
                            <div class="childbox" id="disk-${title}-parent">Disk:<br /> <span><metric id="disk-${title}"></metric>%</span></div>
                        </div>
                        `;
            if (title == 'share.stephensdev.com' || title == 'print.stephensdev.com') {
                temp = `
                        <strong><span id = "status-${title}-parent"></span><span class="widget-header">${title}</span><button class="widget-remove" title="Remove" onclick="removeWidget(${idx})">&times;</button></strong>
                        `;
            } 
            return temp;
        }
        function renderBoard() {
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

                widgetDiv.innerHTML = getWidgetTemplate(widget.title, widget.content, idx);
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

        async function addWidget() {
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

        function removeWidget(idx) {
            const config = getWidgetConfig();
            config.splice(idx, 1);
            saveWidgetConfig(config);
            renderBoard();
        }

        document.getElementById('add-widget-btn').onclick = addWidget;
        window.removeWidget = removeWidget;

        // Initial render
        renderBoard();

        let lastWidth = window.innerWidth;
        let lastHeight = window.innerHeight;
        let resizeTimeout;

        window.addEventListener('resize', function () {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(function () {
                const widthChanged = window.innerWidth !== lastWidth;
                const heightChanged = Math.abs(window.innerHeight - lastHeight) > 50; // Only rerender if height changes by >50px
                if (widthChanged || heightChanged) {
                    lastWidth = window.innerWidth;
                    lastHeight = window.innerHeight;
                    renderBoard();
                }
            }, 150);
        });