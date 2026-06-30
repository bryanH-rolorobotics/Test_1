#!/usr/bin/env python3
"""A small text-based adventure game. No external dependencies required."""


class Room:
    def __init__(self, name, description, exits, items=None,
                 dark=False, has_monster=False, locked=False):
        self.name = name
        self.description = description
        self.exits = exits          # dict: direction -> room_id
        self.items = items if items is not None else []
        self.dark = dark
        self.has_monster = has_monster
        self.monster_defeated = False
        self.locked = locked        # locked: cannot enter until unlocked with key
        self.lit = not dark         # dark rooms start unlit


class Player:
    def __init__(self, starting_room):
        self.current_room = starting_room
        self.inventory = []
        self.game_over = False
        self.won = False


def build_world():
    return {
        'entrance': Room(
            name="Entrance Hall",
            description=(
                "You stand in a grand entrance hall with cracked stone floors. "
                "Faded tapestries hang from the walls. A dark corridor leads north "
                "into an old library. A heavy iron door stands to the east, "
                "leading deeper into the dungeon."
            ),
            exits={'north': 'library', 'east': 'dungeon'},
            items=['torch', 'sword'],
        ),
        'library': Room(
            name="Ancient Library",
            description=(
                "Towering bookshelves stretch into shadow, crammed with crumbling tomes. "
                "The air smells of old parchment and dust. A faint shimmer to the east "
                "suggests a hidden vault behind a locked iron door. "
                "The entrance hall lies to the south."
            ),
            exits={'south': 'entrance', 'east': 'vault'},
            items=['key'],
            dark=True,
        ),
        'dungeon': Room(
            name="Dungeon",
            description=(
                "A dank dungeon reeking of rot and decay. Chains hang from the walls "
                "and bones litter the floor. The entrance hall is back to the west."
            ),
            exits={'west': 'entrance'},
            items=[],
            has_monster=True,
        ),
        'vault': Room(
            name="Treasure Vault",
            description=(
                "A magnificent vault gleaming with gold coins and sparkling jewels. "
                "In the center of the room sits an ornate treasure chest, bound in brass. "
                "The library lies to the west."
            ),
            exits={'west': 'library'},
            items=['treasure chest'],
            locked=True,
        ),
    }


def print_room(room, player):
    print(f"\n=== {room.name} ===")
    if room.dark and not room.lit:
        print("It is pitch black. You can barely see your hand in front of your face.")
        print("You need a light source to see anything here.")
    else:
        print(room.description)
        if room.items:
            items_str = ', '.join(f'a {item}' for item in room.items)
            print(f"You see here: {items_str}.")
        if room.has_monster and not room.monster_defeated:
            print("A fearsome monster lurks in the shadows!")
        if room.locked and player.current_room in ('library',):
            print("A locked iron door blocks the way east.")
    exits_str = ', '.join(room.exits.keys())
    print(f"Exits: {exits_str}")


def handle_go(direction, player, rooms):
    room = rooms[player.current_room]
    if direction not in room.exits:
        print(f"You can't go {direction} from here.")
        return

    target_id = room.exits[direction]
    target = rooms[target_id]

    # Check locked vault door (locked from the library side only)
    if target.locked and player.current_room == 'library':
        print("The iron door to the east is locked. You need a key to open it.")
        return

    # Move player
    player.current_room = target_id

    # Handle dark room on entry
    if target.dark and not target.lit:
        if 'torch' in player.inventory:
            target.lit = True
            print("Your torch blazes to life, chasing the shadows from the room!")
        else:
            print(f"\n=== {target.name} ===")
            print(
                "You step into impenetrable darkness. Without any light, "
                "you stumble blindly and plunge into a hidden pit!"
            )
            print("\nYou died.  -- GAME OVER --")
            player.game_over = True
            return

    # Handle monster encounter on entry
    if target.has_monster and not target.monster_defeated:
        if 'sword' in player.inventory:
            target.monster_defeated = True
            print("\nA hideous monster lunges from the shadows!")
            print("You draw your sword just in time and cut it down with a mighty blow!")
        else:
            print(f"\n=== {target.name} ===")
            print(
                "A hideous monster erupts from the darkness and tears you apart "
                "before you can defend yourself!"
            )
            print("\nYou died.  -- GAME OVER --")
            player.game_over = True
            return

    print_room(target, player)

    # Check win condition: back in entrance holding the treasure
    if player.current_room == 'entrance' and 'treasure chest' in player.inventory:
        print("\nYou burst out of the dungeon into the sunlight, treasure chest in hand!")
        print("The villagers cheer as you return with the legendary treasure!")
        print("\n*** CONGRATULATIONS — YOU WIN! ***")
        player.won = True
        player.game_over = True


def handle_look(player, rooms):
    print_room(rooms[player.current_room], player)


