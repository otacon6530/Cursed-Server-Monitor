import { Menu } from './menu.js';
import { Dashboard } from './dashboard.js';
import { createElement } from '../functions/createElement.js';
export class App {
    constructor() {
        this.div = createElement({ type: 'div', id: 'container', parent: document.body });
        this.menu = new Menu(this.div);
        this.dashboard = new Dashboard(this.div);
    }
}