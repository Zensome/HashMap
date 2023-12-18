# Course: Data Structures
# Assignment: HashMap
# Description: Implementation of hashmap using open addressing for collision resolution.


from a6_include import (
    DynamicArray,
    DynamicArrayException,
    HashEntry,
    hash_function_1,
    hash_function_2,
)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ""
        for i in range(self._buckets.length()):
            out += str(i) + ": " + str(self._buckets[i]) + "\n"
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor**2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Update the key / value pair in the hash map. If the given key already exists,then replace
        the value with the new one; otherwise add a new key / value pair to the hash map.

        :param key: key to be updated
        :param value: value of the key

        :return: None
        """
        # if current load factor >= 0.5, double the capacity of the hash map
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # compute the hash of the key
        hash_value = self._quadratic_probe_for_key(key)

        # if the key already exists, update the value
        if hash_value is not None:
            self._buckets[hash_value].value = value
            return

        # if the key does not exist, find an empty spot
        hash_value = self._quadratic_probe_for_spot(key)

        # then insert the element to the spot
        self._buckets[hash_value] = HashEntry(key, value)
        self._size += 1

    def _quadratic_probe_for_spot(self, key: str) -> int:
        """
        A helper function to do quadratic probing to find an empty spot in the hash map

        :param key: key to be hashed

        :return: index of the empty spot
        """
        # compute the hash of the key
        initial_hash_value = self._hash_function(key) % self._capacity
        curr_element = self._buckets[initial_hash_value]

        if not curr_element or curr_element.is_tombstone:
            return initial_hash_value

        # using the quadratic probing function i_curr = ( i_prev + j^2 ) % m
        # continue probing until an empty spot (None or tombstone) is found
        new_hash_value = initial_hash_value
        j = 1
        while curr_element and curr_element.is_tombstone is False:
            new_hash_value = (initial_hash_value + j**2) % self._capacity
            curr_element = self._buckets[new_hash_value]
            j += 1

        return new_hash_value

    def _quadratic_probe_for_key(self, key: str) -> int:
        """
        A helper function to do quadratic probing to find the key in the hash map

        :param key: key to be hashed

        :return: index of the key if found, else None
        """
        # using the same quadratic probing function
        initial_hash_value = self._hash_function(key) % self._capacity
        curr_element = self._buckets[initial_hash_value]

        if curr_element is None:
            return None

        # Check if the initial hash value is the correct key
        if curr_element.key == key and not curr_element.is_tombstone:
            return initial_hash_value

        # continue probing until the key is found or an empty spot (None) is found
        new_hash_value = initial_hash_value
        j = 1
        while curr_element:
            if curr_element.key == key and curr_element.is_tombstone is False:
                return new_hash_value

            new_hash_value = (initial_hash_value + j**2) % self._capacity
            curr_element = self._buckets[new_hash_value]
            j += 1

        return None

    def resize_table(self, new_capacity: int) -> None:
        """
        Change the capacity of the internal hash table. All existing key/value are maintained and rehashed.

        :param new_capacity: new capacity of the hash map

        :return: None
        """
        # check if new capacity is less than the current number of elements
        if new_capacity < self._size:
            return

        # copy the current buckets and capacity
        old_buckets = self._buckets
        old_capacity = self._capacity

        # initialize a new buckets with the new capacity, which is a prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # reset the hash map internal states so its empty
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        self._size = 0

        # populate the new buckets with None like in the constructor
        for _ in range(new_capacity):
            self._buckets.append(None)

        # rehash every elements in the old buckets
        for element_index in range(old_capacity):
            element = old_buckets[element_index]

            if element and element.is_tombstone is False:
                self.put(element.key, element.value)

    def table_load(self) -> float:
        """
        Return the current hash table load factor.

        :return: load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Return the number of empty buckets in the hash table.

        :return: number of empty buckets
        """
        return self._capacity - self._size

    def get(self, key: str) -> object:
        """
        Return the value of the given key. If the key does not exist, return None.

        :param key: key to look for

        :return: element of the key
        """
        # compute the hash of the key using quadratic probing
        hash_value = self._quadratic_probe_for_key(key)

        # return the value if the key is found
        if hash_value is not None:
            element = self._buckets[hash_value]
            return element.value

        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False

        :param key: key to look for

        :return: boolean
        """
        # compute the hash of the key using quadratic probing
        hash_value = self._quadratic_probe_for_key(key)

        if hash_value is not None:
            return True

        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its value from the hash map if it exists.

        :param key: key to be removed

        :return: None
        """
        # compute the hash of the key using quadratic probing
        hash_value = self._quadratic_probe_for_key(key)

        # if the key exists, remove the key by making it a tombstone
        if hash_value is not None:
            self._buckets[hash_value].is_tombstone = True
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array which contains all the keys and values stored in the hash map.

        :return: dynamic array with key/value tuples
        """
        # create a dynamic array
        key_value_pairs = DynamicArray()

        # populate the array with valid key/value pairs
        for element_index in range(self._capacity):
            element = self._buckets[element_index]
            if element and not element.is_tombstone:
                key_value_pairs.append((element.key, element.value))

        return key_value_pairs

    def clear(self) -> None:
        """
        Clear the contents of the hash map.

        :return: None
        """
        # reset the buckets to None's
        for element_index in range(self._capacity):
            self._buckets[element_index] = None

        self._size = 0

    def __iter__(self):
        """
        Return an iterator for the hash map so it can iterate across itself.

        :return: iterator
        """
        self._index = 0

        return self

    def __next__(self):
        """
        Return the next element in the hash map based on the current location of the iterator.

        :return: next element in hash map
        """
        try:
            element = self._buckets[self._index]

            # skip empty elements and tombstones
            while not element or element.is_tombstone:
                self._index += 1
                element = self._buckets[self._index]

        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return element


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":
    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        # key = "str" + str(i)
        # print("key: ", key)
        # print("original hash value: ", m._hash_function(key) % m._capacity)
        m.put("str" + str(i), i * 100)

        if i % 25 == 24:
            print(
                m.empty_buckets(),
                round(m.table_load(), 2),
                m.get_size(),
                m.get_capacity(),
            )

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put("str" + str(i // 3), i * 100)
        if i % 10 == 9:
            print(
                m.empty_buckets(),
                round(m.table_load(), 2),
                m.get_size(),
                m.get_capacity(),
            )

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put("key1", 10)
    print(m.get_size(), m.get_capacity(), m.get("key1"), m.contains_key("key1"))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get("key1"), m.contains_key("key1"))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(
                f"Check that the load factor is acceptable after the call to resize_table().\n"
                f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5"
            )

        m.put("some key", "some value")
        result = m.contains_key("some key")
        m.remove("some key")

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(
            capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2)
        )

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put("key1", 10)
    print(round(m.table_load(), 2))
    m.put("key2", 20)
    print(round(m.table_load(), 2))
    m.put("key1", 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put("key" + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put("key1", 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put("key2", 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put("key1", 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put("key4", 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put("key" + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get("key"))
    m.put("key1", 10)
    print(m.get("key1"))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key("key1"))
    m.put("key1", 10)
    m.put("key2", 20)
    m.put("key3", 30)
    print(m.contains_key("key1"))
    print(m.contains_key("key4"))
    print(m.contains_key("key2"))
    print(m.contains_key("key3"))
    m.remove("key3")
    print(m.contains_key("key3"))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get("key1"))
    m.put("key1", 10)
    print(m.get("key1"))
    m.remove("key1")
    print(m.get("key1"))
    m.remove("key4")

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put("20", "200")
    m.remove("1")
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put("key1", 10)
    m.put("key2", 20)
    m.put("key1", 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put("key1", 10)
    print(m.get_size(), m.get_capacity())
    m.put("key2", 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print("K:", item.key, "V:", item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove("0")
    m.remove("4")
    print(m)
    for item in m:
        print("K:", item.key, "V:", item.value)
