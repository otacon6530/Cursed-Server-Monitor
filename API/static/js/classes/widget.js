import { Screen } from './screen.js';
import { createElement } from '../functions/createElement.js';
import { loadMetricsForServer } from '../functions/loadMetricsForServer.js';
import { removeWidget } from '../functions/removeWidget.js';
import { DashboardPopUp } from './popup.js';

export class Widget extends Screen {
    constructor(elements, config) {
        super({});
        this.removeWidget = removeWidget;
        this.el = createElement(elements);

        [
            { type: 'span', id: `status-${config.title}-parent` },
            { type: 'span', content: config.title },
            {
                type: 'button',
                className: "widget-remove",
                title: "Remove",
                onclick: () => this.removeWidget(config.idx),
                innerHTML: "&times;"
            },
            {
                type: 'button',
                className: "widget-edit",
                title: "Edit",
                onclick: () => this.editWidget(config.idx),
                innerHTML: "&#9998;"
            },
            {
                type: 'button',
                className: "widget-expand",
                title: "Expand",
                onclick: () => this.expandWidget(config.idx),
                innerHTML: "&#10530;"
            }
        ].forEach(e => createElement({ ...e, parent: this.el }));

        const container = createElement({ type: 'div', className: "childcontainer", parent: this.el });
        [
            ['Uptime', 'uptime'],
            ['CPU', 'cpu'],
            ['Memory', 'ram'],
            ['Disk', 'disk']
        ].forEach(([label, key]) =>
            createElement({
                type: 'metric',
                id: `${key}-${config.title}`,
                parent: createElement({
                    type: 'div',
                    className: "childbox",
                    id: `${key}-${config.title}-parent`,
                    content: `${label}:`,
                    parent: container
                })
            })
        );

        this.config = config;
        this.applyGridStyles();
        this.refresh();
    }

    refresh() {
        loadMetricsForServer(this.config.server);
    }
    editWidget() {

    }

    expandWidget() {
        new DashboardPopUp(document.body);
    }

    applyGridStyles() {
        const c = this.config, s = this.el.style, w = window.innerWidth;
        s.gridColumn = w > 600 ? `${c.gridColumnStart ?? 1} / span ${c.cols ?? 1}` : 'auto';
        s.gridRow    = w > 600 ? `${c.gridRowStart   ?? 1} / span ${c.rows ?? 1}` : 'auto';
    }
}