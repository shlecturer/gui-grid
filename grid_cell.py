from breezypythongui import EasyCanvas


class GridCell(EasyCanvas):
    def __init__(self, parent, width, height, col=None, row=None,
                 outline='lightgrey', fill='white'):
        EasyCanvas.__init__(self, parent, width=width, height=height)

        self.__col = col
        self.__row = row
        self.__fill = fill
        self.__outline = outline
        self.__shapes = []

        self.__rect = self.drawRectangle(0, 0, width - 1, height - 1,
                                         outline=outline, fill=fill)

        self.__click_handler = None

    def set_click_handler(self, handler):
        """Set click handler. The function or method that is passed in
        as the argument {handler} must accept the required arguments
        col and row.
        """
        self.__click_handler = lambda: handler(self.__col, self.__row)

    def clear(self):
        """Delete any shapes that have been drawn in this GridCell.
        """
        for shape in self.__shapes:
            self.delete(shape)

    def draw_naught(self, padding=6, outline='red'):
        """Draw a naught. Use the provided or default values for padding
        and the outline.
        """
        width, height = int(self.getWidth()) - padding, int(self.getHeight()) - padding
        self.__shapes.append(self.drawOval(padding, padding, width, height, outline=outline))

    def draw_cross(self, padding=6, fill='blue'):
        """Draw a cross. Use the provided or default values for padding
        and the fill colour.
        """
        width, height = int(self.getWidth()) - padding, int(self.getHeight()) - padding
        self.__shapes.append(self.drawLine(padding, padding, width, height, fill=fill))
        self.__shapes.append(self.drawLine(padding, height, width, padding, fill=fill))

    def mousePressed(self, event):
        self.itemconfigure(self.__rect, outline='white')

    def mouseReleased(self, event):
        """We consider the mouseReleased event to be a "clicked" event,
        since there is no actual mouseClicked event. That is why we
        call the click handler from within this method.
        """
        self.itemconfigure(self.__rect, outline=self.__outline)

        if self.__click_handler is not None:
            self.__click_handler()
