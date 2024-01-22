from models.ship import Ship


def remove_duplicate_ship(ships: list[Ship]) -> list[Ship]:
    ship_dict = {}
    for ship in ships:
        if ship.name not in ship_dict:
            ship_dict[ship.name] = [ship]
        else:
            ship_dict[ship.name].append(ship)

    new_ships = []
    for ship_name in ship_dict:
        is_find = False
        for ship in ship_dict[ship_name]:
            if len(ship.shop_info) > 0:
                is_find = True
                new_ships.append(ship)
                break
        if not is_find:
            print(f'{ship_name} has no shop info')
            new_ships.append(ship_dict[ship_name][0])
    return new_ships
