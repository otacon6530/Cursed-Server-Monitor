export function createElement({ type, parent, parentId, content, ...attrs }) {
    const el = document.createElement(type);

    // Assign dataset properties if present
    if (attrs.dataset) {
        Object.entries(attrs.dataset).forEach(([key, value]) => {
            el.dataset[key] = value;
        });
        delete attrs.dataset; // Remove dataset from attrs to avoid Object.assign issues
    }

    Object.assign(el, attrs);

    if (content) el.textContent = content;
    if (parentId) parent = document.getElementById(parentId);
    parent?.appendChild(el);
    return el;
}