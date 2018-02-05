# Unscrabble
Automated Words with Friends and Scrabble playing program 

The underlying backtracking algorithm is a python implementation of ['The World's Fastset Scrabble Program - Appel and Jacobson (1988)'](http://www.gtoal.com/wordgames/jacobson+appel/aj.pdf)


The Original Lexicon used is the Enhance North American Baseline Lexicon ([ENABLE](https://code.google.com/archive/p/dotnetperls-controls/downloads)) 
The lexicon is adjusted whenever previously unencountered words are found.
The lexicon is currently stored in a trie data structure. This means lookups are O(k) instead of O(N).
Where N is the size of the lexicon and and k the length of the word.

See the log for plans for future improvements
