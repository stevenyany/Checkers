from tkinter import *

class CheckersPiece:
    '''represents a piece of Checkers'''

    def __init__(self, player, pos, is_king=False):
        '''CheckersPiece(player, pos[, is_king=False])
        creates a Checkers piece of player, in which position, if king'''
        self.player = player
        self.pos = pos
        self.is_king = is_king

    def get_player(self):
        '''CheckersPiece.get_player() -> int
        returns the player's number'''
        return self.player

    def get_position(self):
        '''CheckersPiece.get_position() -> (int, int)
        returns the position of piece'''
        return self.pos

    def get_king(self):
        '''CheckersPiece.get_king() -> bool
        returns whether or not piece is king'''
        return self.is_king

    def make_king(self):
        '''CheckersPiece.make_king()
        turns piece into a king'''
        self.is_king = True

    def change_position(self, pos):
        '''CheckersPieces.change_position(pos)
        changes position of piece to pos'''
        self.pos = pos


class CheckersBoard:
    '''represents a board of Checkers'''
    player_ids = (0, 1)
    
    def __init__(self, rows=8, columns=8):
        '''CheckersBoard([rows=8, columns=8])
        creates a CheckersBoard in starting position'''
        # create starting board
        self.pieces = []
        for row in range(rows):
            for col in range(columns):
                pos = (row, col)
                
                # find starting positions
                if row % 2 != col % 2 and row < rows//2 - 1:
                    # player 1
                    self.pieces.append(CheckersPiece(self.player_ids[1], pos))
                elif row % 2 != col % 2 and row > rows//2:
                    # player 0
                    self.pieces.append(CheckersPiece(self.player_ids[0], pos))

        # attributes
        self.rows = rows
        self.columns = columns
        self.current_player = self.player_ids[0]
        self.endgame = None

    def get_piece(self, pos):
        '''CheckersBoard.get_piece(pos) -> int
        returns the piece at position'''
        for p in self.pieces:
            if p.get_position() == pos:
                return p

        return None

    def remove_piece(self, piece):
        '''CheckersBoard.remove_piece(piece)
        removes piece from board'''
        self.pieces.remove(piece)

    def get_all_pieces_positions(self, player=None):
        '''CheckersBoard.get_all_pieces_positions([players=None]) -> list
        None returns all piece positions
        otherwise returns only player piece positions'''
        positions = []
        for p in self.pieces:
            if player is None:
                positions.append(p.get_position())
            elif p.get_player() == player:
                positions.append(p.get_position())

        return positions
    
    def get_all_pieces(self):
        '''CheckersBoard.get_all_pieces() -> list
        returns all the pieces on board'''
        return self.pieces

    def get_player(self):
        '''CheckersBoard.get_player() -> int
        returns the current player'''
        return self.current_player

    def next_player(self):
        '''CheckersBoard.next_player()
        goes to the next player'''
        self.current_player = self.player_ids[1-self.current_player]

    def get_endgame(self):
        '''CheckersBoard.get_endgame() -> None or int
        returns endgame state'''
        return self.endgame

    def is_movable(self, piece):
        '''CheckersBoard.is_movable(piece) -> dict
        returns a dict of the possible positions where piece can jump'''
        if piece.get_player() != self.current_player:
            return None

        (row, col) = piece.get_position()
        possible_moves = []
        if not piece.get_king():
            if piece.get_player() == 0:
                for dc in (-1, 1):
                    if (0 <= row-1 < self.rows) and (0 <= col+dc < self.columns) and \
                        (row-1, col+dc) not in self.get_all_pieces_positions():
                        possible_moves.append((row-1, col+dc))
            else:
                for dc in (-1, 1):
                    if (0 <= row+1 < self.rows) and (0 <= col+dc < self.columns) and \
                        (row+1, col+dc) not in self.get_all_pieces_positions():
                        possible_moves.append((row+1, col+dc))
        else:
            for dr in (-1, 1):
                for dc in (-1, 1):
                    if (0 <= row+dr < self.rows) and (0 <= col+dc < self.columns) and \
                        (row+dr, col+dc) not in self.get_all_pieces_positions():
                        possible_moves.append((row+dr, col+dc))    

        if len(possible_moves) == 0:
            return None
        else:
            return {piece: possible_moves}

    def is_jumpable(self, piece):
        '''CheckersBoard.is_jumpable(piece) -> dict
        returns a dict of the possible positions where piece can jump'''
        if piece.get_player() != self.current_player:
            return None

        (row, col) = piece.get_position()
        possible_jumps = []
        if not piece.get_king():
            if piece.get_player() == 0:
                for dc in (-1, 1):
                    if (0 <= row-1 < self.rows) and (0 <= col+dc < self.columns) and \
                        (row-1, col+dc) in self.get_all_pieces_positions(1):
                        if (0 <= row-2 < self.rows) and (0 <= col+2*dc < self.columns) and \
                            (row-2, col+2*dc) not in self.get_all_pieces_positions():
                            possible_jumps.append((row-2, col+2*dc))
            else:
                for dc in (-1, 1):
                    if (0 <= row+1 < self.rows) and (0 <= col+dc < self.columns) and \
                        (row+1, col+dc) in self.get_all_pieces_positions(0):
                        if (0 <= row+2 < self.rows) and (0 <= col+2*dc < self.columns) and \
                            (row+2, col+2*dc) not in self.get_all_pieces_positions():
                            possible_jumps.append((row+2, col+2*dc))
        else:
            if piece.get_player() == 0:
                for dr in (-1, 1):
                    for dc in (-1, 1):
                        if (0 <= row+dr < self.rows) and (0 <= col+dc < self.columns) and \
                            (row+dr, col+dc) in self.get_all_pieces_positions(1):
                            if (0 <= row+2*dr < self.rows) and (0 <= col+2*dc < self.columns) and \
                                (row+2*dr, col+2*dc) not in self.get_all_pieces_positions():
                                possible_jumps.append((row+2*dr, col+2*dc))
            else:
                for dr in (-1, 1):
                    for dc in (-1, 1):
                        if (0 <= row+dr < self.rows) and (0 <= col+dc < self.columns) and \
                            (row+dr, col+dc) in self.get_all_pieces_positions(0):
                            if (0 <= row+2*dr < self.rows) and (0 <= col+2*dc < self.columns) and \
                                (row+2*dr, col+2*dc) not in self.get_all_pieces_positions():
                                possible_jumps.append((row+2*dr, col+2*dc))

        if len(possible_jumps) == 0:
            return None
        else:
            return {piece: possible_jumps}


    def get_movable_pieces(self):
        '''CheckersBoard.get_movable_pieces() -> dict
        returns a list of pieces that can move'''
        movable_pieces = {}
        for p in self.pieces:
            if self.is_movable(p) is not None:
                movable_pieces[p] = self.is_movable(p).get(p)

        return movable_pieces

    def get_jumpable_pieces(self):
        '''CheckersBoard.get_jumpable_pieces() -> dict
        returns a list of pieces that can jump'''
        jumpable_pieces = {}
        for p in self.pieces:
            if self.is_jumpable(p) is not None:
                jumpable_pieces[p] = self.is_jumpable(p).get(p)
        
        return jumpable_pieces

    def get_playable_pieces(self):
        '''CheckersBoard.get_playable_pieces() -> dict
        returns a list of pieces that can be played'''
        if len(self.get_jumpable_pieces()) == 0:
            return self.get_movable_pieces()
        else:
            return self.get_jumpable_pieces()

    def move(self, piece, pos):
        piece.change_position(pos)
        (row, col) = pos
        if self.current_player == 0:
            if row == 0:
                piece.make_king()
        else:
            if row == 7:
                piece.make_king()

    def check_endgame(self):
        '''CheckersBoard.check_endgame()
        checks if game is over
        updates the endgame message if over'''
        pieces = [p for p in self.pieces if p.get_player() == self.current_player]
        if len(pieces) == 0 or len(self.get_playable_pieces()) == 0:
            self.endgame = 1 - self.current_player
        

