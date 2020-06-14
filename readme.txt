This project is a basic implementation of a search engine using hash tables. The program
is a search engine for documents, which first indexes all txt files in a specified directory,
then returns the files most relevant to a specified query.

This implementation is quite limited in functionality. The engine does not account for
synonyms or misspelled words. Additionally, it cannot output a relevant section of
a document that is quite long, only that the document contains words relevant to the query.

To use the program, run the project4 file in a Python3 interpreter. The program will first
ask you to specify a directory to be searched. After you enter the path of the directory,
you can search for a query by typing 's:' followed by your query terms. To stop searching
and quit the program, type ':q' at any time.
