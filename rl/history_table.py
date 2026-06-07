class HistoryTable:

    def __init__(self):

        self.evicted = set()

    def add(self, block):

        self.evicted.add(block)

    def was_evicted(
        self,
        block
    ):

        return (
            block
            in self.evicted
        )