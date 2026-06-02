from policies.base_policy import BasePolicy

class LRUPolicy(BasePolicy):
    
    def __init__(self):
        self.order = []

    def access(self,block):
        "Move accessed block to MRU position"
        if block in self.order:
            self.order.remove(block)

        self.order.append(block)

    def victim(self):
        "Return LRU block"
        if not self.order:
            return None
        
        return self.order[0]
    
    def remove(self,block):
        if block in self.order:
            self.order.remove(block)

    def insert(self,block):
        if block in self.order:
            self.order.remove(block)

        self.order.append(block)

    def __str__(self):
        return f"LRU Order: {self.order}"