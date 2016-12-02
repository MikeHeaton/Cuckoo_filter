# Cuckoo_filter
Python implementation of the cuckoo filter data structure. 
Provides efficient compression and membership-testing abilities with O(1) add, query and remove functions. Cool!

Tested on the complete works of Shakespeare:
67108 words added.
0/67108 failures witnessed. (0.0%)
67108/78000 registers filled.   (86.04%)

**Description**
---------

Cuckoo filters are a space- and time- efficient structure for storing and querying very large sets of strings. 
They are great for testing whether an element is a member of a big set: query is O(1) time.
They are great for adding elements to the big set: addition is O(1) time.
They are better than, say, rainbow tables because we can remove elements as well... in O(1) time.
They are great for space efficiency: really big elements are hashed down to a couple of bytes.

They are bad for printing out the big set once its been created. This isn't very possible unless we're using a
reversible fingerprinting function (in which case we probably lose the space saving.)

More information here: https://www.cs.cmu.edu/~dga/papers/cuckoo-conext2014.pdf
Blog post upcoming on www.mike-heaton.com.
