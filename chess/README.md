# Ambivikhry Chess

A compact UCI-compatible chess engine generated as an Ambivikhry engineering experiment.

## Design

- iterative-deepening alpha-beta search
- quiescence search
- transposition table
- capture / TT / killer / history move ordering
- material + lightweight piece-square evaluation
- UCI protocol for Lichess, Cute Chess, BanksiaGUI and other UCI clients

This is a research engine, not a Stockfish replacement. Its purpose is to provide a clean base for later Ambivikhry evolution: stronger evaluation, NNUE-style features, self-play benchmarks and tournament integration.

## Run

```bash
cd chess
python -m pip install -r requirements.txt
python ambivikhry_chess.py
```

Then send standard UCI commands, for example:

```text
uci
isready
position startpos moves e2e4 e7e5
go depth 4
quit
```

## Ambivikhry evolution path

The engine can evolve through measured experiments rather than unrestricted self-modification: every improvement should have a reproducible code change, benchmark and regression test before promotion.
