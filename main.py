from dataloader.ship_item_loader import ShipItemLoader
from dataloader.ship_loader import load_ship


def main():
    ship_item_loader = ShipItemLoader()
    ship = load_ship(ship_item_loader)


if __name__ == "__main__":
    main()

