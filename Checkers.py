from tkinter import *

class CheckersPiece:
    '''represents a piece of Checkers'''

    def __init__(self, player, pos, is_king=False):
        '''CheckersPiece(player, pos[, is_king=False])
        creates a Checkers piece of player, in which position, if king'''
        # attributes
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
        '''CheckersBoard.get_piece(pos) -> int or None
        returns the piece at position'''
        for p in self.pieces:
            # piece has been found
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
            # append all the positions
            if player is None:
                positions.append(p.get_position())
            # append only the positions of player
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
        '''CheckersBoard.get_endgame() -> int or None
        returns endgame state'''
        return self.endgame

    def is_movable(self, piece):
        '''CheckersBoard.is_movable(piece) -> dict or None
        returns a dict of the possible positions where piece can move
            key: piece, value: possible move positions
        returns None if piece cannot move'''
        # piece does not belong to current player
        if piece.get_player() != self.current_player:
            return None

        (row, col) = piece.get_position()
        possible_moves = []
        # piece is not king
        if not piece.get_king():
            # player 0
            if piece.get_player() == 0:
                # check the diagonal positions on top to see if they are empty
                for dc in (-1, 1):
                    if (0 <= row-1 < self.rows) and (0 <= col+dc < self.columns) and \
                        (row-1, col+dc) not in self.get_all_pieces_positions():
                        possible_moves.append((row-1, col+dc))
            # player 1
            else:
                # check the diagonal positions on the botton to see if they are empty
                for dc in (-1, 1):
                    if (0 <= row+1 < self.rows) and (0 <= col+dc < self.columns) and \
                        (row+1, col+dc) not in self.get_all_pieces_positions():
                        possible_moves.append((row+1, col+dc))
        # piece is king
        else:
            # check diangonal positions to see if they are empty
            for dr in (-1, 1):
                for dc in (-1, 1):
                    if (0 <= row+dr < self.rows) and (0 <= col+dc < self.columns) and \
                        (row+dr, col+dc) not in self.get_all_pieces_positions():
                        possible_moves.append((row+dr, col+dc))    

        # no possible moves
        if len(possible_moves) == 0:
            return None
        else:
            return {piece: possible_moves}

    def is_jumpable(self, piece):
        '''CheckersBoard.is_jumpable(piece) -> dict or None
        returns a dict of the possible positions where piece can jump
            key: piece, value: positions jump positions
        returns None if piece cannot jump'''
        # piece does not belong to current player
        if piece.get_player() != self.current_player:
            return None

        (row, col) = piece.get_position()
        possible_jumps = []
        # piece is not king
        if not piece.get_king():
            # player 0
            if piece.get_player() == 0:
                for dc in (-1, 1):
                    # check if the diagonal positions on top contains the other player's piece
                    if (0 <= row-1 < self.rows) and (0 <= col+dc < self.columns) and \
                        (row-1, col+dc) in self.get_all_pieces_positions(1):
                        # check if the positions over them are empty
                        if (0 <= row-2 < self.rows) and (0 <= col+2*dc < self.columns) and \
                            (row-2, col+2*dc) not in self.get_all_pieces_positions():
                            possible_jumps.append((row-2, col+2*dc))
            # player 1
            else:
                for dc in (-1, 1):
                    # check if the diagonal positions on the bottom contain the other player's piece
                    if (0 <= row+1 < self.rows) and (0 <= col+dc < self.columns) and \
                        (row+1, col+dc) in self.get_all_pieces_positions(0):
                        # check if the positions over them are empty
                        if (0 <= row+2 < self.rows) and (0 <= col+2*dc < self.columns) and \
                            (row+2, col+2*dc) not in self.get_all_pieces_positions():
                            possible_jumps.append((row+2, col+2*dc))
        # piece is king
        else:
            # player 0
            if piece.get_player() == 0:
                for dr in (-1, 1):
                    for dc in (-1, 1):
                        # check if the diagonal positions contain the other player's piece
                        if (0 <= row+dr < self.rows) and (0 <= col+dc < self.columns) and \
                            (row+dr, col+dc) in self.get_all_pieces_positions(1):
                            # check if the positions over them are empty
                            if (0 <= row+2*dr < self.rows) and (0 <= col+2*dc < self.columns) and \
                                (row+2*dr, col+2*dc) not in self.get_all_pieces_positions():
                                possible_jumps.append((row+2*dr, col+2*dc))
            # player 1
            else:
                for dr in (-1, 1):
                    for dc in (-1, 1):
                        # check if the diagonal positions contain the other player's piece
                        if (0 <= row+dr < self.rows) and (0 <= col+dc < self.columns) and \
                            (row+dr, col+dc) in self.get_all_pieces_positions(0):
                            # check if the positions over them are empty
                            if (0 <= row+2*dr < self.rows) and (0 <= col+2*dc < self.columns) and \
                                (row+2*dr, col+2*dc) not in self.get_all_pieces_positions():
                                possible_jumps.append((row+2*dr, col+2*dc))

        # no possible jumps
        if len(possible_jumps) == 0:
            return None
        else:
            return {piece: possible_jumps}


    def get_movable_pieces(self):
        '''CheckersBoard.get_movable_pieces() -> dict
        returns a dict of pieces that can move
            key: piece, value: possible move positions'''
        movable_pieces = {}
        for p in self.pieces:
            # check if piece is movable
            if self.is_movable(p) is not None:
                movable_pieces[p] = self.is_movable(p).get(p)

        return movable_pieces

    def get_jumpable_pieces(self):
        '''CheckersBoard.get_jumpable_pieces() -> dict
        returns a dict of pieces that can jump
            key: piece, value: possible jump positions'''
        jumpable_pieces = {}
        for p in self.pieces:
            # check if piece is jumpable
            if self.is_jumpable(p) is not None:
                jumpable_pieces[p] = self.is_jumpable(p).get(p)
        
        return jumpable_pieces

    def get_playable_pieces(self):
        '''CheckersBoard.get_playable_pieces() -> dict
        returns a dict of piece that can be played
            key: piece, value: playable positions'''
        # no pieces can jump
        if len(self.get_jumpable_pieces()) == 0:
            return self.get_movable_pieces()
        else:
            return self.get_jumpable_pieces()

    def move(self, piece, pos):
        '''CheckersBoard.move(piece, pos)
        moves piece to pos'''
        piece.change_position(pos)
        
        # player 0
        if self.current_player == 0:
            # turn piece into king if it reaches the end
            if pos[0] == 0:
                piece.make_king()
        # player 1
        else:
            # turn piece into king if it reaches the end
            if pos[0] == 7:
                piece.make_king()

    def check_endgame(self):
        '''CheckersBoard.check_endgame()
        checks if game is over
        updates the endgame message if over'''
        pieces = [p for p in self.pieces if p.get_player() == self.current_player]

        # check if there are no pieces left of current player or no playable pieces
        if len(pieces) == 0 or len(self.get_playable_pieces()) == 0:
            self.endgame = 1 - self.current_player
        

