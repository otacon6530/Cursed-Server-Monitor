export function saveWidgetConfig(config) {
    localStorage.setItem('widgetBoardConfig', JSON.stringify(config));
}