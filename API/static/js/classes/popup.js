import { createElement } from '../functions/createElement.js';

export class DashboardPopUp {
    constructor(parent) {
        this.menu = createElement({ type: 'div', class: 'PopUp', parent });
        [
            { type: 'button', id: 'add-widget-btn', parent: this.menu, content: 'Add Widget'}
        ].forEach(item => this.addMenuItem(item));
    }

    addMenuItem(item) {
        createElement(item);
    }
}