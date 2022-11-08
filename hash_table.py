"""A (very minimalist) hash table implementation to store (key, value) pairs.

The hash table implements linear probing to handle collisions.

The code draws some inspiration from:
- https://en.wikipedia.org/wiki/Hash_table
- T. H. Cormen, et al., "Introduction to algorithms", MIT press, (2022)
- https://github.com/RunestoneInteractive/pythonds

If you would like a fully object-oriented Hash table implementation, I recommend:
- https://github.com/donsheehy/datastructures
"""


class HashTable:

    def __init__(self, init_size=5, resize_threshold=0.66666):
        """Initialize the hash table.

        Args:
            init_size: the initial size of the hash table.
            resize_threshold: the load factor at which the hash table should be resized.
        """
        self.slots = [None for _ in range(init_size)]
        self.values = [None for _ in range(init_size)]
        self.slots_filled = 0
        self.resize_threshold = resize_threshold

    def insert(self, key, value):
        """Insert a new (key, value) pair into the hash table.

        Args:
            key: the key to insert.
            value: the value to insert.

        """
        slot = self._hash(key)

        anticipated_load_factor = (self.slots_filled + 1) / len(self.slots)
        if anticipated_load_factor > self.resize_threshold:
            self._increase_size()

        while (self.slots[slot] != key) and (self.slots[slot] is not None):
            slot = (slot + 1) % len(self.slots)

        self.slots[slot] = key
        self.values[slot] = value
        self.slots_filled += 1

    def _increase_size(self):
        curr_size = len(self.slots)
        print(f"Resizing the table from {curr_size} to {curr_size * 2}")
        self.slots = self.slots + [None for _ in range(curr_size)]
        self.values = self.values + [None for _ in range(curr_size)]

    def _hash(self, key):
        """Hash the key to a slot in the hash table.

        Args:
            key: the key to hash.
        """
        return key % len(self.slots)

    def search(self, key):
        """Search for a value with a given key in the hash table.

        Args:
            key: the key to search for.
        """
        slot = self._probe(key)
        return self.values[slot]

    def delete(self, key):
        """Delete the (key, value) pair with the given key.

        Args:
            key: the key to delete.
        """
        slot = self._probe(key)
        self.slots[slot] = None
        self.values[slot] = None
        self.slots_filled -= 1

    def _probe(self, key):
        """Probe for a slot with the given key.

        Args:
            key: the key to probe for.
        """
        slot = self._hash(key)
        while self.slots[slot] != key:
            if self.slots[slot] is None:
                raise KeyError(f"Could not find {key} in hash table")
            slot = (slot + 1) % len(self.slots)
        return slot

    def __repr__(self):
        summary = (f"Hash table with {self.slots_filled} entries\n"
                   f" key: {self.slots},\n values: {self.values}")
        return summary


def num2letter(index):
    """Return the letter corresponding to the given index (with a at 0, b at 1
    etc.).

    Args:
        index: the index of the character.
    """
    return chr(index + ord("a"))


if __name__ == "__main__":

    hash_table = HashTable()

    for idx in range(12):
        sample_key, sample_value = idx, num2letter(idx)
        print(f"Inserting key: {sample_key}, val: {sample_value}")
        hash_table.insert(key=sample_key, value=sample_value)

    print("State of the hash table:")
    print(hash_table)

    hash_table.delete(3)
    hash_table.insert(key=3, value=num2letter(3))
    hash_table.delete(7)

    print("State of the hash table:")
    print(hash_table)

    search_keys = [0, 9, 11]
    for search_key in search_keys:
        print(f"Search for {search_key}: {hash_table.search(search_key)}")

    """
    Print out:

    """
