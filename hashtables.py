""" Hashtable Implementation using Separate Chaining
    Course: CPE202
    Quarter: Spring 2020
    Author: Chris Linthacum
"""

# from linked_list import LinkedList

class HashTableLinear:
    """ Implementation of hash table class using linear probing

    """

    def __init__(self, table_size=11):
        """ Takes no parameters. Initialize an empty hash table object
            Returns:
                HashTableSepchain: initialized hash table
        """

        self.table = [None] * table_size

        self.num_items = 0
        self.num_collisions = 0
        self.table_size = table_size

    def __eq__(self, other):
        """ Checks if two hash tables are equal"""

        return isinstance(other, HashTableLinear) and \
               self.table == other.table

    def __repr__(self):
        """ How the hash table repr itself"""
        out_str = ''
        for each in enumerate(self.table):
            line_out = 'Hash_val = {}: {}\n'.format(each[0], each[1])
            out_str += line_out

        return out_str

    def __getitem__(self, key):
        """ Gets a value with []"""
        return self.get(key)

    def __setitem__(self, key, data):
        """ Enables value assignment with []"""

        self.put(key, data)

    def __contains__(self, key):
        """ Enables in operator on Hash Table"""
        return self.contains(key)

    def put(self, key, val):
        """ Takes a key and item and inserts the pair into the hash table
            Args:
                key(str): the key of the pair
                val(any): the data being inserted
            Returns:

        """

        hash_val = hash_string(key, self.table_size)

        if self.contains(key):
            self.remove(key)

        if self.table[hash_val] is None:
            self.table[hash_val] = (key, val)
        else:
            self.num_collisions += 1
            searching = True
            while searching:
                if self.table[hash_val] is None:
                    self.table[hash_val] = (key, val)
                    searching = False
                else:
                    if hash_val == self.table_size - 1:
                        hash_val = 0
                    else:
                        hash_val += 1

        self.num_items += 1

        if self.load_factor() > .75:
            self.rehash((self.table_size * 2) + 1)

    def get(self, key):
        """ Takes a key and returns the value from the hash table"""
        if not self.contains(key):
            raise KeyError

        hash_val = hash_string(key, self.table_size)
        found = False
        while not found:
            if self.table[hash_val][0] == key:
                found = True
                return self.table[hash_val][1]
            if hash_val == self.table_size - 1:
                hash_val = 0
            else:
                hash_val += 1

    def contains(self, key):
        """ Checks if a key is in the hash table"""
        for each in self.table:
            if each is not None:
                if each[0] == key:
                    return True
        return False

    def remove(self, key):
        """ Removes a key-value pair from the table and returns the pair
        """
        hash_val = hash_string(key, self.table_size)
        if not self.contains(key):
            raise KeyError
        found = False
        while not found:
            if self.table[hash_val] is not None:
                if self.table[hash_val][0] == key:
                    temp = self.table[hash_val]
                    found = True
                    self.table[hash_val] = None
                    return temp
            if hash_val == self.table_size - 1:
                hash_val = 0
            else:
                hash_val += 1

    def size(self):
        """ Returns the number of pairs stored in the hash"""
        return self.num_items

    def load_factor(self):
        """ Returns the load factor of the hash table"""
        return self.num_items / self.table_size

    def collisions(self):
        """ Returns the number of collisions that occured while insert into
            hash table. A collision occurs when an item is inserted into the
            hash table at a location where one or more pairs has already been
            inserted. When a table is resized, do not increment the number
            of collisions unless a collision occurs when the new key-value pair
            is being inserted into the resized hash table.
        """

        return self.num_collisions

    def rehash(self, new_size):
        """ Rehash the table for a new size"""

        new_table = HashTableLinear(new_size)
        for each in self.table:
            if each is not None:
                new_table.put(each[0], each[1])
                self.remove(each[0])

        self.table = new_table.table
        self.num_items = new_table.num_items
        self.table_size = new_table.table_size
        self.num_collisions = new_table.num_collisions

