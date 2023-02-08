"""
wordpath.py

@author: Snehil Sharma
"""


from collections import deque
import string
import sys


"""makes mini wordlist based on the given words"""
def make_shortlist(dict_name: string, word_len: int, slist: set):
    with open(dict_name) as d:

        for line in d:
            line = line.strip("\n")
            if len( line) == word_len: 
                slist.add(line)

    d.close


"""finds neighbors that differ by 1 letter for every neighbor until target is found"""
def word_neighbors(dictionary: string, start_word: string, end_word: string):
    word_len = len(start_word)

    short_list = set()

    make_shortlist(dictionary, word_len, short_list)

    if(end_word not in short_list):
        print("no solution")
        exit(0)

    # queue for finding neighbors of neighbors
    wordpath_queue = deque()
    wordpath_queue.append(start_word)

    # set to keep track of visited words
    visited_set = set()
    visited_set.add(start_word)

    word_nbr_lvl = dict()


    while len(wordpath_queue)>0:

        level_words = list()

        current_word = wordpath_queue.popleft()

        visited_set.add(current_word)

        current_word_split = [*current_word]

        # find neighbors
        for i in range(word_len):

            temp = current_word_split[i]

            for letter in string.ascii_lowercase:

                if(letter is current_word_split[i]):
                    continue
                
                current_word_split[i] = letter

                new_word = "".join(current_word_split)

                if(new_word in visited_set):
                    continue

                # when target found    
                if(new_word == end_word):
                    
                    level_words.append(new_word)
                    word_nbr_lvl[current_word] = level_words

                    # return the neighbor dictionary
                    return word_nbr_lvl

                # valid neighbor found
                if(new_word in short_list):

                    wordpath_queue.append(new_word)
                    level_words.append(new_word)
                    short_list.remove(new_word)
                    visited_set.add(new_word)

            current_word_split[i] = temp

        # update the neighbor dictionary
        word_nbr_lvl[current_word] = level_words


# finds the parent of the given neighbor
def find_val(word, dict):

    for key in dict:

        val = dict.get(key)

        for i in range(len(val)):
            if(val[i] == word):
                return key



# finds the word path to the target from starting word     
def word_path(dictionary: string, start_word: string, end_word: string):

    if(len(start_word) != len(end_word)):
        return "no solution"

    dict_name_check = dictionary.split(".")

    if(len(dict_name_check)==1):
        dict_name = dictionary + ".txt"

    else:
        dict_name = dictionary

    # find neighbor list for all neighbors
    nbr_dict = word_neighbors(dict_name, start_word, end_word)

    path_list = list()

    target = start_word

    begin = end_word

    # build the path from the reverse side
    find_path_recur(nbr_dict, target, begin, path_list)

    # flip the path for desired result
    path_list.reverse()

    return path_list

    
# recursively finds the path from end word to start word, when neighbor list given
def find_path_recur(dict, target: string, begin: string, path: list):

    if(begin == target):
        path.append(target)
        return path

    path.append(begin)

    key = find_val(begin, dict)

    find_path_recur(dict, target, key, path)



def main():

    dict_name = sys.argv[1]
    start_word = sys.argv[2]
    end_word = sys.argv[3]

    print(word_path(dict_name, start_word, end_word))



if __name__ == "__main__":
    main()


                    

