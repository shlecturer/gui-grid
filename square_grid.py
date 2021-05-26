import logging
from breezypythongui import EasyFrame
from grid_cell import GridCell


logging.basicConfig(level=logging.INFO)


class SquareGrid(EasyFrame):
    def __init__(self, title, n=10, side=50):
        EasyFrame.__init__(self, title=title)

        # Create a string of column indicators, e.g., 'ABCDEFGHIJ' (n=10)
        ord_a = 65  # Character 'A' ASCII code
        columns = ''.join([chr(x) for x in range(ord_a, ord_a + n)])

        # Initialise the data structure for all cells (nxn)
        cells = {x: [None] * n for x in columns}

        self.__cells = cells

        # Just the labels for the columns
        for col in columns:
            col_n = ord(col) - ord_a
            grid_cell = GridCell(self, side, side, outline='white')
            c = self.addCanvas(grid_cell, column=col_n+1, row=0)
            c.drawText(col, side//2, side//2, font=("Arial", 18, 'bold'))

        # Just the labels for the rows
        for row in range(1, n+1):
            grid_cell = GridCell(self, side, side, outline='white')
            c = self.addCanvas(grid_cell, column=0, row=row)
            c.drawText(str(row), side//2, side//2, font=("Arial", 18, 'bold'))

        # Initialise the grid -> the data structure is a dictionary.
        # The keys are 'A' .. 'J' (default) and the values are simply
        # lists indexed with the row number 0.. 9 (default).
        for col in columns:
            for row in range(n):
                col_n = ord(col) - ord_a
                grid_cell = GridCell(self, side, side, col, row)
                grid_cell.set_click_handler(self.on_click)
                cell = self.addCanvas(grid_cell, column=col_n+1, row=row+1)
                cells[col][row] = cell

    def on_click(self, col, row):
        """Called when a cell is clicked. The caller provides
        the coordinate of the cell. This can be used directly
        to address the cell in {self.__cells}.

        :col: Column of the cell ('A', 'B', ...)
        :row: Row of the cell (1, 2, ...)
        """
        logging.info(f'{col} {row}')


if __name__ == '__main__':
    grid = SquareGrid('My Grid', n=3)
    grid.mainloop()
