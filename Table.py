from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractScrollArea

class Table(QTableWidget):

    def __init__(self, title='Data Table', column1='time', column2='data'):
        super().__init__()
        self.title = title
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        #self.resizeColumnsToContents()
        self.currentRows = 0
        self.setRowCount(self.currentRows)
        self.setColumnCount(2)

    def addData(self, newx, newy):
        self.currentRows += 1
        self.setRowCount(self.currentRows)
        self.setItem(self.currentRows-1,0, QTableWidgetItem(str(newx)))
        self.setItem(self.currentRows-1,1, QTableWidgetItem(str(newy)))
        #self.resizeColumnsToContents()

    def clear(self):
        self.currentRows = 0
        self.setRowCount(self.currentRows)


