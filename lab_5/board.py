import numpy as np
from constants import WHITE, BLACK  # такой вариант позволяет потом подключать файлик с 'константами' к другим файликам, 
                                    # что упрощает работу и делает ее более безопасной
from pieces import Rook, Knight, Bishop, Queen, King, Pawn


# Доска для шахмат
class Board(object):
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
                                    Pawn(WHITE, 0, 6),
                                    Pawn(WHITE, 1, 6),
                                    Pawn(WHITE, 2, 6),
                                    Pawn(WHITE, 3, 6),
                                    Pawn(WHITE, 4, 6),
                                    Pawn(WHITE, 5, 6),
                                    Pawn(WHITE, 6, 6),
                                    Pawn(WHITE, 7, 6)
                                    
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
                                    Pawn(BLACK, 0, 1),
                                    Pawn(BLACK, 1, 1),
                                    Pawn(BLACK, 2, 1),
                                    Pawn(BLACK, 3, 1),
                                    Pawn(BLACK, 4, 1),
                                    Pawn(BLACK, 5, 1),
                                    Pawn(BLACK, 6, 1),
                                    Pawn(BLACK, 7, 1)
                                    
                                ]
        
    def get_piece(self, coords, color):  
        # получить объект по координатам
        if color == WHITE:
            for p in self.white_pieces_list:  
                if p.position == coords:
                    return p
        else:
            for p in self.black_pieces_list:
                if p.position == coords:
                    return p
    
    def get_white_locations(self):  
        # получить список положений белых фигур
        return [piece.position for piece in self.white_pieces_list]
    
    def get_black_locations(self):
        # получить список положений черных фигур
        return [piece.position for piece in self.black_pieces_list]
            
    def to_int_coords(self, xy: str):
        # перевод координаты из вида 'буквачисло' в (int, int) с проверкой на корректность данных 
        try:
            int_y = 8 - int(xy[1])
        except:
            return        
        if len(xy) != 2 or int_y < 0 or int_y > 7 or xy[0].lower() > 'h' or xy[0].lower() < 'a':
            return
        return (int(hex(ord(xy[0]))[-1])-1, 8-int(xy[1]))  # букву переводим в ascii в шестнадцатеричный вариант
        
            
    def move_piece(self, from_coords, to_coords):
        # сделать ход, записать в историю (если фигура съедена, то удалить ее), кол-во ходов в партии +1
        # ход получилось сделать - True, нельзя сделать такой ход - False
        if self.turn == WHITE:  # если сейчас ход белых
            wh_p = self.get_piece(from_coords, WHITE)  
            if wh_p:  # если выбранная фигура существует
                if wh_p.move(to_coords[0], to_coords[1], (self.get_white_locations(), self.get_black_locations())):  # если правильный ход
                    self.history.append([wh_p.image, from_coords, to_coords])  
                    bl_p = self.get_piece(to_coords, BLACK) 
                    if bl_p:  # если нужно было съесть черную фигуру
                        self.black_pieces_list.remove(bl_p)
                        self.history[-1].append(bl_p.image)
                    else:
                        self.history[-1].append('')
                    # передаем ход черным, кол-во ходов в партии +1
                    self.turn = BLACK
                    self.count += 1
                    return True

        else:  # если сейчас ход черных (аналогично белым)
            bl_p = self.get_piece(from_coords, BLACK)
            if bl_p:
                if bl_p.move(to_coords[0], to_coords[1], (self.get_white_locations(),self.get_black_locations())):
                    self.history.append([bl_p.image, from_coords, to_coords])
                    wh_p = self.get_piece(to_coords, WHITE)
                    if wh_p:
                        self.white_pieces_list.remove(wh_p)
                        self.history[-1].append(wh_p.image)
                    else:
                        self.history[-1].append('')

                    self.turn = WHITE
                    self.count += 1
                    return True
                
        return False
    
    
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
        
    
    def moves_back(self, n_moves: int):
        # откат хода или ходов
        if len(self.history) < n_moves:  # если указано слищком большое число ходов для отката, откат до состояния начала игры
            n_moves = len(self.history)
        
        for i in range(n_moves):  # для каждого из n_moves последних ходов
            h_move = self.history[-i-1]
            if self.turn == WHITE:
                self.get_piece(h_move[2], BLACK).position = h_move[1]  # изменяем координаты фигуры, которая сделала ход последней
                if h_move[3]:
                    new_piece = self.create_piece(h_move[3], h_move[2])  #  восстанавливаем съеденную фигуру
                    self.white_pieces_list.append(new_piece)  # добавляем восстановленную фигуру в список существующих соотв. цвета
                self.turn = BLACK  # переопределяем чей ход
                self.count -= 1  # изменяем количество ходов в партии
            else:
                self.get_piece(h_move[2], WHITE).position = h_move[1]
                if h_move[3]:
                    new_piece = self.create_piece(h_move[3], h_move[2])
                    self.black_pieces_list.append(new_piece)
                self.turn = WHITE
                self.count -= 1
        self.history = self.history[:-n_moves]  # изменяем историю

        
    def is_in_danger(self):
        # возвращает список координат фигур ходящего игрока, которые находятся в опасности 
        options_list = []  # куда могут сходить все фигуры противника
        if self.turn == BLACK:
            # ходят черные, угроза от белых
            for p in self.white_pieces_list:
                options_list.append(p.get_moves_list(self.get_white_locations(), self.get_black_locations()))
            p_list = self.get_black_locations()
        else:
            # ходят белые, угроза от черных
            for p in self.black_pieces_list:
                options_list.append(p.get_moves_list(self.get_white_locations(), self.get_black_locations()))
            p_list = self.get_white_locations()
        
        in_danger_list = []
        # проверка, попадает ли фигура в хотя бы какой-то из списков возможных ходов фигур противника
        for i in range(len(p_list)):
            for option in options_list:
                if p_list[i] in option:
                    in_danger_list.append(p_list[i])
        return in_danger_list

    def print_board(self, in_danger=False, coords=None): 
        # распечатать доску, флаги:
        # in_danger - нужно показать фигуры под ударом, 
        #  coords - для фигуры с данными координатами, показать куда можно сходить                            
        d_board = np.full((12, 12), '   ')
        # расставляем на доску буквы, цифры, границы 
        numbers = np.array([' 8 ',' 7 ',' 6 ',' 5 ',' 4 ',' 3 ',' 2 ',' 1 '])
        chars = np.array([' A ',' B ',' C ',' D ',' E ',' F ',' G ',' H '])
        d_board[2:-2, 0] = numbers
        d_board[2:-2, -1] = numbers
        d_board[2:-2, 1] = [' | ']
        d_board[2:-2, -2] = [' | ']
        d_board[0, 2:-2] = chars
        d_board[-1, 2:-2] = chars
        d_board[1, 2:-2] = ['---']
        d_board[-2, 2:-2] = ['---']
        d_board[2:-2, 2:-2] = ' - '
         
        # добавляем на доску фигуры и печатаем
        for p in self.white_pieces_list + self.black_pieces_list:
            d_board[(p.position[1]+2, p.position[0]+2)] = p.image
            
        # указываем возможные ходы для выбранной фигуры 
        if coords:
            moves_lst = self.get_piece(coords, self.turn).get_moves_list(self.get_white_locations(), self.get_black_locations())
            for pos in moves_lst:
                y, x = pos
                d_board[x+2, y+2] = f':{d_board[x+2, y+2][1]}:'
                
        # указываем фигуры под боем
        if in_danger:
            in_danger_lst = self.is_in_danger()
            for pos in in_danger_lst:
                y, x = pos
                d_board[x+2, y+2] = f'!{d_board[x+2, y+2][1]}!'
        
        # печатаем доску 
        print()
        for row in d_board:
            print(''.join(row))
        print()
    
    def play(self):
        # игра (меню действий и общение с пользователем)
        self.print_board()
        print(f'-- {self.turn} --')
        menue = '0. закончить игру\n1. сделать ход\n2. куда можно сходить фигурой\n3. мои фигуры под ударом\n4. откат хода/ходов\n? : '
        choice = input(menue)
        while choice != '0':
            match choice:
                case '1':  # делаем ход, неправильные координаты -> обратно в меню
                    #self.print_board()
                    print(f'-- ход № {self.count+1} --')
                    from_coords = self.to_int_coords(input('выберите фигуру  : '))
                    to_coords = self.to_int_coords(input('куда переместить : '))
                    if not(from_coords and to_coords and self.move_piece(from_coords, to_coords)):
                        print('\n ~ неправильные координаты ! ~ ')
                    self.print_board()

                case '2':  # возможные ходы выбранной фигуры
                    f_coords = self.to_int_coords(input('выберите фигуру  : '))
                    if f_coords:
                        self.print_board(coords=f_coords)
                    else:
                        print('\n ~ неправильные координаты ! ~ ')
                        self.print_board()
                        
                case '3':  # фигуры под ударом
                    self.print_board(in_danger=True)
                case '4':  # откат хода/ходов
                    try:
                        self.moves_back(int(input('сколько ходов? ')))                        
                    except:
                        print('\n ~ не получилось сделать откат ходов! ~ ')
                    self.print_board()
                    
            print(f'-- {self.turn} --')
            choice = input(menue)
            
        # заканчиваем игру
        choice_2 = input('\n1) сдаться\n2) ничья\n? ')
        if choice_2 == '2':  # если выбрали ничью
            print(f'----------------------------\n  ничья !')
        else:  # если выбрали сдаться или несуществующий вариант
            if self.turn != WHITE:
                print(f'----------------------------\n  белые выиграли !')
            else:
                print(f'----------------------------\n  черные выиграли !')