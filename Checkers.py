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
                if row % 2 != col % 2 and row < 3:
                    # player 0
                    self.pieces.append(CheckersPiece(self.player_ids[0], pos))
                elif row % 2 != col % 2 and row > 4:
                    # player 1
                    self.pieces.append(CheckersPiece(self.player_ids[1], pos))

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

    def is_movable(self, player, pos, is_king):
        '''CheckersBoard.is_movable(piece) -> bool
        returns True if piece is movable, False otherwise'''
        (row, col) = pos
        possible_moves = []
        if not is_king:
            if player == 0:
                for dc in (-1, 1):
                    if (0 <= row+1 < self.rows) and (0 <= col+dc < self.columns):
                        possible_moves.append((row+1, col+dc))
            else:
                for dc in (-1, 1):
                    if (0 <= row-1 < self.rows) and (0 <= col+dc < self.columns):
                        possible_moves.append((row-1, col+dc))
        else:
            for dr in (-1, 1):
                for dc in (-1, 1):
                    if (0 <= row+dr < self.rows) and (0 <= col+dc < self.columns):
                        possible_moves.append((row+dr, col+dc))    
                
        for p in self.get_all_pieces_positions():
            if p in possible_moves:
                possible_moves.remove(p)

        if len(possible_moves) != 0:
            return True
        else:
            return False

    def is_jumpable(self, piece):
        '''CheckersBoard.is_jumpable(piece) -> bool
        returns True if piece is jumpable, False otherwise'''
        if piece.get_player() != self.current_player:
            return False

        (row, col) = piece.get_position()
        possible_jumps = []
        if not piece.get_king():
            if self.current_player == 0:
                for dc in (-1, 1):
                    if (0 <= row+1 < self.rows) and (0 <= col+dc < self.columns) and \
                        (row+1, col+dc) in self.get_all_pieces_positions(1):
                        if (0 <= row+2 < self.rows) and (0 <= col+2*dc < self.columns) and \
                            (row+2, col+2*dc) not in self.get_all_pieces_positions():
                            possible_jumps.append((row+2, col+2*dc))
            else:
                for dc in (-1, 1):
                    if (0 <= row-1 < self.rows) and (0 <= col+dc < self.columns) and \
                        (row-1, col+dc) in self.get_all_pieces_positions(0):
                        if (0 <= row-2 < self.rows) and (0 <= col+2*dc < self.columns) and \
                            (row-2, col+2*dc) not in self.get_all_pieces_positions():
                            possible_jumps.append((row-2, col+2*dc))
        else:
            if self.current_player == 0:
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
                            (row+dr, col+dc) in self.get_all_pieces_positions(1):
                            if (0 <= row+2*dr < self.rows) and (0 <= col+2*dc < self.columns) and \
                                (row+2*dr, col+2*dc) not in self.get_all_pieces_positions():
                                possible_jumps.append((row+2*dr, col+2*dc))

        if len(possible_jumps) != 0:
            return True
        else:
            return False


    def get_movable_pieces(self):
        '''CheckersBoard.get_movable_pieces() -> list
        returns a list of pieces that can move'''
        movable_pieces = []
        for p in self.pieces:
            if self.is_movable(p):
                movable_pieces.append(p)

        return movable_pieces

    def get_jumpable_pieces(self):
        '''CheckersBoard.get_jumpable_pieces() -> list
        returns a list of pieces that can jump'''
        jumpable_pieces = []
        for p in self.pieces:
            if self.is_jumpable(p):
                jumpable_pieces.append(p)
        
        return jumpable_pieces


    def get_legal_jumps(self, position):
        '''CheckersBoard.get_legal_jumps(position) -> list
        returns a list legal jumps of the piece at position'''
        (row, col) = position
        legal_jumps = []

        # position does not have a king
        if not self.kings[position]:
            # jumps for player 0
            if self.board[position] == 0:
                for dc in (-1, 1):
                    # make sure that the adjacent pieces contain an opponent's piece
                    if (0 <= row + 1 < 8) and (0 <= col + dc < 8) and \
                       self.board[(row + 1, col + dc)] == 1:
                        # make sure that the jump is on an empty square
                        if (0 <= row + 2 < 8) and (0 <= col + 2*dc < 8) and \
                           self.board[(row + 1, col + 2*dc)] is None:
                            legal_jumps.append((row + 2, col + 2*dc))
            # jumps for player 1
            else:
                for dc in (-1, 1):
                    # make sure that the adjacent pieces contain an opponent's piece
                    if (0 <= row - 1 < 8) and (0 <= col + dc < 8) and \
                       self.board[(row - 1, col + dc)] == 0:
                        # make sure that the jump is on an empty square
                        if (0 <= row - 2 < 8) and (0 <= col + 2*dc < 8) and \
                           self.board[(row - 2, col + 2*dc)] is None:
                            legal_jumps.append((row - 2, col + 2*dc))
        # position has a king
        else:
            for dr in (-1, 1):
                for dc in (-1, 1):
                    # jumps for player 0 king
                    if self.board[position] == 0:
                        # make sure the adjacent squares have an opponent's piece
                        if (0 <= row + dr < 8) and (0 <= row + dc < 8) and \
                           self.board[(row + dr, col + dc)] == 1:
                            # make sure the jump is on an empty square
                            if (0 <= row + 2*dr < 8) and (0 <= row + 2*dc < 8) and \
                               self.board[(row + 2*dr, col + 2*dc)] is None:
                                legal_jumps.append((row + 2*dr, col + 2*dc))
                    # jumps for player 1 king
                    else:
                        # make sure the adjacent squares have an oppoent's piece
                        if (0 <= row + dr < 8) and (0 <= row + dc < 8) and \
                           self.board[(row + dr, col + dc)] == 0:
                            # make sure the jump is on an empty square
                            if (0 <= row + 2*dr < 8) and (0 <= row + 2*dc < 8) and \
                               self.board[(row + 2*dr, col + 2*dc)] is None:
                                legal_jumps.append((row + 2*dr, col + 2*dc))

        return legal_jumps

    def get_legal_actions(self):
        '''CheckersBoard.get_legal_actions() -> list
        returns a list of the current player's legal actions'''
        legal_actions = {}

        # check for pieces that can jump
        for row in range(8):
            for col in range(8):
                position = (row, col)
                if self.board[position] == self.current_player:
                    if self.get_legal_jumps(position) > 0:
                        legal_actions[position] = self.get_legal_jumps()
 
        # if there are no pieces that can jump, check for pieces that can move
        if len(legal_actions) == 0:
            for row in range(8):
                for col in range(8):
                    if self.board[position] == self.current_player:
                        if self.get_legal_moves(position) > 0:
                            legal_actions[position] = self.get_legal_moves()

        return legal_actions

    def check_endgame(self):
        '''CheckersBoard.check_endgame()
        checks if game is over
        updates the endgame message if over'''
        pieces = list(self.board.values())
        if pieces.count(self.current_player) == 0 or len(self.get_legal_actions()) == 0:
            self.endgame = 1 - self.current_player
        

