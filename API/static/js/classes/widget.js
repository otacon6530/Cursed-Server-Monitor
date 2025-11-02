import { Screen } from './screen.js';
import { createElement } from '../functions/createElement.js';
import { loadMetricsForServer } from '../functions/loadMetricsForServer.js';

export class Widget extends Screen {
    constructor(elements,config) {
        super({});
        this.el = createElement(elements);
        this.config = config;
        this.applyGridStyles();
        if (config.server) this.refresh();
    }

    refresh() {
        loadMetricsForServer(this.config.server);
    }

    applyGridStyles() {
        const c = this.config,
            s = this.el.style,
            w = window.innerWidth;
        s.gridColumn = w > 600 ? `${c.gridColumnStart ?? 1} / span ${c.cols ?? 1}` : 'auto';
        s.gridRow    = w > 600 ? `${c.gridRowStart   ?? 1} / span ${c.rows ?? 1}` : 'auto';
    }

}