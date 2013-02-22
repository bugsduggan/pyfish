pyfish
======

A very simple CLI interface for working with UCI chess engines

commands
========

just run .pyfish --help for a summary of the commands available

making it work
==============

You'll need some kind of UCI chess engine. I've been testing this with Stockfish (and that's
what it expects as a default) but it **should** work with any UCI compatible engine.

You'll probably also want some kind of opening book (in polyglot .bin format). Use some
google-fu to find one you like

todo
====

The engine currently just plays with default settings for everything apart from the opening
book. It would be nice to be able to tune the difficulty.
