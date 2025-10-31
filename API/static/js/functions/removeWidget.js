import { saveWidgetConfig } from './saveWidgetConfig.js';
import { renderBoard } from './renderBoard.js';
import { getWidgetConfig } from './getWidgetConfig.js';

export function removeWidget(idx) {
    const config = getWidgetConfig();
    config.splice(idx, 1);
    saveWidgetConfig(config);
    renderBoard();
}