class DashboardMenu {
    constructor() {
        this.menuItems = [];
    }

    addMenuItem(item) {
        this.menuItems.push(item);
    }

    displayMenu() {
        console.log("Dashboard Menu:");
        this.menuItems.forEach((item, index) => {
            console.log(`${index + 1}. ${item}`);
        });
    }

    getMenuItems() {
        return [...this.menuItems];
    }
}