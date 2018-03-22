# Tianyi Lan #
# Challenge1: autocomplete-me #

import sys
import heapq

# Build Node class with attributes
class Node:
    def __init__(self, word=None, weight=-1):
        self.word = word
        self.isWord = False
        self.weight = weight
        self.childMax = -1
        self.children = {}

    # This is used to break ties when two nodes in autocomplete have same weights
    # Returns true for lt(less than) and returns any of the two
    def __lt__(self, other):
        return True

# Build Trie class based on Node
class Trie:
    #set root as a node
    def __init__(self):
        self.root = Node()

    def addWord(self, wordStr, weight):
        """ This function adds words and weights into the trie data structure"""
        current = self.root

        #adds letters to each node
        for char in wordStr:
            # update childMax if current weight is bigger
            if weight > current.childMax:
                current.childMax = weight
            # creates new node if it's a new letter
            if char not in current.children:
                current.children[char] = Node()
                
            current = current.children[char]

        # for the last letter of a word, adds weight and word
        current.isWord = True
        current.word = wordStr
        current.weight = weight

    def search(self, wordStr):
        """ This function finds the node in the trie with the input word string"""
        if len(wordStr) == 0:
            raise ValueError("The search string can not be empty.")
        current = self.root
        for index in range(0, len(wordStr)):
            char = wordStr[index]
            if char not in current.children:
                raise ValueError("This word string does not exist in Trie.")
            current = current.children[char]
        return current


def read_terms(filename, encoding='UTF-8'):
    """ This function reads in a file to make a trie"""
    trie = Trie()
    with open(filename, "r", encoding=encoding) as file:
        next(file)
        for line in file:
            if line != "\n":
                out = line.strip('\n').split('\t')
                trie.addWord(wordStr=out[1], weight=int(out[0]))
    return trie


def autocomplete(wordStr, words, num):
    """ This function completes the task and finds the word list
        with maximum weights
    """

    # find the node that the input word string is on
    try:
        prefix = words.search(wordStr)
    # catch the error if there is one and return empty list
    except ValueError:
        return []
    
    queue = []
    heapq.heapify(queue)

    results = []
    # push word with its weight to queue if input is a word
    if prefix.isWord:
        heapq.heappush(queue, (-prefix.weight, prefix, True))
    # push input word string with its children max
    heapq.heappush(queue, (-prefix.childMax, prefix, False))
    
    while len(queue) > 0 and len(results) < num:
        # pop the largest in the queue
        priority, node, aWord = heapq.heappop(queue)
        # add to output list if poped node is a word
        if aWord:
            results.append((-priority, node.word))

        # check its children till find the word with this children max
        else:
            for child in node.children:
                if node.children[child].isWord:
                    heapq.heappush(queue, (-node.children[child].weight, node.children[child], True))
                heapq.heappush(queue, (-node.children[child].childMax, node.children[child], False))

    return results


# driver script
if __name__ == "__main__" and len(sys.argv) > 1:
    wordStr = sys.argv[1]
    words = read_terms(sys.argv[2])
    num = int(sys.argv[3])
    print("The words with largest weights are:", autocomplete(wordStr, words, num))
