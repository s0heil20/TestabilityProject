

class Connection:

    def __init__(self, id, type="NET") -> None:
        self.value = 'X'   # default value for a given connection
        self.level = 0     # default level for a given connection
        self.type = type   # default type for a connection is NET but IN and OUT can be given to the constructor
        self.id = id       

    def __eq__(self, other) -> bool:
        if type(self) != type(other):
            return False
        return self.id == other.id
    