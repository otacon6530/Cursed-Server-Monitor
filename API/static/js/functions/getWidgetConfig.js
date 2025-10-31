export function getWidgetConfig() {
    return JSON.parse(localStorage.getItem('widgetBoardConfig') || '[]');
}