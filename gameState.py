class gameState:
    def __init__(self, playerName, playerLocation, inventory):
        self.playerName = playerName
        self.playerLocation = playerLocation
        self.inventory = inventory

    def __str__(self):
        inv_str = "\n".join([f"\t{k}: {v}" for k, v in self.inventory.items()])
        return f"Player Name: {self.playerName}\nPlayer Location: {self.playerLocation}\nInventory:\n{inv_str}"
    
