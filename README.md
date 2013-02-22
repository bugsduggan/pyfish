#Pyfish

A very simple CLI interface for working with UCI chess engines.

##Commands

Just run `.pyfish.py --help` for a summary of the commands available.

Essentially, if you give it a list of moves (like `e2e4 e7e5...`) it will find you the
best next move.

If you run it with the `-i` or `--interactive` flag, you can play a game against the computer.
(specifying 'w' or 'b' after the flag will allow you to play as that colour. The default
is to play as white)

##Making it work

You'll need some kind of UCI chess engine. I've been testing this with Stockfish (and that's
what it expects as a default) but it **should** work with any UCI compatible engine.

You'll probably also want some kind of opening book (in polyglot .bin format). Use some
google-fu to find one you like

##Todo

The engine currently just plays with default settings for everything apart from the opening
book. It would be nice to be able to tune the difficulty.

It would also be nice if there were **any** error handling at all.
