import { saveWidgetConfig } from './saveWidgetConfig.js';
import { renderBoard } from './renderBoard.js';
import { getWidgetConfig } from './getWidgetConfig.js';

export function removeWidget(idx) {
    saveWidgetConfig(getWidgetConfig().filter((_, i) => i !== idx));
    renderBoard();
}