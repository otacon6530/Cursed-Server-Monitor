export function widgetsIntersect(a, b) {
    const aColStart = a.gridColumnStart || 1;
    const aColEnd = aColStart + (a.cols || 1) - 1;
    const aRowStart = a.gridRowStart || 1;
    const aRowEnd = aRowStart + (a.rows || 1) - 1;

    const bColStart = b.gridColumnStart || 1;
    const bColEnd = bColStart + (b.cols || 1) - 1;
    const bRowStart = b.gridRowStart || 1;
    const bRowEnd = bRowStart + (b.rows || 1) - 1;

    // Check for overlap
    return !(aColEnd < bColStart || aColStart > bColEnd ||
        aRowEnd < bRowStart || aRowStart > bRowEnd);
}