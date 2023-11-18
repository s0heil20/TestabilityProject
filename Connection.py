

class Connection:

    def __init__(self, id, type="NET") -> None:
        self.value = 'U'   # default value for a given connection
        self.level = 0     # default level for a given connection
        self.type = type   # default type for a connection is NET but IN and OUT can be given to the constructor
        self.fanouts = []  # FANOUT array that includes fanout nets of this connection
        self.fault_set = set()  # Fault set of this connection that is needed for the deductive algorithm calculations
        self.id = id 

    def get_new_fan_out_net_name(self):
        return str(len(self.fanouts) + 1)

    def apply_value_to_fanouts(self):
        for fanout in self.fanouts:
            fanout.value = self.value

    def apply_fault_to_fanouts(self):
        for fanout in self.fanouts:
            fanout.fault_set = self.fault_set | {fanout.id + "-sa" + str(1-fanout.value)}

    def __eq__(self, other) -> bool:
        if type(self) != type(other):
            return False
        return self.id == other.id
    