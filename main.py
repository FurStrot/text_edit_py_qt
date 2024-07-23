import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, 
                             QWidget,
                             QLabel,
                             QVBoxLayout,
                             QHBoxLayout,
                             QPushButton,
                             QTextEdit,
                             QListWidget,
                             QLineEdit,
                             QInputDialog
                             )
from PyQt5.sip import voidptr

app = QApplication([])


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.init_ui()
        self.connects()
        self.show()
        try:
            with open("dict.json", "r", encoding="UTF-8") as file:
                self.notes_dict = json.load(file)
        except:
            with open("dict.json", "w") as file:
                self.notes_dict = {}
        self.create_notes_list()

    def __del__(self):
        pass

    def setup_window(self):
        self.setWindowTitle("Умные заметки")

    def init_ui(self):
        self.text_note = QTextEdit()

        text_label = QLabel("Список заметок")

        self.list_note = QListWidget()

        self.layout_btn_box1 = QHBoxLayout()
        self.btn_create_note = QPushButton("Создать заметку")
        self.btn_delite_note = QPushButton("Удалиить заметку")

        self.save_note = QPushButton("Сохранить все заметки")

        text_label_2 = QLabel("Список тегов")

        self.lise_tegs = QListWidget()

        self.line_edit_tegs = QLineEdit("Введите тег...")

        self.layout_btn_box2 = QHBoxLayout()
        self.btn_add_note = QPushButton("Добавить к заметке")
        self.btn_unpin_note = QPushButton("Открепить от заметки")

        self.btn_search_note = QPushButton("Искать заметки по тегу")

        self.main_layout = QHBoxLayout()
        self.right_layout = QVBoxLayout()


        self.right_layout.addWidget(text_label)
        self.right_layout.addWidget(self.list_note)
        
        #Коробка 1
        self.right_layout.addLayout(self.layout_btn_box1)
        self.layout_btn_box1.addWidget(self.btn_create_note)
        self.layout_btn_box1.addWidget(self.btn_delite_note)

        self.right_layout.addWidget(self.save_note)
        self.right_layout.addWidget(text_label_2)
        self.right_layout.addWidget(self.lise_tegs)
        self.right_layout.addWidget(self.line_edit_tegs)

        #Коробка 2
        self.right_layout.addLayout(self.layout_btn_box2)
        self.layout_btn_box2.addWidget(self.btn_add_note)
        self.layout_btn_box2.addWidget(self.btn_unpin_note)

        self.right_layout.addWidget(self.btn_search_note)

        self.main_layout.addWidget(self.text_note)
        self.main_layout.addLayout(self.right_layout)
        
        self.setLayout(self.main_layout)

    def connects(self):
        self.btn_create_note.clicked.connect(self.create_note)
        self.btn_delite_note.clicked.connect(self.delete_note)
        self.save_note.clicked.connect(self.save_text_notes)
        self.btn_add_note.clicked.connect(self.add_tags)
        self.list_note.itemClicked.connect(self.click_note)
        self.btn_unpin_note.clicked.connect(self.delete_tags)
    
    def create_note(self):
        text, flag = QInputDialog.getText(self, "Создание заметки", "Введите название заметки:")

        if text and flag:
            # self.list_note.addItem(text)
            self.notes_dict[text] = {"text": "", "tags": []}
            self.create_notes_list()
    
    def delete_note(self):
        selected_item = self.list_note.currentItem()
        if selected_item:
            note_name = selected_item.text()
            # if note_name in self.notes_dict:
            del self.notes_dict[note_name]
            self.text_note.clear()
            self.open_file("w")
            self.create_notes_list()
            
    def delete_tags(self):
        selected_item = self.lise_tegs.currentItem()
        find_note = self.list_note.currentItem()

        if selected_item and find_note:
            tage_name = selected_item.text()
            note_name = find_note.text()
            if tage_name in self.notes_dict[note_name]["tags"]:
                self.notes_dict[note_name]["tags"].remove(tage_name)
                self.lise_tegs.clear()
                self.open_file("w")
                self.create_notes_list()

    def create_notes_list(self):
        names_list = self.notes_dict.keys()
        names_list = sorted(names_list)
        self.list_note.clear()
        self.list_note.addItems(names_list)

    def save_text_notes(self):
        selected_item = self.list_note.currentItem()
        if selected_item:
            note_name = selected_item.text()
            self.notes_dict[note_name]["text"] = self.text_note.toPlainText()
            self.open_file("w")

    def open_file(self, type):
        with open("dict.json", type) as file:
            json.dump(self.notes_dict, file, ensure_ascii=False)
            
    def add_tags(self):
        selected_item = self.list_note.currentItem()
        self.text_teg = self.line_edit_tegs.text()
        if selected_item and self.text_teg:
            self.notes_dict[selected_item.text()]["tags"].append(self.text_teg)
            self.open_file("w")
        self.update_tage_list()
            
    def update_tage_list(self):
        selected_items = self.list_note.currentItem()
        if selected_items:
            tags = self.notes_dict[selected_items.text()]["tags"]
            self.lise_tegs.clear()
            self.lise_tegs.addItems(tags)
    
    def click_note(self):
        selected_item = self.list_note.currentItem()
        if selected_item:
            note_name = selected_item.text()
            text_note = self.notes_dict[note_name]["text"]
            tage_list = self.notes_dict[note_name]["tags"]
            self.text_note.setText(text_note)
            self.lise_tegs.clear()
            self.lise_tegs.addItems(tage_list)
    



window = MainWindow()
app.exec_()
# list("Привет!")
# ["П", "Р", "И", "В", "Е", "T", "!"]


# tuple("Привет!")
# ("П", "Р", "И", "В", "Е", "T", "!")

# ("Привет", True)