class CheckersSquare(Canvas):
    '''displays a square in the Checkers game'''
    
    def __init__(self, master):
        '''CheckersSquare(master)
        creates a new Checkers square'''
        super().__init__(master, width=50, height=50)

        # set the mouse events
        self.bind('<Button>', master.choose_piece)
        self.bind('<Button>', master.move_piece)

    def add_piece(self, color):
        '''CheckersSquare.add_piece(color)
        adds a piece to square of color'''
        self.create_oval(10, 10, 44, 44, fill=color)

    def remove_piece(self):
        '''CheckersSquare.remove_piece()
        removes the current piece on square'''
        oval_list = self.find_all()
        for oval in oval_list:
            self.delete(oval)


class CheckersGame(Frame):
    '''represents a game for Checkers'''
    
    def __init__(self, master, rows=8, columns=8):
        '''CheckersGame(master)
        creates a new Checkers game'''
        super().__init__(master, bg='white')
        self.grid()
        
        # set up board and piece colors
        self.board = CheckersBoard()
        self.colors = ('red', 'white')

        # rows and columns
        self.rows = rows
        self.columns = columns

        # create the squares
        self.squares = {}
        for row in range(rows):
            for col in range(columns):
                pos = (row, col)
                self.squares[pos] = CheckersSquare(self)
                self.squares[pos].grid(row=row, column=col)
                
                # make the squares different colors
                if row % 2 == col % 2:
                    self.squares[pos]['bg'] = 'blanched almond'
                    self.squares[pos]['highlightbackground'] = 'blanched almond'
                else:
                    self.squares[pos]['bg'] = 'dark green'
                    self.squares[pos]['highlightbackground'] = 'dark green'

        self.rowconfigure(8, minsize=3)

        # turn label
        self.score_label = Label(self, text='Turn:', font=('Arial', 14), bg='white')
        self.score_label.grid(row=9, column=1)
        
        # turn color
        self.turn_color = CheckersSquare(self)
        self.turn_color.grid(row=9, column=2)
        self.turn_color.unbind('<Button>')

        self.update_display()

    def update_display(self):
        CheckersGame.update_display()
        '''updates squares to match board'''
        pos_0 = self.board.get_all_pieces_positions(0)
        pos_1 = self.board.get_all_pieces_positions(1)

        # add pieces to the right squares
        for p in pos_0:
            self.squares[p].add_piece(self.colors(0))
        for p in pos_1:
            self.squares[p].add_piece(self.colors(1))

        # set the turn to current player
        current_player = self.board.get_player()
        self.turn_color.remove_piece()
        self.turn_color.add_piece(self.colors[current_player])

    def choose_piece(self, event):
        '''CheckersGame.get_click(event)
        event handler for mouse click
        gets click data and boxes the clicked piece'''
        pass

    def move_piece(self, event):
        '''CheckersGame.move_piece(event)
        event handler for mouse click
        gets click data and moves the clicked piece'''
        pass


def play_checkers():
    '''play_checkers()
    starts a game of Checkers'''
    root = Tk()
    root.title('Checkers')
    RG = CheckersGame(root)
    RG.mainloop()


play_checkers()
