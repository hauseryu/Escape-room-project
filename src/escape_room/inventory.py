
class Inventory():
    def __init__(self):
        self.canvas = None
        self.inventory = []
        pass

    def draw(self,canvas):
        self.canvas = canvas    
        canvas.create_rectangle(0, 0, 300, 200, fill="black")
        canvas.create_text(
            100, 10, text="Inventory", fill="white", font=("Arial", 12, "bold"))
        
    def addObject(self,object):
        self.inventory.append(object)

    def objectInInventory(self,object):
        return (object in self.inventory)
    

