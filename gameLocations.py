class Item:
    def __init__(self, name):
        self.name=name
        self.itemDescription=0 
    
    def __init__(self, name, itemDescription):
        self.name = name
        self.itemDescription = itemDescription

class Character:
    def __init__(self, name):
        self.name=name
        self.characterDescription=0 

    def __init__(self, name, characterDescription):
        self.name = name
        self.characterDescription = characterDescription

class gameLocations:
    def __init__(self):

        mushroom = Item("mushroom", "A small, edible mushroom.")

        stick = Item("stick", "A long, thin stick.")

        torch = Item("torch", "A burning torch.")

        rope = Item("rope", "A long, sturdy rope.")

        shell = Item("shell", "A pretty seashell.")
        
        seaweed = Item("seaweed", "A slimy, green plant.")

        bobokin = Character("bobokin", "A small, goblin-like creature.")

        bokoblin = Character("bokoblin", "A small, zelda creature with horn.")

        self.locations = {
            "forest": {
                "description": "You are in a dense forest. The trees are tall and the air is damp.",
                "items": [mushroom, stick],
                "characters": [],
                "connections": {
                    "north": "cave",
                    "south": "beach"
                }
            },
            "cave": {
                "description": "You are in a dark cave. The walls are rough and you can hear water dripping somewhere.",
                "items": [torch, rope],
                "characters": [bobokin,bokoblin],
                "connections": {
                    "south": "forest"
                }
            },
            "beach": {
                "description": "You are on a sandy beach. The waves are crashing against the shore and seagulls are crying overhead.",
                "items": [shell, seaweed],
                "characters": [],
                "connections": {
                    "north": "forest"
                }
            }
        }

    def add_location(self, name="", description="", items=[], characters=[], connections={}):
        if name == "" or description == "":
            print("Error: Must provide name and description.")
            return

        if name in self.locations:
            print(
                f"Errot: Location {name} already exists. Updating location...")
            return

        self.locations[name] = {"description": description, "items": items,
                                "characters": characters, "connections": connections}

        print(f"Location {name} added successfully.")

    def add_location(self, name, description, items=[], connections={}):
        self.locations[name] = {"description": description,
                                "items": items, "connections": connections}

    def add_location(self, name, description, connections={}):
        self.locations[name] = {
            "description": description, "connections": connections}

    def add_location(self, name, description, characters=[]):
        self.locations[name] = {
            "description": description, "characters": characters}

    def add_location(self, name, description, items=[], characters=[], connections={}):
        self.locations[name] = {"description": description, "items": items,
                                "characters": characters, "connections": connections}

    def add_item_to_location(self, name, item):
        if name not in self.locations:
            print(f"Error: location '{name}' not found.")
        else:
            self.locations[name]["items"].append(item)

    def add_description_to_location(self, name, description):
        if name not in self.locations:
            print(f"Error: location '{name}' not found.")

        else:
            self.locations[name]["description"] = description

    def add_connection_to_location(self, name, direction, destination):

        if name not in self.locations:
            print(f"Error: location '{name}' not found.")

            return

        if direction in self.locations[name]["connections"]:
            print(
                f"Error: location '{direction}' already exists in location '{name}'.")

            return

        if destination not in self.locations:
            print(f"Error: destination '{destination}' not in locations.")

            return

        if direction not in ['north', 'south', 'east', 'west']:
            print(f"Error: Invalid direction '{direction}'.")

            return

        opposite_direction = {
            'north': 'south',
            'south': 'north',
            'east': 'west',
            'west': 'east'
        }

        if opposite_direction[direction] in self.locations[destination]["connections"]:
            print(
                f"Error: destination '{destination}' already has opposite direction connection.")
            return

        self.locations[name]["connections"][direction] = destination

        self.locations[destination]["connections"][opposite_direction[direction]] = name

        return

    def get_location(self, name):
        if name not in self.locations:
            print(f"Error: location '{name}' not found.")

        return self.locations.get(name, None)

    def get_description(self, name):
        if name not in self.locations:
            print(f"Error: location '{name}' not found.")

        return self.get_location(name)["description"]

    def get_items(self, name):
        if name not in self.locations:
            print(f"Error: location '{name}' not found.")
            return

        if "items" not in self.get_location(name):
            print(f"Error: '{name}' does not have items.")
            return
        
        stringArray=[]

        for item in self.get_location(name)["items"]:
            stringX=""+item.name
            stringArray.append(stringX)

        return stringArray

    def get_characters(self, name):
        if name not in self.locations:
            print(f"Error: location '{name}' not found.")
        
        if "characters" not in self.get_location(name):
            print(f"Error: '{name}' does not have characters.")
            return

        stringArray=[]

        for character in self.get_location(name)["characters"]:
            stringX=""+character.name
            stringArray.append(stringX)

        return stringArray

    def get_connections(self, name):
        if name not in self.locations:
            print(f"Error: location '{name}' not found.")

        if "connections" not in self.get_location(name) or not self.get_location(name):
            print(f"Error: '{name}' does not have connections.")
            return

        return self.get_location(name)["connections"]
