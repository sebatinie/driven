import pickle
import copy


class Player:
    def __init__(self, name, level, inventory, position):
        self.name = name
        self.level = level
        self.inventory = inventory
        self.position = position

    def serialize(self):
        return {
            'name': self.name,
            'level': self.level,
            'inventory': self.inventory,
            'position': self.position
        }


def save_players(filename, players):
    with open(filename, 'wb') as f:
        for player in players:
            pickle.dump(player.serialize(), f)


def load_players(filename):
    players = []

    with open(filename, 'rb') as f:
        while True:
            try:
                data = pickle.load(f)

                player = Player(
                    data['name'],
                    data['level'],
                    copy.deepcopy(data['inventory']),
                    copy.deepcopy(data['position'])
                )

                players.append(player)

            except EOFError:
                break

            except pickle.UnpicklingError:
                print("Error: Corrupted save file.")
                break

    return players


def update_player_stats(player, level_boost):
    player.level += level_boost
    return player


players = [
    Player(
        'Alice',
        5,
        ['sword', 'shield'],
        (10, 20)
    ),
    Player(
        'Bob',
        3,
        ['bow'],
        (15, 25)
    )
]


save_players('game_state.pkl', players)

loaded_players = load_players('game_state.pkl')

# Modify deserialized data
loaded_players[0].inventory.append('health_potion')
update_player_stats(loaded_players[0], 2)

for p in loaded_players:
    print(
        f"{p.name}: "
        f"Level {p.level}, "
        f"Position {p.position}, "
        f"Inventory {p.inventory}"
    )