import autocomplete_me as ac
import time
import cProfile

#times read_terms() process   
begin1 = time.clock()
words = ac.read_terms("movies.txt")
stop1 = time.clock()
diff1= stop1 - begin1
print("Building the Trie takes: {}".format(diff1))
print("\n")

#times autocomplete() process
begin2 = time.clock()
ac.autocomplete("The", words, 5)
stop2 = time.clock()
diff2 = stop2 - begin2
print("Finishing autocomplete for 'The' takes: {}".format(diff2))
print("\n")

#times all functions separately with "The" as search string and "movies.txt"
# as text input
cProfile.run('ac.autocomplete("The", ac.read_terms("movies.txt"), 5)')