def handle_take(item_name, player, rooms):
    room = rooms[player.current_room]

    if room.dark and not room.lit:
        print("It's too dark to find anything here.")
        return

    found = next(
        (item for item in room.items if item_name.lower() in item.lower()),
        None,
    )
    if found is None:
        print(f"There is no '{item_name}' here.")
        return

    room.items.remove(found)
    player.inventory.append(found)
    print(f"You picked up the {found}.")


def handle_use(item_name, player, rooms):
    found = next(
        (item for item in player.inventory if item_name.lower() in item.lower()),
        None,
    )
    if found is None:
        print(f"You don't have a '{item_name}'.")
        return

    room = rooms[player.current_room]

    if 'torch' in found.lower():
        if room.dark and not room.lit:
            room.lit = True
            print("You hold your torch aloft. The room is illuminated!")
            print_room(room, player)
        else:
            print("The torch is already providing light here.")

    elif 'key' in found.lower():
        if player.current_room == 'library':
            vault = rooms.get('vault')
            if vault and vault.locked:
                vault.locked = False
                print("You insert the key into the lock. With a heavy clunk, the iron door swings open!")
            else:
                print("The door is already unlocked.")
        else:
            print("There's nothing here to use the key on.")

    elif 'sword' in found.lower():
        if room.has_monster and not room.monster_defeated:
            room.monster_defeated = True
            print("You brandish your sword and slay the monster with a single stroke!")
        else:
            print("You swing your sword heroically, but there's nothing to fight here.")

    elif 'treasure' in found.lower():
        print("The treasure chest gleams with riches beyond imagining. Get back to the entrance to escape!")

    else:
        print(f"You're not sure how to use the {found} here.")


def handle_inventory(player):
    if not player.inventory:
        print("Your inventory is empty.")
    else:
        print("You are carrying:")
        for item in player.inventory:
            print(f"  - {item}")


DIRECTION_ALIASES = {'n': 'north', 's': 'south', 'e': 'east', 'w': 'west'}


def parse_command(raw, player, rooms):
    parts = raw.strip().lower().split(None, 1)
    if not parts:
        print("Please enter a command. Type 'help' for a list of commands.")
        return

    verb = parts[0]
    arg = parts[1].strip() if len(parts) > 1 else ''

    if verb in ('quit', 'q', 'exit'):
        print("Thanks for playing! Farewell, adventurer.")
        player.game_over = True

    elif verb in ('look', 'l'):
        handle_look(player, rooms)

    elif verb == 'go':
        if not arg:
            print("Go where? Try: go north, go south, go east, go west")
            return
        handle_go(DIRECTION_ALIASES.get(arg, arg), player, rooms)

    elif verb in DIRECTION_ALIASES:
        handle_go(DIRECTION_ALIASES[verb], player, rooms)

    elif verb in ('north', 'south', 'east', 'west'):
        handle_go(verb, player, rooms)

    elif verb in ('take', 'get', 'grab'):
        if not arg:
            print("Take what? (e.g. take torch)")
            return
        handle_take(arg, player, rooms)

    elif verb == 'pick':
        # support "pick up <item>"
        item = arg[3:].strip() if arg.startswith('up ') else arg
        if not item:
            print("Pick up what?")
            return
        handle_take(item, player, rooms)

    elif verb == 'use':
        if not arg:
            print("Use what? (e.g. use torch)")
            return
        handle_use(arg, player, rooms)

    elif verb in ('inventory', 'inv', 'i'):
        handle_inventory(player)

    elif verb in ('help', '?', 'h'):
        print_help()

    else:
        print(f"Unknown command: '{verb}'. Type 'help' for a list of commands.")


def print_help():
    print("""
Commands:
  go <direction>      Move (north, south, east, west)
  n / s / e / w       Shorthand for go north/south/east/west
  look  (l)           Describe the current room
  take <item>         Pick up an item from the room
  use <item>          Use an item from your inventory
  inventory (inv, i)  List what you're carrying
  quit                Quit the game
  help                Show this message
""")


def main():
    print("=" * 52)
    print("        DUNGEON OF THE LOST TREASURE")
    print("=" * 52)
    print(
        "\nYou are an adventurer seeking a legendary treasure"
        "\nhidden deep within an ancient dungeon complex."
        "\nFind the treasure chest and escape to win!"
        "\n\nType 'help' for a list of commands.\n"
    )

    rooms = build_world()
    player = Player('entrance')
    print_room(rooms[player.current_room], player)

    while not player.game_over:
        try:
            raw = input("\n> ")
        except (EOFError, KeyboardInterrupt):
            print("\nThanks for playing! Farewell, adventurer.")
            break
        if raw.strip():
            parse_command(raw, player, rooms)


if __name__ == '__main__':
    main()
