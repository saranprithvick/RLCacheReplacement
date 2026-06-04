from simulator.cache_line import CacheLine


class Cache:
    def __init__(self,size,policy):
        self.size = size
        self.policy = policy
        self.lines = {}
        self.access_frequency = {}

        self.hits = 0
        self.misses = 0
        self.evictions = 0

    def build_state(self, victim):

        freq = self.access_frequency.get(victim, 0)

        # victim() always returns LRU
        recency_bucket = 0

        if freq <= 1:
            frequency_bucket = 0

        elif freq <= 3:
            frequency_bucket = 1

        else:
            frequency_bucket = 2

        return {
            "recency_bucket": recency_bucket,
            "frequency_bucket": frequency_bucket
        }
    
    def rl_decision(self,state):
        
        if state["frequency_bucket"] == 2:
            return "KEEP"
        
        return "EVICT"

    def access(self,block):
        
        self.access_frequency[block] = (
            self.access_frequency.get(block,0) + 1
        )

        #HIT
        if block in self.lines:
            self.hits += 1
            self.policy.access(block)

            print(f"{block:>2} -> HIT   "
                  f"Cache={list(self.lines.keys())}"
                  )
            
            return
        
        #MISS
        self.misses += 1

        #Cache Full
        if len(self.lines) >= self.size:

            victim = self.policy.victim()
            
            state = self.build_state(victim)

            decision = self.rl_decision(state)

            print(
                f"Victim={victim}",
                f"State={state}",
                f"Action={decision}",
            )

            if decision == "EVICT":

                del self.lines[victim]

                self.policy.remove(victim)

                self.evictions += 1

                print(
                    f"{block:>2} -> MISS    "
                    f"Evict={victim}"
                )

            else:

                # Give victim second chance

                self.policy.remove(victim)

                self.policy.insert(victim)

                victim = self.policy.victim()

                del self.lines[victim]

                self.policy.remove(victim)

                self.evictions += 1

                print(
                    f"{block:>2} -> MISS    "
                    f"SecondChance "
                    f"Evict={victim}"
                )

        else:
            print(
                f"{block:>2} -> MISS"
            )

        self.lines[block] = CacheLine(block)

        self.policy.insert(block)
    
    def get_stats(self):

        total = self.hits + self.misses
        
        return {
            "hits" : self.hits,
            "misses" : self.misses,
            "evictions" : self.evictions,
            "hit_rate" : round(self.hits/total,4),
            "miss_rate" : round(self.misses/total,4)
        }
    
    def print_stats(self):

        stats = self.get_stats()

        print("\n ===== RESULTS =====")

        print(f"Hits      : {stats['hits']}")
        print(f"Misses    : {stats['misses']}")
        print(f"Evictions : {stats['evictions']}")
        print(f"Hit Rate  : {stats['hit_rate']:.2%}")
        print(f"Miss Rate : {stats['miss_rate']:.2%}")