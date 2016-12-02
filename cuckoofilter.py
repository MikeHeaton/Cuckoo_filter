"""
Implement a Cuckoo Filter class
Written for Recurse Center Algoclub by Mike Heaton, 2/12/16
"""
import math
fails = []

class CuckooFilter():
    def __init__(self, length, bucket_size,
                maxinsertiontime=500, fingerprintlen = 2**6):
        """Length x array, each of which is a set(?) of buckets.
        Can't do a set, could do a multiset or Counter"""
        self.length = length
        self.bucket_size = bucket_size
        self.maxinsertiontime = maxinsertiontime
        self.hashtable = [Bucket([], bucket_size) for t in range(self.length)]
        self.hash = self._makehash(length)
        self.fingerprint = (lambda x: bin(self._makehash(fingerprintlen)(x)))

        """TODO: allow creation from iterable"""
        """TODO: better fingerprint function"""

    def __str__(self):
        return "\n".join([str(i)+" : "+str(self.hashtable[i]) for i in range(self.length)])

    def add(self, item):
        failure = self._iteradd(item, None, 0)
        if failure != 0:
            fails.append(item)
            itemhash1, itemhash2, itemfprint = self.gethashes_and_fprint(item)
            '''print("""
            Insertion of {} failed, data structure is FULL.
            Hashes: {} {}; fingerprint: {}
            Contents: {}
                      {}""".format(item, itemhash1, itemhash2, itemfprint,
                                    self.hashtable[itemhash1], self.hashtable[itemhash2]))'''

    def _iteradd(self, item, bumped_location, num_attempts):
        itemhash1, itemhash2, itemfprint = self.gethashes_and_fprint(item)

        if bumped_location != itemhash1:
            failedinsert = self.hashtable[itemhash1].add(itemfprint)
            if failedinsert == 0:
                return 0

        if bumped_location != itemhash2:
            failedinsert = self.hashtable[itemhash2].add(itemfprint)
            if failedinsert == 0:
                return 0

        """If both insertion attempts fail, bump an element out of the
            second position and reinsert it somewhere else."""
        if num_attempts >= self.maxinsertiontime:
            return 1
        if bumped_location != itemhash1:
                nextitem = self.hashtable[itemhash2].pop()
                shouldbeok = self.hashtable[itemhash2].add(itemfprint)
                if shouldbeok != 0:
                    print("Add failed after deletion, this shouldn't have happened lol.")
                return self._iteradd(nextitem, itemhash2, num_attempts + 1,)
        else:
                nextitem = self.hashtable[itemhash1].pop()
                shouldbeok = self.hashtable[itemhash1].add(itemfprint)
                if shouldbeok != 0:
                    print("Add failed after deletion, this shouldn't have happened lol.")
                return self._iteradd(nextitem, itemhash1, num_attempts + 1, )

    def remove(self, item):
        itemhash1, itemhash2, itemfprint = self.gethashes_and_fprint(item)

        if itemfprint in self.hashtable[itemhash1]:
            self.hashtable[itemhash1].remove(itemfprint)
        else:
            self.hashtable[itemhash2].remove(itemfprint)

    def query(self, item):
        itemhash1, itemhash2, itemfprint = self.gethashes_and_fprint(item)

        if itemfprint in self.hashtable[itemhash1] or item in self.hashtable[itemhash2]:
            return True
        else:
            return False

    def _makehash(self, length):
        """Make a hash function which hashes something to within
        the hashtable length."""
        def hashfunction(x):
            return hash(x) % length
        return hashfunction

    def gethashes_and_fprint(self, item):
        itemhash1 = self.hash(item)
        itemfprint = self.fingerprint(item)
        #print(itemhash1, itemfprint, self.hash(itemfprint))
        itemhash2 = (itemhash1 ^ self.hash(itemfprint)) % self.length
        if itemhash1 == itemhash2:
            itemhash2 = itemhash2 + 1 % self.length

        return itemhash1, itemhash2, itemfprint

class Bucket(list):
    def __init__(self, members, bucketsize):
        super(Bucket,self).__init__(members)
        self.maxsize = bucketsize

    def add(self, item):
        """Input: item to be added.
        Output: 0 if the insert succeeds (there is space in the bucket)
                1 if the insert fails (no space in the bucket)."""
        if len(self) < self.maxsize:
            self.insert(0, item)
            return 0
        else:
            return 1

    def remove(self, item):
        if item in self:
            list.remove(self, item)

    """'in' and 'len' and 'pop' methods are identical to list, so don't implement it here."""


M = 9750
K = 8
testfilter = CuckooFilter(M, K, maxinsertiontime=500, fingerprintlen = 2**10)

f = open('shakespeare.txt', 'r')
allstring = f.read()

words = set(allstring.split())

for word in words:
    testfilter.add(word)

print('''----------
{} words added.
{}/{} failures witnessed. ({}%)
{}/{} registers filled.   ({}%)'''.format(len(words), len(fails), len(words),
                                    round(100*len(fails)/float(len(words)),4),
                                    len(words)-len(fails),M*K, round(100*(len(words)-len(fails))/float(M*K),2)))

print(testfilter.query("Macbeth"))
print(testfilter.query("Television"))
print(testfilter.remove("Macbeth"))
print(testfilter.query("Macbeth"))
