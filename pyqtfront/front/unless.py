from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)


class UselessWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Бесполезные функции")
        self.resize(600, 400)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(0, 20, 0, 0)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("Файл")
        help_menu = menu_bar.addMenu("Помощь")

        file_menu.addAction("Закрыть", self.close)
        help_menu.addAction("О программе", self.show_info)

        self.text_browser = QTextBrowser()
        # эта страничка рандом какой-то если честно
        htmltext = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Простая страничка</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
        }

        h1 {
            color: #FF1493;
            margin-bottom: 20px;
            text-align: center;
        }

        .card {
            background-color: #FFC0CB;
            padding: 20px 30px;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            text-align: center;
            transition: transform 0.2s;
        }

        .card p {
            color: #555;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <h1>Привет, я просто набор бесполезных функций!</h1>
    
    <div class="card">
        <p>Йоу!</p>
    </div>
</body>
</html>
"""
        self.text_browser.append(htmltext)

        layout.addWidget(self.text_browser)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.tab1 = QWidget()
        self.tab1_layout = QVBoxLayout(self.tab1)

        self.table = QTableWidget(5, 5)
        self.table.setHorizontalHeaderLabels([f"Колонка {i + 1}" for i in range(5)])
        self.table.setVerticalHeaderLabels([f"Строка {i + 1}" for i in range(5)])

        for i in range(5):
            for j in range(5):
                self.table.setItem(i, j, QTableWidgetItem(f"{i},{j}"))

        self.tab1_layout.addWidget(self.table)
        self.tabs.addTab(self.tab1, "Я бесполезная таблица!")

        self.tab2 = QWidget()
        self.tab2_layout = QVBoxLayout(self.tab2)
        self.tab2_text = QTextBrowser()
        self.tab2_text.setText("А я еще какая-то штука")
        self.tab2_layout.addWidget(self.tab2_text)
        self.tabs.addTab(self.tab2, "Я бесполезная штука")

        self.clear_button = QPushButton("Очистить текст")
        self.clear_button.clicked.connect(self.text_browser.clear)
        layout.addWidget(self.clear_button)

    def show_info(self):
        QtWidgets.QMessageBox.information(
            self, "О программе", "Это окно бесполезных функций, оно тут самое крутое"
        )
