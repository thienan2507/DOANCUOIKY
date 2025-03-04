from DoAnCuoiKy.ui.DailySummary import Ui_Daily_Summary



class DailySummaryExt(Ui_Daily_Summary):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

    def showWindow(self):
        self.MainWindow.show()

