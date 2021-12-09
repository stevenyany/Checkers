from tkinter import *

class CheckersSquare(Canvas):
    '''displays a square in the Checkers game'''
    
    def __init__(self, master, row, col):
        '''CheckersSquare(master, row, col)
        creates a new, blank Checkers square at coordinate (row, col)'''
        # create and place the widget
        super().__init__(master, width=50, height=50)
        self.grid(row=row, column=col)

        # set the attributes
        self.position = (row, col)

        # set the mouse events
        self.bind('<Button-1>', master.choose_piece)
        self.bind('<Button-1>', master.move_piece)

    def get_position(self):
        '''CheckersSquare.get_position() -> (int, int)
        returns (row, column) of square'''
        return self.position

    def add_piece(self, color):
        '''CheckersSquare.add_piece(color)
        adds a piece to square of color'''
        self.create_oval(10, 10, 44, 44, fill=color)

    def remove_piece(self):
        '''CheckersSquare.remove_piece()
        removes the current piece on square'''
        oval_list = self.find_all()
        # clear square
        for oval in oval_list:
            self.delete(oval)


class CheckersBoard:
    '''represents a board of Checkers'''
    
    def __init__(self):
        '''CheckersBoard()
        creates a CheckersBoard in starting position'''
        self.board = {}
        # create opening position
        for row in range(8):
            for col in range(8):
                position = (row, col)
                
                # find starting positions
                if row % 2 != col % 2 and row < 3:
                    # player 0
                    self.board[position] = 0
                elif row % 2 != col % 2 and row > 4:
                    # player 1
                    self.board[position] = 1
                # empty positions
                else:
                    self.board[position] = None

        self.current_player = 0

    def get_piece(self, position):
        '''CheckersBoard.get_piece(position) -> int
        returns the piece at position'''
        return self.board[position]

    def get_player(self):
        '''CheckersBoard.get_player() -> int
        returns the current player'''
        return self.current_player


class CheckersGame(Frame):
    '''represents a game for Checkers'''
    
    def __init__(self, master):
        '''CheckersGame(master)
        creates a new Checkers game'''
        super().__init__(master, bg='white')
        self.grid()
        
        # set up board and piece colors
        self.board = CheckersBoard()
        self.colors = ('red', 'white')

        # create the squares
        self.squares = {}
        for row in range(8):
            for col in range(8):
                position = (row, col)
                self.squares[position] = CheckersSquare(self, row, col)
                
                # make the squares different colors
                if row % 2 == col % 2:
                    self.squares[position]['bg'] = 'blanched almond'
                    self.squares[position]['highlightbackground'] = 'blanched almond'
                else:
                    self.squares[position]['bg'] = 'dark green'
                    self.squares[position]['highlightbackground'] = 'dark green'

        self.rowconfigure(8,minsize=3)

        # turn label
        self.score_label = Label(self, text='Turn:', font=('Arial', 14), bg='white')
        self.score_label.grid(row=9, column=1)
        
        # turn color
        self.turn_color = CheckersSquare(self, 9, 2)
        self.turn_color.unbind('<Button-1>')

        self.update_display()

    def update_display(self):
        '''CheckersGame.update_display()
        updates squares to match board'''
        for row in range(8):
            for col in range(8):
                position = (row, col)
                piece = self.board.get_piece(position)

                # add pieces to the right squares
                if piece is not None:
                    self.squares[position].add_piece(self.colors[piece])

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
    game = CheckersGame(root)
    game.mainloop()

play_checkers()