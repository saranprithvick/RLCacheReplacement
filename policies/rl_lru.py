from policies.lru import LRUPolicy

class RLLRU(LRUPolicy):

    def __init__(self):
        super().__init__()