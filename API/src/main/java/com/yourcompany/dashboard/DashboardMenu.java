import java.util.ArrayList;
import java.util.List;

public class DashboardMenu {
    private List<String> menuItems;

    public DashboardMenu() {
        menuItems = new ArrayList<>();
    }

    public void addMenuItem(String item) {
        menuItems.add(item);
    }

    public void displayMenu() {
        System.out.println("Dashboard Menu:");
        for (int i = 0; i < menuItems.size(); i++) {
            System.out.println((i + 1) + ". " + menuItems.get(i));
        }
    }

    public List<String> getMenuItems() {
        return new ArrayList<>(menuItems);
    }
}