
export function updateElement(id, newValue, nullValue) {
    try {
        document.getElementById(id).textContent = newValue;
    } catch (err) {
        // Handle error if needed
    }
}