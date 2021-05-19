import logging
from breezypythongui import EasyCanvas, EasyFrame

logging.basicConfig(level=logging.INFO)


class Grid(EasyFrame):
    def __init__(self, title, n=10):
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
            grid_cell = GridCell(self, 30, 30, outline='white')
            c = self.addCanvas(grid_cell, column=col_n+1, row=0)
            c.drawText(col, 15, 15, font=("Arial", 18, 'bold'))

        # Just the labels for the rows
        for row in range(1, 11):
            grid_cell = GridCell(self, 30, 30, outline='white')
            c = self.addCanvas(grid_cell, column=0, row=row)
            c.drawText(str(row), 15, 15, font=("Arial", 18, 'bold'))

        # Initialise the grid -> the data structure is a dictionary.
        # The keys are 'A' .. 'J' (default) and the values are simply
        # lists indexed with the row number 0.. 9 (default).
        for col in columns:
            for row in range(n):
                col_n = ord(col) - ord_a
                grid_cell = GridCell(self, 30, 30, col, row)
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


class GridCell(EasyCanvas):
    def __init__(self, parent, width, height, col=None, row=None,
                 outline='lightgrey', fill='white'):
        EasyCanvas.__init__(self, parent, width=width, height=height)

        self.__fill = fill
        self.__outline = outline
        self.__rect = self.drawRectangle(0, 0, width - 1, height - 1,
                                         outline=outline, fill=fill)

        try:
            # Try to get the on_click event handler from the parent
            self.__click_handler = lambda: parent.on_click(col, row)
        except AttributeError:
            logging.warning('Parent does not have on_click method.')
            self.__click_handler = None

    def mousePressed(self, event):
        self.itemconfigure(self.__rect, outline='white')

    def mouseReleased(self, event):
        """We consider the mouseReleased event to be a "clicked" event,
        since there is no actual mouseClicked event.
        """
        self.itemconfigure(self.__rect, outline=self.__outline)

        if self.__click_handler is not None:
            self.__click_handler()


if __name__ == '__main__':
    grid = Grid('My Grid')
    grid.mainloop()
