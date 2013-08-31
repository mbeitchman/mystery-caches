

import caches
import pprint

MAX_BLOCK_SIZE = 32 # block size is always a power of 2
MAX_CACHE_SIZE = 2 ** 16 # cache size is always a power of 2
MAX_ASSOC = 8 # associativity is always a power of 2
MAX_VBUFFER_SIZE = 6 # victim buffer size is just a natural number

def find_block_size( cache ):
    """Returns block size (in bytes) of the cache."""
    cache.reset()
    cache.access(0)
    for i in range(1,MAX_BLOCK_SIZE+1):
        if(cache.access(i) == False):
            break

    cache.reset()
    return i

def find_cache_size( cache, block_size ):
    """Returns total size (in bytes) of the cache."""
    done = False
    for i in range(1,MAX_CACHE_SIZE+1):
        for j in range(2**i):
            cache.access(j)

        for k in range(2**i):
            if cache.access(k) == False:
                done = True
                break
        if done == True:
            break
        else:
            cachesize = i

        cache.reset()
        
    cache.reset()

    return 2**cachesize

def find_associativity( cache, size, block_size ):
    """Returns associativity of the cache for a cache without a
    victim buffer.
    """
    assert not cache.has_victim_buffer()
    cache.reset()
    return discover_associativity( cache, size, block_size )
    

def discover_associativity( cache, size, block_size ):

    blockbits = (block_size-1).bit_length()
    indexbits = (size-1).bit_length()

    cache.reset()
    # initialize test values
    values = [0]
    for i in range(0,MAX_ASSOC):
        values.append(2**(blockbits+indexbits+(i)))
    # test associativity
    for i in range(1, MAX_ASSOC+1):
        # add values to the cache
        for j in range(i+1):
            cache.access(values[j])

        # test how many of the values are still in the cache
        for k in range(i):
            if(cache.access(values[k]) == False):
                return i

        cache.reset()

def discover_associativity_with_vb( cache, size, block_size ):

    blockbits = (block_size-1).bit_length()
    indexbits = (size-1).bit_length()
    initialsize = 0
    assoc = 0
    totalsize = 0

    cache.reset()
    # initialize test values
    values = [0]
    for i in range(0,MAX_ASSOC):
        values.append(2**(blockbits+indexbits+(i)))

    # second set of test values
    values1 = [block_size*1]
    for i in range(0,MAX_ASSOC):
        values1.append(values1[0] + (2**(blockbits+indexbits+(i))))

    # test associativity
    for i in range(1, MAX_ASSOC+1):
        # add values to the cache
        for j in range(i+1):
            cache.access(values[j])

        # test how many of the values are still in the cache
        for k in range(i):
            if(cache.access(values[k]) == False):
                initialsize = i
                break

        cache.reset()

        if initialsize != 0:
            break

    cache.reset()

    totalsize = initialsize

    # test associativity
    for i in range(initialsize):
            cache.access(values[i])
    
    # test associativity
    for i in range(initialsize):
            cache.access(values1[i])

    # see what is still in the cache
    while initialsize > 0:
        if(cache.access(values[initialsize-1]) == True):
            assoc = assoc + 1
        else:
            break
        initialsize = initialsize - 1

    return assoc, totalsize-assoc

def find_victim_buffer_size( cache, size, block_size ):
    """Returns a tuple of (associativity,victim buffer size) for a
    cache with a victim buffer.
    """
    assert cache.has_victim_buffer()

    cache.reset()

    return discover_associativity_with_vb(cache, size, block_size) 

def main(cache):
    answers = {}

    block_size = find_block_size(cache)
    answers['block size'] = block_size

    size = find_cache_size(cache, block_size)
    answers['cache size'] = size

    if cache.has_victim_buffer():
        assoc,vb_size = find_victim_buffer_size(cache, size, block_size)
        answers['victim buffer size'] = vb_size
        answers['associativity'] = assoc
    else:
        answers['associativity'] = find_associativity(cache, size, block_size)

    return answers

if __name__ == "__main__":
    # test your code by creating different caches here
    cache = caches.Cache( bsize=2, assoc=4, size=64, vbsize=None )
    #cache = caches.Cache( bsize=2, assoc=1, size=64, vbsize=None ) # direct-mapped
    #cache = caches.Cache( bsize=2, assoc=4, size=8, vbsize=None ) # fully-associative
    #cache = caches.Cache( bsize=4, assoc=2, size=16, vbsize=1) # victim buffer
    #cache = caches.Cache( bsize=4, assoc=1, size=16, vbsize=1) # direct-mapped + victim buffer

    pprint.pprint(main(cache))