class CheckersSquare(Canvas):
    '''displays a square in the Checkers game'''
    
    def __init__(self, master, pos):
        '''CheckersSquare(master)
        creates a new Checkers square'''
        super().__init__(master, width=50, height=50)

        # attributes
        self.pos = pos

        # set the mouse events
        self.bind('<Button>', master.click_on)

    def get_position(self):
        '''CheckersSquare.get_position() -> (int, int)
        returns position of square'''
        return self.pos

    def show_piece(self, color, with_star=False):
        '''CheckersSquare.add_piece(color[, with_star=False])
        adds a piece to square of color'''
        self.create_oval(10, 10, 44, 44, fill=color)

        # star the piece
        if with_star:
            self.create_text(27, 35, fill='black', font=('Arial', 30), text='*')

    def highlight(self, on=True):
        '''CheckersSquare.highlight(on=True)
        highlights square if True, unhiglight if False'''
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
        # delete the piece
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

        # input_mode: 0 for select, 1 for move
        self.input_mode = 0

        # put the playable pieces in the highlight list
        self.highlight_squares = []
        for p in self.board.get_playable_pieces():
            self.highlight_squares.append(self.squares[p.get_position()])

        self.update_display()
    
    def click_on(self, event):
        '''CheckersGame.click_on(event)
        event handler for mouse click
        gets click data and tries to make a move'''
        square = event.widget
        pos = square.get_position()

        # do nothing if click is not on a highlighted square
        if not square in self.highlight_squares:
            return

        # turn highlight off on current highlighted squres
        for sq in self.highlight_squares: 
            sq.highlight(False)

        # move piece
        if self.input_mode == 1:
            self.input_mode = 0

            # move piece from selected pos to pos
            was_not_king = not self.board.get_piece(self.selected_pos).get_king()
            self.board.move(self.board.get_piece(self.selected_pos), pos)
            (row_old, col_old) = self.selected_pos
            (row_new, col_new) = pos

            # piece jumped
            if abs(row_old-row_new) == 2 and abs(col_old-col_new) == 2:
                remove_pos = ((row_old+row_new) // 2, (col_old+col_new) // 2)
                self.board.remove_piece(self.board.get_piece(remove_pos))

                active_piece = self.board.get_piece(pos) 
                
                # piece cannot continue jumping
                if active_piece not in self.board.get_playable_pieces():
                    self.board.next_player()

                    # put the new playable pieces in the highlight list
                    self.highlight_squares = []
                    for p in self.board.get_playable_pieces():
                        self.highlight_squares.append(self.squares[p.get_position()])
                # piece can continue jumping
                else:
                    is_king = active_piece.get_king()
                    new_king = was_not_king and is_king

                    # normal continuous jumping
                    if (self.board.is_jumpable(active_piece) is not None) and (not new_king):
                        self.input_mode = 1
                        self.selected_pos = pos

                        # highlight the new jump positions
                        self.highlight_squares = []
                        for sq in self.get_movable_squares(self.squares[pos]):
                            self.highlight_squares.append(sq)
                    # piece just became king after jumping
                    else:
                        self.board.next_player()

                        # put the new playable pieces in the highlight list
                        self.highlight_squares = []
                        for p in self.board.get_playable_pieces():
                            self.highlight_squares.append(self.squares[p.get_position()])
            else:
                self.board.next_player()

                # put the new playable pieces in the highlight list
                self.highlight_squares = []
                for p in self.board.get_playable_pieces():
                    self.highlight_squares.append(self.squares[p.get_position()])

            self.board.check_endgame()
        # select piece
        else:
            self.input_mode = 1

            # put the playable positions in the highlight list
            self.highlight_squares = []
            for s in self.get_movable_squares(square):
                self.highlight_squares.append(s)

            self.selected_pos = square.get_position()

        self.update_display()

    def get_movable_squares(self, square):
        '''CheckersGame.get_movable_squares(square) -> list
        returns a list of the squares that have a playable piece'''
        movable_squares = []
        piece = self.board.get_piece(square.get_position())

        # find the playable positions and append the corresponding squares to the list
        for pos in self.board.get_playable_pieces().get(piece):
            movable_squares.append(self.squares[pos])

        return movable_squares

    def update_display(self):
        '''CheckersGame.update_display()
        updates squares to match board'''
        # delete all pieces
        for pos in self.squares:
            self.squares[pos].clear()
        
        # put the pieces on the board in their current posiitons
        for piece in self.board.get_all_pieces():
            pos = piece.get_position()
            self.squares[pos].show_piece(self.colors[piece.get_player()], piece.get_king())

        # check if the game is over
        if isinstance(self.board.get_endgame(), int):
            self.turn_color.clear()
            win_label = Label(self, text=f'{self.colors[1-self.board.get_player()]} wins!'.capitalize(), font=('Arial', 24))
            win_label.grid(row=self.rows+1, column=self.columns//2, columnspan=4)
            return

        # highlight the squares which contain the squares that can be clicked
        for square in self.highlight_squares: 
            square.highlight()

        # show whose turn it is in the turn square
        self.turn_color.show_piece(self.colors[self.board.get_player()])


def play_checkers():
    '''play_checkers()
    starts a game of Checkers'''
    root = Tk()
    root.title('Checkers')
    CG = CheckersGame(root)
    CG.mainloop()


play_checkers()
