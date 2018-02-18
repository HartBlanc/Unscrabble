# Unscrabble
***
  Automated Words with Friends and Scrabble playing program 


## Play in Facebook Messenger with Google Chrome and Selenium
___
  playInSelenium.py uses the computer vision library OpenCV to read the board and tile rack from the WordsWithFriends messenger app.
  Simply run playInSelenium.py, login to facebook messenger in the google chrome window that opens and navigate to the game   you would like to play.

![18-02-2018](https://thumbs.gfycat.com/PerkyBriskChevrotain-size_restricted.gif)

See log.txt for plans for future improvements

## Algorithm
___
  The underlying backtracking algorithm is a python implementation of ['The World's Fastset Scrabble Program - Appel and Jacobson (1988)'](http://www.gtoal.com/wordgames/jacobson+appel/aj.pdf)

  The major components of the algorithm are **Anchors** and **Cross Sets**.

#### Anchors
  The anchor of a newly place world is the left-most, newly placed tile that is adjacent to an existing tile.


  Therefore the potential anchors, i.e. the candidate places where new words could be placed, are all the tiles adjacent tiles already on the board.


#### Cross Sets
   The algorithm reduces the problem to one dimension by using Cross Sets.

  A Cross Set for a tile is the set of letters that can form a valid word when considering the letters vertically adjacent to the tile. 

  By only considering the letters in the Cross Set of each tile when forming rows horizontally we can simply consider forming horizontal words. The board can then be transposed to find the vertical words.

#### Backtracking algorithm
  Once the anchors and cross sets are known the backtracking algorithm is used to form words from the anchors.
  The algorithm extends left from the anchor considering all combinations of the rack.
  Each left part is then extended right into all possible valid words by traversing the lexicon pruned by the cross sets.


## Lexicon
___
  The Original Lexicon used is the Enhance North American Baseline Lexicon ([ENABLE](https://code.google.com/archive/p/dotnetperls-controls/downloads)) 
  The lexicon is adjusted whenever previously unencountered words are found.
  The lexicon is currently stored in a trie data structure. This means lookups are O(k) instead of O(N).
  Where N is the size of the lexicon and and k the length of the word.
