from DoAnCuoiKy.ui.ImportExport import Ui_mainWindow


class ImportExportExt(Ui_mainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

    def showWindow(self):
        self.MainWindow.show()

