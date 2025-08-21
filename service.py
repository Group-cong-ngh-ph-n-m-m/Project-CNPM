class Service:
    def __init__(self, id: int = None, name: str = "", description: str = "", price: float = 0.0):
        self.id = id
        self.name = name
        self.description = description
        self.price = price

    def __repr__(self):
        return f"<Service id={self.id}, name={self.name}>"
