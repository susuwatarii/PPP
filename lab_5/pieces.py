from abc import ABC, abstractmethod
from constants import WHITE, BLACK  # такой вариант позволяет потом подключать файлик с 'константами' к другим файликам, 
                                    # что упрощает работу и делает ее более безопасной

# Фигура (родительский класс)
class Piece(ABC):
    def __init__(self, color, x, y):
        # двигалась ли уже фигура
        self.first_move = True
        # цвет фигуры
        self.color = color
        # позиция на доске
        self.position = (x, y)

    @abstractmethod
    def get_moves_list(self, white_locations, black_locations):  # иммитация виртуального метода
        # получить список положений, куда фигура может сходить
        pass

    def check_coords(self, to_x, to_y, locations):
        # проверить корректность координат для перемещения фигуры
        moves_lst = self.get_moves_list(locations[0], locations[1])
        if moves_lst and (to_x, to_y) in moves_lst:
            return True
        return False

    def move(self, to_x, to_y, locations):
        # перемещение, смена координат
        if self.check_coords(to_x, to_y, locations):
            self.position = (to_x, to_y)
            self.first_move = False
            return True
        else:
            return False
        

# Пешка
class Pawn(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        # как выглядит на доске
        self.image = ' P ' if color == WHITE else ' p '

    def get_moves_list(self, white_locations, black_locations):
        # получить список положений, куда фигура может сходить
        moves_lst = []        
        if self.color == BLACK:
            if (self.position[0], self.position[1] + 1) not in white_locations and \
                    (self.position[0], self.position[1] + 1) not in black_locations and self.position[1] < 7:#<7
                moves_lst.append((self.position[0], self.position[1] + 1))
            if (self.position[0], self.position[1] + 2) not in white_locations and \
                    (self.position[0], self.position[1] + 2) not in black_locations and self.first_move: #self.position[1] == 1:
                moves_lst.append((self.position[0], self.position[1] + 2))
            if (self.position[0] + 1, self.position[1] + 1) in white_locations:
                moves_lst.append((self.position[0] + 1, self.position[1] + 1))
            if (self.position[0] - 1, self.position[1] + 1) in white_locations:
                moves_lst.append((self.position[0] - 1, self.position[1] + 1))
        else:
            if (self.position[0], self.position[1] - 1) not in white_locations and \
                    (self.position[0], self.position[1] - 1) not in black_locations and self.position[1] > 0: # >0
                moves_lst.append((self.position[0], self.position[1] - 1))
            if (self.position[0], self.position[1] - 2) not in white_locations and \
                    (self.position[0], self.position[1] - 2) not in black_locations and self.first_move: 
                moves_lst.append((self.position[0], self.position[1] - 2))
            if (self.position[0] + 1, self.position[1] - 1) in black_locations:
                moves_lst.append((self.position[0] + 1, self.position[1] - 1))
            if (self.position[0] - 1, self.position[1] - 1) in black_locations:
                moves_lst.append((self.position[0] - 1, self.position[1] - 1))
        return moves_lst
    

# Король 
class King(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        # как выглядит на доске
        self.image = ' K ' if color == WHITE else ' k '

    def get_moves_list(self, white_locations, black_locations):
        # получить список положений, куда фигура может сходить
        moves_lst = []
        if self.color == WHITE:
            friends_list = white_locations
        else:
            friends_list = black_locations
        targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]  # куда может сходить король если он точка отсчета
        for i in range(8):
            target = (self.position[0] + targets[i][0], self.position[1] + targets[i][1])
            if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
                moves_lst.append(target)
        return moves_lst

    
# Конь
class Knight(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        # как выглядит на доске
        self.image = ' N ' if color == WHITE else ' n '

    def get_moves_list(self, white_locations, black_locations):
        # получить список положений, куда фигура может сходить
        moves_list = []
        if self.color == WHITE:
            friends_list = white_locations
        else:
            friends_list = black_locations
        targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
        for i in range(8):
            target = (self.position[0] + targets[i][0], self.position[1] + targets[i][1])
            if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
                moves_list.append(target)
        return moves_list
    

# Ферзь
class Queen(Piece):  
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        # как выглядит на доске
        self.image = ' Q ' if color == WHITE else ' q '

    def get_moves_list(self, white_locations, black_locations):
        # получить список положений, куда фигура может сходить
        # Bishop.get_moves_list + Rook.get_moves_list
        moves_list = []
        if self.color == WHITE:
            enemies_list = black_locations
            friends_list = white_locations
        else:
            friends_list = black_locations
            enemies_list = white_locations

        targets = [(1, -1), (-1, -1), (1, 1), (-1, 1), (0, 1), (0, -1), (1, 0), (-1, 0)]
        for target in targets:
            path = True
            chain = 1
            x, y = target
            while path:
                if ( self.position[0] + (chain * x),  self.position[1] + (chain * y)) not in friends_list and \
                        0 <=  self.position[0] + (chain * x) <= 7 and 0 <=  self.position[1] + (chain * y) <= 7:
                    moves_list.append(( self.position[0] + (chain * x),  self.position[1] + (chain * y)))
                    if ( self.position[0] + (chain * x),  self.position[1] + (chain * y)) in enemies_list:
                        path = False
                    chain += 1
                else:
                    path = False
        return moves_list
    

# Ладья
class Rook(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        # как выглядит на доске
        self.image = ' R ' if color == WHITE else ' r '

    def get_moves_list(self, white_locations, black_locations):
        # получить список положений, куда фигура может сходить
        moves_list = []
        if self.color == WHITE:
            enemies_list = black_locations
            friends_list = white_locations
        else:
            friends_list = black_locations
            enemies_list = white_locations
        targets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for target in targets:
            path = True
            chain = 1
            x, y = target
            while path:
                if (self.position[0] + (chain * x), self.position[1] + (chain * y)) not in friends_list and \
                        0 <= self.position[0] + (chain * x) <= 7 and 0 <= self.position[1] + (chain * y) <= 7:
                    moves_list.append((self.position[0] + (chain * x), self.position[1] + (chain * y)))
                    if (self.position[0] + (chain * x), self.position[1] + (chain * y)) in enemies_list:
                        path = False
                    chain += 1
                else:
                    path = False
        return moves_list
    

# Слон
class Bishop(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        # как выглядит на доске
        self.image = ' B ' if color == WHITE else ' b '

    def get_moves_list(self, white_locations, black_locations):
        # получить список положений, куда фигура может сходить
        moves_list = []
        if self.color == WHITE:
            enemies_list = black_locations
            friends_list = white_locations
        else:
            friends_list = black_locations
            enemies_list = white_locations
        targets = [(1, -1), (-1, -1), (1, 1), (-1, 1)]
        for target in targets:
            path = True
            chain = 1
            x, y = target
            while path:
                if ( self.position[0] + (chain * x),  self.position[1] + (chain * y)) not in friends_list and \
                        0 <=  self.position[0] + (chain * x) <= 7 and 0 <=  self.position[1] + (chain * y) <= 7:
                    moves_list.append(( self.position[0] + (chain * x),  self.position[1] + (chain * y)))
                    if ( self.position[0] + (chain * x),  self.position[1] + (chain * y)) in enemies_list:
                        path = False
                    chain += 1
                else:
                    path = False
        return moves_list
    
    