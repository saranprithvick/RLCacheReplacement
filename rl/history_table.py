from collections import OrderedDict


class HistoryTable:
    """Bounded FIFO eviction history (Ghost Cache).

    Tracks the last `capacity` evicted blocks along with
    the RL decision metadata (state, action) that led to
    their eviction.

    - When a new block is added and the table is full,
      the oldest entry is expired and returned so the
      caller can issue a positive reward.
    - When a block is looked up (was_evicted / remove),
      its stored metadata is returned so the caller can
      issue a negative reward for a near-miss.
    """

    def __init__(self, capacity=8):

        self.capacity = capacity
        self.evicted = OrderedDict()

    def add(self, block, state=None, action=None):
        """Record an evicted block with its decision metadata.

        Returns (expired_block, (state, action)) if an old
        entry was pushed out, or None if no expiration occurred.
        """

        # If block is already tracked, remove the old entry
        # so we can re-insert at the end (most recent).
        if block in self.evicted:
            del self.evicted[block]

        expired = None

        if len(self.evicted) >= self.capacity:
            # Pop the oldest entry (FIFO order)
            expired_block, expired_meta = (
                self.evicted.popitem(last=False)
            )
            expired = (expired_block, expired_meta)

        self.evicted[block] = (state, action)

        return expired

    def remove(self, block):
        """Remove a block from the history table.

        Returns the stored (state, action) metadata if
        the block was present, or None otherwise.
        """

        if block in self.evicted:
            meta = self.evicted.pop(block)
            return meta

        return None

    def was_evicted(self, block):

        return block in self.evicted