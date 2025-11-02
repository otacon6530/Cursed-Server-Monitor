import { createElement } from '../functions/createElement.js';

export class Screen {
    constructor(Elements) {
        this.createElement = createElement;
        this.addElement(Elements);
    }
    addElement(Elements) {
        [...(Array.isArray(Elements) ? Elements : [Elements])].forEach(item => this.createElement(item));
    }
}