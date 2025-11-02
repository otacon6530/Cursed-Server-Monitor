import { createElement } from '../functions/createElement.js';
import { addWidget } from '../functions/addWidget.js';

export class Menu {
    constructor(parent) {
        this.ele = createElement({ type: 'div', id: 'DashBoardMenu', parent });
        [
            {
                type: 'button',
                id: 'add-widget-btn',
                parent: this.ele,
                content: 'Add Widget',
                onclick: () => addWidget()
            }, {
                type: 'button',
                id: 'add-widget-btn',
                parent: this.ele,
                content: 'Add Widget',
                onclick: () => addWidget()
            }, {
                type: 'button',
                id: 'add-widget-btn',
                parent: this.ele,
                content: 'Add Widget',
                onclick: () => addWidget()
            }, {
                type: 'button',
                id: 'add-widget-btn',
                parent: this.ele,
                content: 'Add Widget',
                onclick: () => addWidget()
            }, {
                type: 'button',
                id: 'add-widget-btn',
                parent: this.ele,
                content: 'Add Widget',
                onclick: () => addWidget()
            }
        ].forEach(item => this.addMenuItem(item));
    }

    addMenuItem(item) {
        createElement(item);
    }
}