import autocomplete_me as ac
import unittest
import random
import string
from autocomplete_me import Trie

## This class contains unit tests for function autocomplete()##
class autocomplete(unittest.TestCase):
    
    #case 1: test for wiktionary
    def test_autocomplete_for_wiki(self):
        wikiTrie = ac.read_terms("wiktionary.txt")
        result = ac.autocomplete("the", wikiTrie, 5)
        expected = [(5627187200, 'the'), (334039800, 'they'), (282026500, 'their'), (250991700, 'them'), (196120000, 'there')] 
        self.assertEqual(expected, result)
    #case 2: test for pokemon
    def test_autocomplete_for_pokemon(self):
        pokTrie = ac.read_terms("pokemon.txt")
        result = ac.autocomplete("Sh", pokTrie, 5)
        expected = [(81075, 'Sharpedo'), (55024, 'Shedinja'), (43597, 'Shaymin'), (42367, 'Shuckle'), (31091, 'Shiftry')]
        self.assertEqual(expected, result)
    #case 3: test for babynames
    def test_autocomplete_for_babynames(self):
        babyTrie = ac.read_terms('baby-names.txt')
        result = ac.autocomplete("L", babyTrie, 5)
        expected = [(16709, 'Liam'), (13066, 'Logan'), (10623, 'Lucas'), (9319, 'Landon'), (8930, 'Luke')]
        self.assertEqual(expected, result)
    #case 4: test for movies
    def test_autocomplete_for_movies(self):
        movTrie = ac.read_terms('movies.txt')
        result = ac.autocomplete("The", movTrie, 5)
        expected = [(623357910, 'The Avengers (2012)'), (534858444, 'The Dark Knight (2008)'), (448139099, 'The Dark Knight Rises (2012)'), (422783777, 'The Lion King (1994)'), (408010692, 'The Hunger Games (2012)')]
        self.assertEqual(expected, result)
    #case 5: test for not-in-trie input
    def test_autocomplete_for_input_not_in_trie(self):
        babyTrie = ac.read_terms('baby-names.txt')
        result = ac.autocomplete("XXX", babyTrie, 5)
        expected = []
        self.assertEqual(expected, result)
    #case 6: test for empty input
    def test_autocomplete_for_empty_input(self):
        pokTrie = ac.read_terms("pokemon.txt")
        result = ac.autocomplete("", pokTrie, 5)
        expected = []
        self.assertEqual(expected, result)

#test for addWord() function in Trie
class trie_addWord(unittest.TestCase):
    def test_addWord_for_movies(self):
        T =Trie()
        T.addWord('a', 73)
        self.assertEqual(T.search('a').weight, 73)
        self.assertEqual(T.search('a').word, 'a')
        T.addWord('at', 55)
        self.assertEqual(T.search('a').childMax, 55)
        self.assertEqual(T.search('at').weight, 55)
        self.assertEqual(T.search('at').childMax, -1)
        T.addWord('act', 28)
        self.assertEqual(T.search('a').childMax, 55)
        self.assertEqual(T.search('ac').childMax, 28)
        self.assertEqual(T.search('ac').word, None)
        self.assertEqual(T.search('act').weight, 28)
        
#test for search() function in the Trie
class trie_search(unittest.TestCase):
    def test_for_search(self):
        T = Trie()
        T.addWord('pet', 58)
        self.assertEqual(T.search('p').weight, -1)
        self.assertEqual(T.search('p').childMax, 58)
        self.assertEqual(T.search('pe').word, None)
        self.assertEqual(T.search('pe').isWord, False)
        self.assertEqual(T.search('pet').word, 'pet')
        self.assertEqual(T.search('pet').weight, 58)
        self.assertRaises(ValueError, T.search, 'te')
        self.assertRaises(ValueError, T.search, '')

# Randomized test for trie building
class randomized_trie(unittest.TestCase):
    def test_for_random_file(self):
        #generate file of random words and weights
        T=Trie()
        wordList = []
        size = random.randint(600, 2500)
        noRepeat = {}
        for index in range(size):
            ranStr = ''.join([random.choice(string.ascii_lowercase) for i in range(random.randint(2,9))])
            ranWeight = random.randint(1,100000)
            #check for no repeating words
            if ranStr not in noRepeat:
                noRepeat[ranStr] = 1
                wordList.append((ranWeight, ranStr))
                T.addWord(wordStr = ranStr, weight = ranWeight)

        #sort wordList in desceding weight
        wordList.sort(reverse=True)
        result = []
        searchStr = 't'
        for index in range(len(wordList)):
            if len(result) == 5:
                break
            else:
                current = wordList[index][1]
                if current[0] == searchStr:
                    result.append(wordList[index])
                    
        #check the two have same results
        self.assertEqual(result, ac.autocomplete('t', T, 5))       


if __name__ == "__main__":
    unittest.main()
