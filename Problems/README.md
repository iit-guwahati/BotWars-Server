This folder contains the problems that have been used while developing and
testing this server. 

Following are the problems present in this folder :-

sample
------

This problem is only presented to demonstrate how this folder needs to be setup
for handling any custom problem. 


dartpart
--------

Print numbers from 1 to 1000 with one number on each line but if the number is a
square, print "dart"; if it's a cube, print "part". If the number is both a
square and a cube, print "dartpart" (on one line) . This has to be done in the
minimal characters (or keystrokes) of code. The final score is given by

s = (300 - characters_of_code) / 3 [if number of characters < 300]

if the number of characters >= 300, then the score is 1.


scramble
--------

The submitted program will be given an input file in which the first line is an
integer 'n' ( < = 100). The next n lines will contain n alphabets. Consequently,
all the lines, except the first, combine to give an n x n set of tiles. The
task of your program is to find words (as given in the dictionary in
CSW12.txt [huge file, browsers may face issue in opening it; it is advised that
you directly download the file]). Your program doesn’t need to carry the
dictionary itself. You are allowed to submit only one program file. You can
assume that the dictionary can be opened using the path : “Problems/CSW12.txt”.
Here are the rules regarding creating words :-

- Starting from any character on the board, you can move up, down, left, right
or diagonally.

- Movement is valid as long as it is within the board and the movements don’t
wrap around the boards.

- Tiles can be reused within one word and over different words.

The output of the program represents each word through the ‘starting tile’
[using cartesian co-ordinate system treating the top-left tile as (0,0) and the
bottom-right tile as (n - 1,n - 1) and a sequence of movements. The sequence of
movements is described through a string of numbers. Refer to the table below to
see how the numbers represent the direction

    0 (north west)            1 (north)           2 (north east)
    3 (west)                 <current_tile>       5 (east)
    6 (south west)            7 (south)           8 (south east)

Only one word is represented on one line through the starting tile and sequence
of movements. The line should contain first have the starting tile co-ordinate
(as explained earlier), without the parenthesis followed by a space followed by
a sequence of numbers (no space or any other delimiter) describing the
movements.

SAMPLE INPUT:

3

CAT

ATE

MET

SAMPLE OUTPUT:

0,0 775

0,0 75

0,0 57

Scores will be provided for every correct word (incorrect words are ignored)
Every path is treated differently, hence two paths giving the same word would
be considered as two different words (and rewarded accordingly). Scores for a
word is the sum of the scores of the characters. Score for the characters is
given as :

 1 point: E, A, I, O, N, R, T, L, S, U

 2 points: D, G

 3 points: B, C, M, P

 4 points: F, H, V, W, Y

 5 points: K

 8 points: J, X
 
The distribution of the characters is inversely associated to the scores.
