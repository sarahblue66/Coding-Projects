import autocomplete_me as ac
import matplotlib.pyplot as plt
from autocomplete_me import Trie
import random
import time

# this class generates random subsets and then plot filesize vs performance
class graph:
    def random_file(newfile, filename="movies.txt", encoding='UTF-8'):
        ''' creates a text file that is a random subset of a given file
            filename is the original file's name
            newfile is the name of the random subset
        '''
        with open(filename, "r", encoding=encoding) as file:
            allLines = file.readlines()
            fileSize = random.randrange(10000, 100000)
            lines = random.sample(allLines[1:], fileSize)

        with open(newfile, "w", encoding=encoding) as file:
            for line in lines:
                strLine = str(line)
                file.write(strLine)
        return [newfile, fileSize]
                                  
  
    time1, time2, size = [], [], []
    for i in range(30):
        [randFile, fileSize] = random_file("rand_i", "movies.txt")
        #times building trie and records time to list
        start_i = time.clock()
        trie = ac.read_terms(randFile)
        size_i = fileSize
        #adds filesize to size list
        size.append(size_i)
        running1 = time.clock() - start_i
        #times matcher and records time to list
        time1.append(running1)
        newStart_i = time.clock()
        ac.autocomplete('T', trie, 5)
        running2 = time.clock() - newStart_i
        time2.append(running2)
        
    plt.title('Performance by Input Size')
    plt.xlabel('Input Size')
    plt.ylabel('Execution Time (s)')
    plt.grid(True)
    plt.xlim(10000,100000)
    plt.ylim(0,10)

    #plot filesize against two time lists with legends    
    plt.scatter(size, time1, color="red", label="Loading data")
    plt.scatter(size, time2, color="blue", label="Matcher")
    plt.legend()

    plt.show()
