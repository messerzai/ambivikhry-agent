"""Ambivikhry Chess: compact UCI chess engine using python-chess.

Search: iterative deepening alpha-beta, transposition table, quiescence,
MVV-LVA move ordering, killer moves and history heuristic.
"""
from __future__ import annotations

import time
from dataclasses import dataclass

import chess

INF = 100_000
MATE = 90_000
PIECE = {
    chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
    chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 0,
}
PST = {
    chess.PAWN: [0, 5, 5, 0, 5, 10, 20, 0],
    chess.KNIGHT: [-40, -20, -10, -10, -5, 0, 5, 5],
    chess.BISHOP: [-20, -10, -10, -5, 0, 5, 5, 5],
    chess.ROOK: [0, 0, 5, 10, 10, 5, 0, 0],
    chess.QUEEN: [-10, -5, 0, 0, 5, 5, 0, -10],
    chess.KING: [-30, -20, -20, -10, 0, 10, 20, 30],
}


@dataclass
class TTEntry:
    depth: int
    score: int
    flag: int  # 0 exact, 1 lower bound, 2 upper bound
    move: chess.Move | None


class Engine:
    def __init__(self, max_depth: int = 5, time_limit: float = 2.0):
        self.max_depth = max_depth
        self.time_limit = time_limit
        self.tt: dict[object, TTEntry] = {}
        self.history: dict[tuple[bool, int, int], int] = {}
        self.killers: dict[int, tuple[chess.Move, ...]] = {}
        self.nodes = 0
        self.stop = False
        self.deadline = 0.0
        self._ply = 0

    def evaluate(self, board: chess.Board) -> int:
        """Static evaluation, positive from White's point of view."""
        if board.is_checkmate():
            return -MATE if board.turn else MATE
        if board.is_stalemate() or board.is_insufficient_material():
            return 0

        score = 0
        for color in (chess.WHITE, chess.BLACK):
            sign = 1 if color else -1
            for piece_type, value in PIECE.items():
                score += sign * value * len(board.pieces(piece_type, color))
                table = PST[piece_type]
                for square in board.pieces(piece_type, color):
                    rank = chess.square_rank(square)
                    relative_rank = rank if color else 7 - rank
                    score += sign * table[min(relative_rank, 7)]

        mobility = len(list(board.legal_moves))
        score += mobility * (2 if board.turn else -2)
        return score

    def _order(self, board: chess.Board, moves, tt_move=None):
        def key(move):
            if move == tt_move:
                return 1_000_000
            capture = board.is_capture(move)
            victim = board.piece_at(move.to_square)
            attacker = board.piece_at(move.from_square)
            see = 0
            if capture and attacker:
                see = (PIECE.get(victim.piece_type, 0) if victim else 100) - PIECE[attacker.piece_type]
            killers = self.killers.get(self._ply, ())
            return (
                (9000 if capture else 0)
                + see
                + (8000 if move in killers else 0)
                + self.history.get((board.turn, move.from_square, move.to_square), 0)
            )

        return sorted(moves, key=key, reverse=True)

    def _check_time(self):
        if time.monotonic() >= self.deadline:
            self.stop = True

    def qsearch(self, board: chess.Board, alpha: int, beta: int) -> int:
        self.nodes += 1
        if self.nodes & 2047 == 0:
            self._check_time()

        stand_pat = self.evaluate(board)
        if stand_pat >= beta:
            return beta
        alpha = max(alpha, stand_pat)

        moves = [m for m in board.legal_moves if board.is_capture(m) or board.gives_check(m)]
        for move in self._order(board, moves):
            board.push(move)
            score = -self.qsearch(board, -beta, -alpha)
            board.pop()
            if self.stop:
                break
            if score >= beta:
                return beta
            alpha = max(alpha, score)
        return alpha

    def search(self, board: chess.Board, depth: int, alpha: int, beta: int, ply: int = 0) -> int:
        self._ply = ply
        self.nodes += 1
        if self.nodes & 2047 == 0:
            self._check_time()
        if self.stop:
            return 0
        if board.is_checkmate():
            return -MATE + ply
        if board.is_stalemate():
            return 0
        if depth <= 0:
            return self.qsearch(board, alpha, beta)

        key = board._transposition_key()
        entry = self.tt.get(key)
        if entry and entry.depth >= depth:
            if entry.flag == 0:
                return entry.score
            if entry.flag == 1:
                alpha = max(alpha, entry.score)
            elif entry.flag == 2:
                beta = min(beta, entry.score)
            if alpha >= beta:
                return entry.score

        original_alpha = alpha
        best = -INF
        best_move = None
        tt_move = entry.move if entry else None
        for move in self._order(board, list(board.legal_moves), tt_move):
            board.push(move)
            score = -self.search(board, depth - 1, -beta, -alpha, ply + 1)
            board.pop()
            if self.stop:
                return 0
            if score > best:
                best, best_move = score, move
            if score > alpha:
                alpha = score
                if not board.is_capture(move):
                    key_h = (board.turn, move.from_square, move.to_square)
                    self.history[key_h] = self.history.get(key_h, 0) + depth * depth
            if alpha >= beta:
                if not board.is_capture(move):
                    old = self.killers.get(ply, ())
                    self.killers[ply] = (move,) + tuple(m for m in old if m != move)[:1]
                break

        flag = 0 if original_alpha < best < beta else (1 if best <= original_alpha else 2)
        self.tt[key] = TTEntry(depth, best, flag, best_move)
        return best

    def best_move(self, board: chess.Board) -> chess.Move | None:
        self.deadline = time.monotonic() + self.time_limit
        self.stop = False
        self.nodes = 0
        best = next(iter(board.legal_moves), None)

        for depth in range(1, self.max_depth + 1):
            self.stop = False
            score = -INF
            candidate = None
            for move in self._order(board, list(board.legal_moves)):
                board.push(move)
                current = -self.search(board, depth - 1, -INF, INF, 1)
                board.pop()
                if self.stop:
                    break
                if current > score:
                    score, candidate = current, move
            if not self.stop and candidate:
                best = candidate
            if self.stop:
                break
        return best


def uci() -> None:
    engine = Engine()
    board = chess.Board()
    while True:
        line = input().strip()
        if not line:
            continue
        parts = line.split()
        command = parts[0]

        if command == "uci":
            print("id name Ambivikhry-Chess 0.1")
            print("id author Ambivikhry")
            print("uciok", flush=True)
        elif command == "isready":
            print("readyok", flush=True)
        elif command == "ucinewgame":
            engine = Engine()
            board = chess.Board()
        elif command == "position":
            i = 1
            if i < len(parts) and parts[i] == "startpos":
                board = chess.Board()
                i += 1
            elif i < len(parts) and parts[i] == "fen":
                board = chess.Board(" ".join(parts[i + 1:i + 7]))
                i += 7
            if i < len(parts) and parts[i] == "moves":
                for uci_move in parts[i + 1:]:
                    board.push_uci(uci_move)
        elif command == "go":
            if "depth" in parts:
                engine.max_depth = int(parts[parts.index("depth") + 1])
            if "movetime" in parts:
                engine.time_limit = int(parts[parts.index("movetime") + 1]) / 1000.0
            move = engine.best_move(board)
            if move:
                print("bestmove", move.uci(), flush=True)
        elif command == "quit":
            break
        elif command == "stop":
            engine.stop = True


if __name__ == "__main__":
    uci()
