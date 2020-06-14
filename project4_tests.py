""" Function Tests for Project 4
    Course: CPE202
    Quarter: Spring 2020
    Author: Chris Linthacum
"""

import unittest as ut

from hashtables import import_stopwords, HashTableLinear
from project4 import SearchEngine, build_stopwords

FILE = "stop_words.txt"

class HashTableLinearTests(ut.TestCase):
    """ Tests for Separate Chain Hash Table"""

    def test_basic(self):
        """ Tests basic functionality"""

        hash_table = HashTableLinear()
        hash_table.put('unless', 'unless')
        self.assertTrue(hash_table.contains('unless'))
        hash_table.put('every', 'every')
        hash_table.put('being', 'being')
        hash_table.put('elsewhere', 'elsewhere')
        hash_table.put('nothing', 'nothing')
        hash_table.put('hereby', 'hereby')
        hash_table.put('latter', 'latter')
        hash_table.put('and', 'and')
        hash_table.put('afterwards', 'afterwards')
        hash_table.put('say', 'say')
        hash_table.put('very', 'very')
        hash_table.put('few', 'few')
        hash_table.put('well', 'well')
        hash_table.put('various', 'various')
        hash_table.put('make', 'make')
        hash_table.put('regarding', 'regarding')
        hash_table.put('take', 'take')
        hash_table.put('give', 'give')
        hash_table.put('whole', 'whole')
        hash_table.put('i', 'i')
        hash_table.put('against', 'against')
        hash_table.put('can', 'can')

        hash_table.get('every')
        hash_table.get('being')
        hash_table.get('elsewhere')
        hash_table.get('nothing')
        hash_table.get('hereby')
        hash_table.get('latter')
        hash_table.get('and')
        hash_table.get('afterwards')
        hash_table.get('say')
        hash_table.get('very')
        hash_table.get('few')
        hash_table.get('well')
        hash_table.get('various')
        hash_table.get('make')
        hash_table.get('regarding')
        hash_table.get('take')
        hash_table.get('give')
        hash_table.get('whole')
        hash_table.get('i')
        hash_table.get('against')
        hash_table.get('can')

    def test_whole_functionality(self):
        """ Tests the Separate Chain Hash Table Functionality"""

        filename = 'stop_words.txt'
        hash_table = HashTableLinear()

        hash_table = import_stopwords(filename, hash_table)

        self.assertRaises(KeyError, hash_table.get, 'BubbleGum')
        self.assertTrue('to' in hash_table)

        second_hash = HashTableLinear()
        second_hash.put('three', 'three')
        third_hash = HashTableLinear()
        third_hash.put('three', 'three')
        self.assertEqual(second_hash, third_hash)
        self.assertNotEqual(hash_table, second_hash)
        self.assertNotEqual(hash_table, 5)
        expected = "Hash_val = 0: None\n" \
            "Hash_val = 1: None\n" \
            "Hash_val = 2: None\n" \
            "Hash_val = 3: None\n" \
            "Hash_val = 4: ('three', 'three')\n" \
            "Hash_val = 5: None\n" \
            "Hash_val = 6: None\n" \
            "Hash_val = 7: None\n" \
            "Hash_val = 8: None\n" \
            "Hash_val = 9: None\n" \
            "Hash_val = 10: None\n"

        self.assertEqual(expected, repr(second_hash))

        second_hash['four'] = 'four'
        self.assertEqual(second_hash['four'], 'four')
        second_hash['five'] = 'five'
        self.assertEqual(0, hash_table.get('from'))

        self.assertFalse(second_hash.contains('p'))
        self.assertTrue(second_hash.contains('five'))
        second_hash.remove('five')
        self.assertFalse(second_hash.contains('five'))
        self.assertRaises(KeyError, second_hash.remove, 'p')

        self.assertEqual(1, third_hash.size())

        self.assertEqual(0, third_hash.collisions())

class SearchEngineTests(ut.TestCase):
    """ unittests for the SearchEngine class methods"""

    # def test_read_file(self):
    #     """ Tests read_file of taking a file and reading to list of strings"""
    #     infile = 'test_file.txt'
    #     temp = SearchEngine(None, None)
    #     output = temp.read_file(infile)
    #     expected_out = ['Line 1', 'Line 2', 'Line 3', 'Line 4']
    #
    #     self.assertEqual(expected_out, output)

    # def test_parse_words(self):
    #     """ Tests the parse_words method and helper exclude_stopwords"""
    #
    #     filename = 'parse_text_test.txt'
    #     stopwords = build_stopwords('stop_words.txt')
    #     temp = SearchEngine(None, stopwords)
    #     lines = temp.read_file(filename)
    #     print(lines)
    #     lines = temp.parse_words(lines)
    #     exclude_words = ['The', 'over', 'the', 'This', 'is', 'on', 'an']
    #     for each in exclude_words:
    #         self.assertTrue(each not in lines)

    def test_build_stopwords(self):
        """ Tests the build_stopwords function"""
        filename = 'stop_words.txt'
        stop_words = build_stopwords(filename)
        self.assertTrue("on" in stop_words)

    # Need tests for count_words,

    def test_full_functionality(self):
        """ Tests a basic run through the SE process"""

        stopwords = build_stopwords('stop_words.txt')

        search_engine = SearchEngine('test_dir', stopwords)

        self.assertTrue(search_engine.term_freqs.contains('alphabet'))
        self.assertFalse(search_engine.term_freqs.contains('exclamation'))
        self.assertTrue(search_engine.term_freqs.contains('engine'))
        self.assertTrue(search_engine.term_freqs.contains('second'))

        reference_engine = SearchEngine('ref_dir', stopwords)

        self.assertNotEqual(search_engine, 8)
        self.assertNotEqual(search_engine, reference_engine)

        print(reference_engine)

        reference = "SearchEngine Instance:\n" \
                    "Hash_val = 0: None\n" \
                    "Hash_val = 1: None\n" \
                    "Hash_val = 2: None\n" \
                    "Hash_val = 3: None\n" \
                    "Hash_val = 4: None\n" \
                    "Hash_val = 5: None\n" \
                    "Hash_val = 6: None\n" \
                    "Hash_val = 7: None\n" \
                    "Hash_val = 8: None\n" \
                    "Hash_val = 9: None\n" \
                    "Hash_val = 10: None\n"

        self.assertEqual(reference, repr(reference_engine))

        # print(search_engine.get_scores(['google']))

        query = 's:google'
        query = query[2:]
        results = search_engine.search(query)
        print(results)

    def test_provided_docs(self):
        """ Tests of a run through the provided docs folder"""

        stopwords = build_stopwords('stop_words.txt')

        search_engine = SearchEngine('docs', stopwords)
        # print(search_engine.get_scores(['computer', 'science']))
        # x = search_engine.get_scores(['computer', 'science'])
        # print(x)


if __name__ == '__main__':
    ut.main()
