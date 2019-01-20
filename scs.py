#!/usr/bin/env python
from __future__ import print_function
from random import randint as rand

def superseq(a, b):
    a_idx, b_idx = 0, 0
    hits = 0
    while a_idx < len(a) and b_idx < len(b):
        hc = False
        for i in range(b_idx, len(b)):
            if a[a_idx] == b[i]:
                hits += 1
                a_idx += 1
                b_idx = i
                hc = True
                break
        if not hc:
            a_idx += 1
    return hits

class GA(object):
    def __init__(self, s1, s2):
        self._s1 = s1
        self._s2 = s2
        self._chrs = sorted(set(s1 + s2))
        self._len = len(self._chrs)
        self._len_lower = min(len(self._s1), len(self._s2))
        self._len_upper = max(len(self._s1), len(self._s2))

    def random_char(self):
        return self._chrs[rand(0, self._len-1)]

    def random_length(self):
        return rand(self._len_upper, self._len_lower + self._len_upper)

    def random_individual(self):
        return ''.join( [self.random_char() for _ in range(self.random_length())] )

    def mutate(self, ind):
        state = rand(0, 2)
        if state == 0:
            if len(ind) <= 2:
                return ind
            idx = rand(0, len(ind)-2)
            return ind[:idx] + ind[idx+2:]
        if state == 1:
            if len(ind) <= 2:
                return ind
            idx = rand(0, len(ind)-2)
            return ind[:idx] + self.random_char() + ind[idx:]
        if state == 2:
            if len(ind) <= 2:
                return ind
            idx = rand(0, len(ind)-2)
            return ind[:idx] + self.random_char() + ind[idx+1:]


    def fitness(self, ind):
        supseq_score = superseq(self._s1, ind) + superseq(self._s2, ind)
        return -(2*supseq_score - len(ind))

    def crossover(self, ind1, ind2):
        if len(ind1) >= 3:
            i1 = rand(0, len(ind1) - 2)
            j1 = rand(i1, len(ind1) - 1)
            ind1 = ind1[i1:j1]
        if len(ind2) >= 3:
            i2 = rand(0, len(ind2) - 2)
            j2 = rand(i2, len(ind2) - 1)
            ind2 = ind2[i2:j2]
        return ind1 + ind2

    def run(self, size=10, its=1000):
        pool = [ self.random_individual() for _ in range(size) ]
        for i in range(its):
            print(1+i, '\n\t'.join(pool))
            for i in range(size//2):
                pool.append(self.mutate(pool[i]))
            for i in range(10):
                for j in range(10):
                    if i != j:
                        pool.append(self.crossover(pool[i], pool[j]))
            pool = sorted(set([p for p in pool if p]), key=self.fitness)[:size]
        return pool[:10]


def main(s1, s2):
    ga = GA(s1, s2)
    print(ga.run())

if __name__ == '__main__':
    from sys import argv
    if len(argv) != 3:
        exit('Usage: scs s1 s2')
    main(argv[1], argv[2])
