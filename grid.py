from breezypythongui import EasyCanvas, EasyFrame


class Grid(EasyFrame):
    ORD_A = 65  # Character 'A' ASCII code

    def __init__(self, title, n=10):
        EasyFrame.__init__(self, title=title)

        # Create a string of column indicators, e.g., 'ABCDEFGHIJ' (n=10)
        columns = ''.join([chr(x) for x in range(self.ORD_A, self.ORD_A + n)])

        # Initialise the data structure for all cells (nxn)
        cells = {x: [None] * n for x in columns}

        self.__cells = cells
        self.__click_handler = None

        for col in columns:
            col_n = ord(col) - self.ORD_A
            grid_cell = GridCell(self, 30, 30, outline='white')
            c = self.addCanvas(grid_cell, column=col_n+1, row=0)
            c.drawText(col, 15, 15, font=("Arial", 18, 'bold'))

        for row in range(1, 11):
            grid_cell = GridCell(self, 30, 30, outline='white')
            c = self.addCanvas(grid_cell, column=0, row=row)
            c.drawText(str(row), 15, 15, font=("Arial", 18, 'bold'))

        # Initialise the grid - data structure is a dictionary.
        # The columns are 'A' .. 'J' (default) and the row are simply
        # 1 .. 10 (default).
        for col in columns:
            for row in range(n):
                col_n = ord(col) - self.ORD_A
                grid_cell = GridCell(self, 30, 30, col, row)
                grid_cell.set_click_handler(self.on_click)
                cell = self.addCanvas(grid_cell, column=col_n+1, row=row+1)
                cells[col][row] = cell

    def set_click_handler(self, handler):
        self.__click_handler = handler

    def on_click(self, col, row):
        """Called when a cell is clicked. The caller provides
        the coordinate of the cell. This can be used directly
        to address the cell in {self.__cells}.

        :col: Column of the cell ('A', 'B', ...)
        :row: Row of the cell (1, 2, ...)
        """
        if self.__click_handler is not None:
            self.__click_handler(col, row)


class GridCell(EasyCanvas):
    def __init__(self, parent, width, height, col=None, row=None,
                 outline='lightgrey', fill='white'):
        EasyCanvas.__init__(self, parent, width=width, height=height)

        # Store coordinate of cell for click handler
        self.__coordinate = col, row

        # Needed for the click handler
        self.__click_handler = None

        self.drawRectangle(0, 0, width-1, height-1, outline=outline, fill=fill)

    def set_click_handler(self, handler):
        self.__click_handler = handler

    def mouseReleased(self, event):
        """We consider the mouseReleased event to be a "clicked" event,
        since there is no actual mouseClicked event.
        """
        if self.__click_handler is not None:
            self.__click_handler(*self.__coordinate)


if __name__ == '__main__':
    grid = Grid('My Grid')
    grid.set_click_handler(lambda col, row: print(col, row))
    grid.mainloop()
