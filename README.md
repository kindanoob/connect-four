# pyconnect_four
Python implementation of the Connect four game using Pygame

Program was tested on Ubuntu 16.04 LTS Xenial, Python 3.10.12, Pygame 2.6.0

Requirements:
1) Python 3.10.12
2) Pygame 2.6.0

Instructions:
1) Run main.py script to lauch the application (`python3 main.py`).
2) The goal of the game is to form a horizontal, vertical of diagonal line of four discs of your color. Note than if you form more than four discs in a line, then you still win because the line of more than four discs contains a line of exactly four discs.
3) Choose who moves first by mouse left click on Player or Computer. First player plays red discs and second player plays yellow discs.
4) Make moves by left click on the digit located in the top row. If you click on the digit i and i_th column is not full, then  disc of your color will be placed in the bottommost vacant position of column i. If the corresponding column is full, the move is not made and you need to choose a valid column.

If you want to learn more about Connect four game please refer to the following wikipedia article: https://en.wikipedia.org/wiki/Connect_Four

The project is still in the development stage and there are many things yet to be implemented.
