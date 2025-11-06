import { createElement } from '../functions/createElement.js';

export class DashboardPopUp {
    constructor(parent) {
        this.dispose();
        this.el = createElement({ type: 'div', className: 'PopUp', parent });
        const innerDiv = createElement({ type: 'div', parent: this.el });
        [  
            
            {
                type: 'button',
                className: "popup-close",
                title: "Close",
                onclick: () => this.dispose(),
                innerHTML: "&times;",
                parent: innerDiv
            }
        ].forEach(item => this.addMenuItem(item));
    }

    addMenuItem(item) {
        createElement(item);
    }

    dispose() {
        document.querySelectorAll('.PopUp').forEach(el => el.remove());
    }
}