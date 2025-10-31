export function getWidgetTemplate(title, content, idx) {
    let temp = `
                        <strong><span id = "status-${title}-parent"></span><span>${title}</span><button class="widget-remove" title="Remove" onclick="removeWidget(${idx})">&times;</button></strong> <br />
                        <div class="childcontainer">
                            <div class="childbox" id="uptime-${title}-parent" >Uptime:<br /> <metric id="uptime-${title}"></metric></div>
                            <div class="childbox" id="cpu-${title}-parent">CPU:<br /> <span><metric id="cpu-${title}"></metric>%</span></div>
                            <div class="childbox" id="ram-${title}-parent">Memory:<br /> <span><metric id="ram-${title}"></metric>%</span></div>
                            <div class="childbox" id="disk-${title}-parent">Disk:<br /> <span><metric id="disk-${title}"></metric>%</span></div>
                        </div>
                        `;
    if (title == 'share.stephensdev.com' || title == 'print.stephensdev.com') {
        temp = `
                        <strong><span id = "status-${title}-parent"></span><span class="widget-header">${title}</span><button class="widget-remove" title="Remove" onclick="removeWidget(${idx})">&times;</button></strong>
                        `;
    }
    return temp;
}