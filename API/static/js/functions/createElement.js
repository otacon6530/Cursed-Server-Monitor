export function createElement({ type, parent, content, ...attrs }) {
    const el = document.createElement(type);
    Object.assign(el, attrs);
    if (content) el.textContent = content;
    parent?.appendChild(el);
    return el;
}