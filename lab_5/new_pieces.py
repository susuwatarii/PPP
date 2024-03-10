# реализация придуманных мной новых фигур для шахмат / доп задание 1 (сложность 1)
from pieces import Piece
from constants import WHITE, BLACK


# вариация пешки - слабая пешка, в отличие от пешки на первом ходу ходит только на 1 клетку вперед, а не на 2 или 1
# обозначается W или w 
class WeakPawn(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        # как выглядит на доске
        self.image = ' W ' if color == WHITE else ' w '

    def get_moves_list(self, white_locations, black_locations):
        # получить список положений, куда фигура может сходить
        moves_lst = []        
        if self.color == BLACK:
            if (self.position[0], self.position[1] + 1) not in white_locations and \
                    (self.position[0], self.position[1] + 1) not in black_locations and self.position[1] < 7:
                moves_lst.append((self.position[0], self.position[1] + 1))
                
            if (self.position[0] + 1, self.position[1] + 1) in white_locations:
                moves_lst.append((self.position[0] + 1, self.position[1] + 1))
            if (self.position[0] - 1, self.position[1] + 1) in white_locations:
                moves_lst.append((self.position[0] - 1, self.position[1] + 1))
        else:
            if (self.position[0], self.position[1] - 1) not in white_locations and \
                    (self.position[0], self.position[1] - 1) not in black_locations and self.position[1] > 0:
                moves_lst.append((self.position[0], self.position[1] - 1))
                
            if (self.position[0] + 1, self.position[1] - 1) in black_locations:
                moves_lst.append((self.position[0] + 1, self.position[1] - 1))
            if (self.position[0] - 1, self.position[1] - 1) in black_locations:
                moves_lst.append((self.position[0] - 1, self.position[1] - 1))
        return moves_lst
    
    
# вариация пешки - пешка которая и ходит наискосок, и ест тоже наискосок
# обозначается O или o
class ObliquePawn(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        # как выглядит на доске
        self.image = ' O ' if color == WHITE else ' o '

    def get_moves_list(self, white_locations, black_locations):
        # получить список положений, куда фигура может сходить
        moves_lst = []        
        if self.color == BLACK:
            if (self.position[0] + 1, self.position[1] + 1) not in white_locations and \
                    (self.position[0]+1, self.position[1]+1) not in black_locations and self.position[1] < 7 and self.position[0] < 7:
                moves_lst.append((self.position[0]+1, self.position[1] + 1))
            if (self.position[0] - 1, self.position[1] + 1) not in white_locations and \
                    (self.position[0]-1, self.position[1]+1) not in black_locations and self.position[1] < 7 and 0 < self.position[0]:
                moves_lst.append((self.position[0]-1, self.position[1] + 1))

            if (self.position[0] + 1, self.position[1] + 1) in white_locations:
                moves_lst.append((self.position[0] + 1, self.position[1] + 1))
            if (self.position[0] - 1, self.position[1] + 1) in white_locations:
                moves_lst.append((self.position[0] - 1, self.position[1] + 1))
        else:
            if (self.position[0]-1, self.position[1] - 1) not in white_locations and \
                    (self.position[0]-1, self.position[1] - 1) not in black_locations and self.position[1] > 0 and self.position[0] > 0:
                moves_lst.append((self.position[0]-1, self.position[1] - 1))
            if (self.position[0]+1, self.position[1] - 1) not in white_locations and \
                    (self.position[0]+1, self.position[1] - 1) not in black_locations and self.position[1] > 0 and self.position[0] < 7:
                moves_lst.append((self.position[0]+1, self.position[1] - 1))

            if (self.position[0] + 1, self.position[1] - 1) in black_locations:
                moves_lst.append((self.position[0] + 1, self.position[1] - 1))
            if (self.position[0] - 1, self.position[1] - 1) in black_locations:
                moves_lst.append((self.position[0] - 1, self.position[1] - 1))
        return moves_lst
    
    
# Медведь
# ходит на 1 или 2 или 3 клетки в любую сторону: прямо, назад, в сторону, по диагоналям (не может перескакивать через фигуры)
# обозначается E или e
class Bear(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        # как выглядит на доске
        self.image = ' E ' if color == WHITE else ' e '

    def get_moves_list(self, white_locations, black_locations):
        # получить список положений, куда фигура может сходить
        moves_lst = []
        if self.color == WHITE:
            friends_list = white_locations
            enemies_list = black_locations
        else:
            friends_list = black_locations
            enemies_list = white_locations
        targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1),
                  (2, 0), (2, 2), (2, -2), (-2, 0), (-2, 2), (-2, -2), (0, 2), (0, -2),
                  (3, 0), (3, 3), (3, -3), (-3, 0), (-3, 3), (-3, -3), (0, 3), (0, -3)]  # куда может сходить медведь если он точка отсчета
        for i in range(24):
            if targets[i] != (100,100):
                target = (self.position[0] + targets[i][0], self.position[1] + targets[i][1])
                if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
                    if target in enemies_list:  # фмгура может съесть только ближайшую фигуру противника по выбранной траектории
                        # фигура не может перескакивыть фигуры противника
                        if i < 16:
                            targets[i+8]=(100,100)
                        if i < 8:
                            targets[i+16] = (100,100)
                    moves_lst.append(target)
        return moves_lst