# class HashTableSepchain:
#     """ Implementation of hash table class using separate chaining
#
#     """
#
#     def __init__(self, table_size=11):
#         """ Takes no parameters. Initialize an empty hash table object
#             Returns:
#                 HashTableSepchain: initialized hash table
#         """
#
#         self.table = [None] * table_size
#
#         self.num_items = 0
#         self.num_collisions = 0
#         self.table_size = table_size
#
#     def __eq__(self, other):
#         """ Checks if two hash tables are equal"""
#
#         return isinstance(other, HashTableSepchain) and \
#                self.table == other.table
#
#     def __repr__(self):
#         """ How the hash table repr itself"""
#         out_str = ''
#         for each in enumerate(self.table):
#             line_out = 'Hash_val = {}: {}\n'.format(each[0], each[1])
#             out_str += line_out
#
#         return out_str
#
#     def __getitem__(self, key):
#         """ Gets a value with []"""
#         return self.get(key)
#
#     def __setitem__(self, key, data):
#         """ Enables value assignment with []"""
#
#         self.put(key, data)
#
#     def __contains__(self, key):
#         """ Enables in operator on Hash Table"""
#         return self.contains(key)
#
#     def put(self, key, val):
#         """ Takes a key and item and inserts the pair into the hash table
#             Args:
#                 key(str): the key of the pair
#                 val(any): the data being inserted
#             Returns:
#
#         """
#         hash_val = hash_string(key, self.table_size)
#         if self.table[hash_val] is None:
#             self.table[hash_val] = LinkedList()
#         else:
#             self.num_collisions += 1
#
#         if self.contains(key):
#             self.table[hash_val].remove(key)
#
#         self.table[hash_val].insert(key, val)
#
#         self.num_items += 1
#
#         if self.load_factor() > 1.5:
#             self.rehash((self.table_size * 2) + 1)
#
#     def get(self, key):
#         """ Takes a key and returns the value from the hash table"""
#         if not self.contains(key):
#             raise KeyError
#
#         hash_val = hash_string(key, self.table_size)
#
#         active_list = self.table[hash_val]
#         active_node = active_list.head
#         found = False
#         while not found:
#             if active_node.key == key:
#                 found = True
#                 return active_node.val
#             active_node = active_node.next
#
#     def contains(self, key):
#         """ Checks if a key is in the hash table"""
#         hash_val = hash_string(key, self.table_size)
#         if self.table[hash_val] is None:
#             return False
#         return self.table[hash_val].contains(key)
#
#     def remove(self, key):
#         """ Removes a key-value pair from the table and returns the pair
#         """
#         hash_val = hash_string(key, self.table_size)
#         if not self.contains(key):
#             raise KeyError
#
#         active_list = self.table[hash_val]
#         kv_pair = active_list.remove(key)
#         self.num_items -= 1
#         return kv_pair
#
#     def size(self):
#         """ Returns the number of pairs stored in the hash"""
#         return self.num_items
#
#     def load_factor(self):
#         """ Returns the load factor of the hash table"""
#         return self.num_items / self.table_size
#
#     def collisions(self):
#         """ Returns the number of collisions that occured while insert into
#             hash table. A collision occurs when an item is inserted into the
#             hash table at a location where one or more pairs has already been
#             inserted. When a table is resized, do not increment the number
#             of collisions unless a collision occurs when the new key-value pair
#             is being inserted into the resized hash table.
#         """
#
#         return self.num_collisions
#
#     def rehash(self, new_size):
#         """ Rehash the table for a new size"""
#         new_table = HashTableSepchain(new_size)
#         for each in self.table:
#             if each is not None:
#                 while each.num_items > 0:
#                     extracted = each.remove(each.head.key)
#                     new_table.put(extracted[0], extracted[1])
#
#         self.table = new_table.table
#         self.num_items = new_table.num_items
#         self.table_size = new_table.table_size
#         self.num_collisions = new_table.num_collisions

def hash_string(string, size):
    """ Generate a hash of a string
        Args:
            string(str): the string being hashed
            size(int): the size of the hash table
        Returns:
            int: the hash value of the string
    """

    hash_val = 0
    for val in string:
        hash_val = (hash_val * 31 + ord(val)) % size
    return hash_val

def import_stopwords(filename, hashtable):
    """ Import a list of stopwords from a file
        Args:
            filename(str): filename of list of words
            hashtable(HashTable): hash table object words will be added to
        Returns:
            HashTable: hash table object with the words added to it
    """

    file = open(filename, 'r')
    word_line = file.readline()
    word_list = word_line.split()
    for word in word_list:
        hashtable.put(word, 0)

    file.close()
    return hashtable
