""" Search Engine Implementation with HashTables
    Course: CPE202
    Quarter: Spring 2020
    Author: Chris Linthacum
"""

import re
import os
import math

from hashtables import HashTableLinear, import_stopwords

class SearchEngine:
    """ Search engine class to build an inverted index of documents stored
        in a specified directory and provides a functionality to search
        documents with query terms.
        Attributes:
            directory (str): a directory name
            stopwords (HashMap): a hash table containing stop words
            doc_length (HashMap): a hash table containing the total number of
                                  words in each document
            term_freqs (HashMap): a hash table of hash tables for each term.
                                  Each hash table contains the frequency of
                                  the term in documents (document names are
                                  the keys and the frequencies of the values)
    """

    def __init__(self, directory, stopwords):
        """ Initialize the data structure by taking a directory name and a
            hash table containing stopwords.
            Args:
                directory (str): a directory name
                stopwords (HashMap): a hash table containing stopwords
        """

        self.doc_length = HashTableLinear()
        self.term_freqs = HashTableLinear()
        self.stopwords = stopwords
        self.file_list = []
        self.index_files(directory)

    def __eq__(self, other):
        """ Compares the data structure to other"""
        return isinstance(other, SearchEngine) and \
            self.doc_length == other.doc_length and \
            self.term_freqs == other.term_freqs and \
            self.stopwords == other.stopwords

    def __repr__(self):
        """ How the data structure is represented"""
        return "SearchEngine Instance:\n" + str(self.term_freqs)

    def read_file(self, infile):
        """ Reads all words contained in the file except for stop words
            Args:
                infile (str): the path to a file
            Returns:
                list: a list of str read from a file
        """
        with open(infile, 'r') as file:
            str_list = file.readlines()
        for index, line in enumerate(str_list):
            str_list[index] = line.rstrip('\n')
        return str_list

    def parse_words(self, lines):
        """ Splits strings into words by spaces, converts words to lower
            cases, and removes newline chars, parentheses, brackets, and
            punctuations
            Args:
                lines (list): a list of strings
            Returns:
                list: a list of words
        """
        words = []
        for each in lines:
            line_list = each.split()
            for index, word in enumerate(line_list):
                line_list[index] = re.sub('[\W_]+', '', word)
            words += line_list

        for index, word in enumerate(words):
            words[index] = word.lower()

        words = self.exclude_stopwords(words)

        return words

    def exclude_stopwords(self, terms):
        """ Exclude stopwords from the list of terms
            Args:
                terms (list): list of terms to be cleaned of stop words
            Returns:
                  list: a list of str with stopwords removed
        """
        out_list = []
        for each in terms:
            if each not in self.stopwords:
                out_list.append(each)

        return out_list

    def count_words(self, file_path_name, words):
        """ Count words in a file and store the frequency of each word in the
            term_freqs hash table. The keys of the term_freqs hash table shall
            be words. The values of the term_freqs hash table shall be hash
            tables (term_freqs is a hash table of hash tables). The keys of
            the hash tables (inner hash table) stored in the term_freqs shall
            be file names. Values of inner hash tables shall be the frequencies
            of words.

        Args:
            file_path_name (str): the file name
            words (list): a list of words
        """
        self.doc_length.put(file_path_name, len(words))

        while len(words) > 0:
            current_word = words[0]
            word_freq = 0

            word_freq = words.count(current_word)

            try:
                while True:
                    words.remove(current_word)
            except ValueError:
                pass

            # If the word already in term_freqs, retrieve the doc freq table
            # otherwise, create a new hash table
            if current_word in self.term_freqs:
                freq_hash = self.term_freqs.get(current_word)
            else:
                freq_hash = HashTableLinear()

            freq_hash.put(file_path_name, word_freq)
            self.term_freqs.put(current_word, freq_hash)

    def index_files(self, directory):
        """ Processes a directory and makes an index of all the files
            Args:
                directory (str): the directory being indexed
        """

        dir_list = os.listdir(directory)
        full_dir_list = []
        for index, item in enumerate(dir_list):
            full_dir_list.append(os.path.join(directory, item))
        file_list = []
        for index, item in enumerate(full_dir_list):
            if os.path.isfile(item):
                parts = os.path.splitext(item)
                if parts[1] == '.txt':
                    file_list.append(full_dir_list[index])

        # The list of txt files in directory is now in file_list
        self.file_list = file_list

        for file in file_list:
            str_list = self.read_file(file)
            words = self.parse_words(str_list)
            self.count_words(file, words)

    def get_wf(self, tf):
        """ computes the weighted frequency
            Args:
                tf (float): term frequency
            Returns:
                float: the weighted frequency
        """

        if tf > 0:
            wf = 1 + math.log(tf)
        else:
            wf = 0
        return wf

    def get_scores(self, terms):
        """ Creates a list of scores for each file in corpus
            The score = weighted frequency / the total word count in file.

            Args:
                terms (list): a list of str
            Returns:
                list: a list of tuples, each containing the file_path_name
                      and its relevancy score
        """

        scores = HashTableLinear()
        for term in terms:
            word_hash_table = self.term_freqs.get(term)
            for file in self.file_list:
                if word_hash_table.contains(file):
                    if scores.contains(file):
                        scores[file] += self.get_wf(word_hash_table[file])
                    else:
                        scores[file] = self.get_wf(word_hash_table[file])

        score_list = []
        for file in self.file_list:
            if scores.contains(file) and scores[file] > 0:
                norm_score = scores[file] / self.doc_length[file]
                score_list.append((file, norm_score))
        return score_list

    def rank(self, scores):
        """ Ranks files in the descending order of relevancy
            Args:
                scores (list): a list of tuples: (file_path_name, score)
            Returns:
                list: a list of tuples (file_path_name, score) sorted in
                      descending order of relevancy
        """

        for pos in range(1, len(scores)):
            cur_pos = pos

            while cur_pos > 0 and scores[cur_pos - 1][1] < scores[cur_pos][1]:
                temp = scores[cur_pos - 1]
                scores[cur_pos - 1] = scores[cur_pos]
                scores[cur_pos] = temp

        # Reverse the order so its descending
        # scores.reverse()

        return scores

    def search(self, query):
        """ Search for the query terms in files
            Args:
                query (str): query input: e.g. "computer science"
            Returns:
                list: a list of tuples: (files_path_name, score) sorted in
                descending order or relevancy excluding files whose relevancy
                score is 0.
        """

        terms = self.parse_words([query])
        cleaned_terms = []
        hash_terms = HashTableLinear()
        for term in terms:
            if not hash_terms.contains(term):
                cleaned_terms.append(term)
            hash_terms.put(term, term)
        scores = self.get_scores(cleaned_terms)
        scores = self.rank(scores)

        return scores

    def print_nice_results(self, scores):
        """ Takes the output of scores method and makes the results more
            presentable to look at.
            Args:
                scores (list): list of tuples that is output from self.scores
        """
        for each in scores:
            print(each[0] + str(each[1]))

def build_stopwords(filename):
    """ Function to build hash table of stop words from a text list
        Args:
            filename (str): path of stop words file
    """

    hash_table = HashTableLinear()
    stop_words = import_stopwords(filename, hash_table)

    return stop_words

def main():
    """ Main function of the program. Allows it to be run in terminal"""
    dir_path = input('Please input the path of the directory '
                     'containing documents: ')
    stopwords = build_stopwords('stop_words.txt')
    search_engine = SearchEngine(dir_path, stopwords)
    searching = True
    while searching:
        query = input('Please input a search query. Prepend it with "s:" '
                      'Input ":q" to quit:')
        if query[0:2] == ':q':
            searching = False
        elif query[0:2] == 's:':
            query = query[2:]
            results = search_engine.search(query)
            search_engine.print_nice_results(results)
        else:
            print('Sorry, that was an unexpected input.')


if __name__ == '__main__':
    main()
