import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore
import mainWindow
import BrownRobinson

class Application(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButtonCalculate.clicked.connect(self.calculate)
        self.spinBoxStrategyACount.valueChanged.connect(self.spinBoxAValueChanged)
        self.spinBoxStrategyBCount.valueChanged.connect(self.spinBoxBValueChanged)

    def calculate(self):
        strategyMatrix = []
        #Считываем входные данные
        for i in range(self.tableWidgetStrategyMatrixInput.rowCount()):
            strategyMatrix.append([])
            for j in range(self.tableWidgetStrategyMatrixInput.columnCount()):
                if self.tableWidgetStrategyMatrixInput.item(i, j) != None:
                    strategyMatrix[i].append(int(self.tableWidgetStrategyMatrixInput.item(i, j).text()))
                else:
                    strategyMatrix[i].append(0)
        maxError = float(self.lineEditMaxError.text())
        maxIteration = int(self.spinBoxMaxIterationCount.value())
        total = BrownRobinson.BrownRobinson(strategyMatrix, maxError, maxIteration)
        solution = total["solution"]
        answer = total["answer"]
        print(solution)
        print(maxError)
        print(maxIteration)
        print(strategyMatrix)
        #Вывыд пошагового решения
        self.tableWidgetSolution.setRowCount(len(solution) - 1)
        self.tableWidgetSolution.setColumnCount(len(solution[0]))
        header = ["Выбор\nА", "Выбор\nБ"]
        header.extend(["x{}".format(a+1) for a in range(self.spinBoxStrategyACount.value())])
        header.extend(["y{}".format(a+1) for a in range(self.spinBoxStrategyBCount.value())])
        header.extend(["Верхняя\nоценка", "Нижняя\nоценка", "Ошибка"])
        self.tableWidgetSolution.setHorizontalHeaderLabels(header)
        for i in range(1, len(solution)):
            for j in range(len(solution[0])):
                addItem = solution[i][j] if type(solution[i][j])=='int' else round(solution[i][j], 4)
                self.tableWidgetSolution.setItem(i-1, j, QtWidgets.QTableWidgetItem(str(addItem)))
        self.tableWidgetSolution.resizeColumnsToContents()

        self.tableWidgetAnswer.setRowCount(1)
        self.tableWidgetAnswer.setColumnCount(len(answer[0])+len(answer[1])+2)
        headerAnswer = ["x{}".format(a+1) for a in range(len(answer[0]))]
        headerAnswer.extend(["y{}".format(a+1) for a in range(len(answer[1]))])
        headerAnswer.extend(["Ошибка", "Выигрыш А/\nпроигрыш Б"])
        self.tableWidgetAnswer.setHorizontalHeaderLabels(headerAnswer)
        for i in range(len(answer[0])):
            self.tableWidgetAnswer.setItem(0, i, QtWidgets.QTableWidgetItem(str(round(answer[0][i], 3))))
        
        for i in range(len(answer[0]), len(answer[0])+len(answer[1])):
            self.tableWidgetAnswer.setItem(0, i, QtWidgets.QTableWidgetItem(str(round(answer[1][i-len(answer[0])], 3))))
        
        self.tableWidgetAnswer.setItem(0, len(answer[0])+len(answer[1]), QtWidgets.QTableWidgetItem(str(round(answer[2], 4))))
        self.tableWidgetAnswer.setItem(0, len(answer[0])+len(answer[1])+1, QtWidgets.QTableWidgetItem(str(round(answer[3], 4))))
        self.tableWidgetAnswer.resizeColumnsToContents()


    def spinBoxAValueChanged(self):
        self.tableWidgetStrategyMatrixInput.setRowCount(self.spinBoxStrategyACount.value()) 

    def spinBoxBValueChanged(self):
        self.tableWidgetStrategyMatrixInput.setColumnCount(self.spinBoxStrategyBCount.value()) 

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = Application()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()