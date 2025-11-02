import { createElement } from '../functions/createElement.js';
import { loadMetricsForServer } from '../functions/loadMetricsForServer.js';
import { getWidgetTemplate } from '../functions/getWidgetTemplate.js';
import { Widget } from './widget.js';

export class Dashboard {
    constructor(parent) {
        this.div = createElement({ type: 'div', id: 'board', className: 'board-container', parent });

        this.getWidgetConfig().forEach((widget, idx) => {
            const widgetDiv = this.createWidgetDiv(widget, idx);
        });
    }

    createWidgetDiv(widget, idx) {
        const widgetObj = new Widget({
            type: 'div',
            className: 'widget',
            dataset: { idx },
            parent: this.div,
            innerHTML: getWidgetTemplate(widget.title, widget.content, idx),
            draggable: true
        }, widget);
        widgetObj.refresh();
        return widgetObj.el;
    }

    

    getWidgetConfig() {
        return JSON.parse(localStorage.getItem('widgetBoardConfig') || '[]');
    }

    saveWidgetConfig(config) {
        localStorage.setItem('widgetBoardConfig', JSON.stringify(config));
    }
}