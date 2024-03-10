from board import Board
from pieces import Rook, Knight, Bishop, Queen, King, Pawn
from new_pieces import ObliquePawn, WeakPawn, Bear
from constants import WHITE, BLACK


# наследуем от Board
class NewBoard(Board):
    # все методы такие же как у Board, но при создании доски вместо создания нескольких пешек создаются придуманные фигуры
    
    def __init__(self):
        # номер хода
        self.count = 0
        # запись истории партии
        self.history = list()  # фигура / начальные координаты / куда переместилась | съеденная фигура
        # чей сейчас ход
        self.turn = WHITE  # WHITE или BLACK
        
        # белые фигуры     
        self.white_pieces_list = [
                                    Rook(WHITE,   0, 7),
                                    Knight(WHITE, 1, 7),
                                    Bishop(WHITE, 2, 7),
                                    Queen(WHITE,  3, 7),
                                    King(WHITE,   4, 7),
                                    Bishop(WHITE, 5, 7),
                                    Knight(WHITE, 6, 7),
                                    Rook(WHITE,   7, 7),
                                    WeakPawn(WHITE, 0, 6),
                                    Pawn(WHITE, 1, 6),
                                    Pawn(WHITE, 2, 6),
                                    ObliquePawn(WHITE, 3, 6),
                                    Bear(WHITE, 4, 6),
                                    Pawn(WHITE, 5, 6),
                                    Pawn(WHITE, 6, 6),
                                    WeakPawn(WHITE, 7, 6)
                                    
                                ]
        # черные фигуры 
        self.black_pieces_list = [
                                    Rook(BLACK,   0, 0),
                                    Knight(BLACK, 1, 0),
                                    Bishop(BLACK, 2, 0),
                                    Queen(BLACK,  3, 0),
                                    King(BLACK,   4, 0),
                                    Bishop(BLACK, 5, 0),
                                    Knight(BLACK, 6, 0),
                                    Rook(BLACK,   7, 0),
                                    WeakPawn(BLACK, 0, 1),
                                    Pawn(BLACK, 1, 1),
                                    Pawn(BLACK, 2, 1),
                                    ObliquePawn(BLACK, 3, 1),
                                    Bear(BLACK, 4, 1),
                                    Pawn(BLACK, 5, 1),
                                    Pawn(BLACK, 6, 1),
                                    WeakPawn(BLACK, 7, 1)
                                ]
    def create_piece(self, img, pos):
        # создаем и возвращаем фигуру на основе ее image и координат
        if img.islower():
            color = BLACK
        else:
            color = WHITE
        match img.lower():
            case ' r ':
                return Rook(color, pos[0], pos[1])
            case ' k ':
                return King(color, pos[0], pos[1])
            case ' q ':
                return Queen(color, pos[0], pos[1])
            case ' p ':
                return Pawn(color, pos[0], pos[1])
            case ' b ':
                return Bishop(color, pos[0], pos[1])
            case ' n ':
                return Knight(color, pos[0], pos[1])
            case ' e ':
                return Bear(color, pos[0], pos[1])
            case ' o ':
                return ObliquePawn(color, pos[0], pos[1])
            case ' w ':
                return WeakPawn(color, pos[0], pos[1])
            