class CheckersSquare(Canvas):
    '''displays a square in the Checkers game'''
    
    def __init__(self, master, pos):
        '''CheckersSquare(master)
        creates a new Checkers square'''
        super().__init__(master, width=50, height=50)

        self.master = master
        self.pos = pos

        # set the mouse events
        self.bind('<Button>', master.click_on)

    def get_position(self):
        '''CheckersSquare.get_position() -> (int, int)
        returns position of square'''
        return self.pos

    def show_piece(self, color, with_star=False):
        '''CheckersSquare.add_piece(color)
        adds a piece to square of color'''
        self.create_oval(10, 10, 44, 44, fill=color)
        if with_star:
            self.create_text(27, 35, fill='black', font=('Arial', 30), text='*')

    def highlight(self, on=True):
        if on:
            self['bg'] = 'light green'
            self['highlightbackground'] = 'yellow'
        else:
            self['bg'] = 'dark green'
            self['highlightbackground'] = 'dark green'

    def clear(self):
        '''CheckersSquare.clear()
        removes current piece on square'''
        oval_list = self.find_all()
        for oval in oval_list:
            self.delete(oval)


class CheckersGame(Frame):
    '''represents a game for Checkers'''
    
    def __init__(self, master, rows=8, columns=8, colors=('red', 'white')):
        '''CheckersGame(master[, rows=8, columns=8, colors=('red', 'white')])
        creates a new Checkers game with rows * columns board and pieces of colors'''
        super().__init__(master, bg='white')
        self.grid()
        
        # set up board and piece colors
        self.board = CheckersBoard(rows, columns)
        self.colors = colors

        # rows and columns
        # TODO: use rows and columns from self.board
        self.rows = rows
        self.columns = columns

        # create the squares
        self.squares = {}
        for row in range(rows):
            for col in range(columns):
                pos = (row, col)
                self.squares[pos] = CheckersSquare(self, pos)
                self.squares[pos].grid(row=row, column=col)
                
                # make the squares different colors
                if row % 2 == col % 2:
                    self.squares[pos]['bg'] = 'blanched almond'
                    self.squares[pos]['highlightbackground'] = 'blanched almond'
                else:
                    self.squares[pos]['bg'] = 'dark green'
                    self.squares[pos]['highlightbackground'] = 'dark green'

        # status configuration
        self.rowconfigure(rows, minsize=3)
        status_row = rows + 1

        # turn label in status row
        self.turn_label = Label(self, text='Turn:', font=('Arial', 14), bg='white')
        self.turn_label.grid(row=status_row, column=1)
        
        # turn color in status row
        self.turn_color = CheckersSquare(self, (status_row, 2))
        self.turn_color.grid(row=status_row, column=2)
        self.turn_color.unbind('<Button>')

        self.input_mode = 0     # input_mode: 0 for select, 1 for move

        self.highlight_squares = []
        for p in self.board.get_playable_pieces():
            self.highlight_squares.append(self.squares[p.get_position()])

        self.update_display()
    
    def click_on(self, event):
        square = event.widget
        pos = square.get_position()
        if not square in self.highlight_squares:
            return

        # turn highlight off on current highlightsqures
        for sq in self.highlight_squares: 
            sq.highlight(False)

        # TODO: update self.board, and update self.squares accordingly
        if self.input_mode == 1:
            self.input_mode = 0

            # self.board.move to change piece pos and remove piece if applicable
            was_not_king = not self.board.get_piece(self.selected_pos).get_king()
            self.board.move(self.board.get_piece(self.selected_pos), pos)
            (row_old, col_old) = self.selected_pos
            (row_new, col_new) = pos
            if abs(row_old-row_new) == 2 and abs(col_old-col_new) == 2:
                remove_pos = ((row_old+row_new) // 2, (col_old+col_new) // 2)
                self.board.remove_piece(self.board.get_piece(remove_pos))

                active_piece = self.board.get_piece(pos) 
                if active_piece not in self.board.get_playable_pieces():
                    self.board.next_player()
                    self.highlight_squares = []
                    for p in self.board.get_playable_pieces():
                        self.highlight_squares.append(self.squares[p.get_position()])
                else:
                    is_king = active_piece.get_king()
                    new_king = was_not_king and is_king
                    if (self.board.is_jumpable(active_piece) is not None) and (not new_king):
                        # need to jump again
                        self.input_mode = 1
                        self.selected_pos = pos
                        self.highlight_squares = []
                        for sq in self.get_movable_squares(self.squares[pos]):
                            self.highlight_squares.append(sq)
                    else:
                        self.board.next_player()
                        self.highlight_squares = []
                        for p in self.board.get_playable_pieces():
                            self.highlight_squares.append(self.squares[p.get_position()])
            else:
                self.board.next_player()

                self.highlight_squares = []
                for p in self.board.get_playable_pieces():
                    self.highlight_squares.append(self.squares[p.get_position()])

            self.board.check_endgame()
        else:
            self.input_mode = 1

            # set new highlight squares based on the selected square and movable squares
            self.highlight_squares = []
            for s in self.get_movable_squares(square):
                self.highlight_squares.append(s)

            self.selected_pos = square.get_position()

        self.update_display()

    def get_movable_squares(self, square):
        movable_squares = []
        piece = self.board.get_piece(square.get_position())
        for pos in self.board.get_playable_pieces().get(piece):
            movable_squares.append(self.squares[pos])

        return movable_squares

    def update_display(self):
        '''CheckersGame.update_display()
        updates squares to match board'''
        for pos in self.squares:
            self.squares[pos].clear()
        
        for piece in self.board.get_all_pieces():
            pos = piece.get_position()
            self.squares[pos].show_piece(self.colors[piece.get_player()], piece.get_king())

        if isinstance(self.board.get_endgame(), int):
            self.turn_color.clear()
            win_label = Label(self, text=f'{self.colors[1-self.board.get_player()]} wins!'.capitalize(), font=('Arial', 24))
            win_label.grid(row=self.rows+1, column=self.columns//2, columnspan=4)
            return

        for square in self.highlight_squares: 
            square.highlight()

        self.turn_color.show_piece(self.colors[self.board.get_player()])


def play_checkers():
    '''play_checkers()
    starts a game of Checkers'''
    root = Tk()
    root.title('Checkers')
    RG = CheckersGame(root)
    RG.mainloop()


play_checkers()
