#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox

# Цветовая палитра: Тру-Кибер-Минимализм
BG_COLOR = "#0D1117"          # Глубокий терминальный черный
PANEL_COLOR = "#161B22"       # Цвет панелей и кнопок
BORDER_COLOR = "#21262D"      # Цвет сетки и границ
TEXT_GREEN = "#7EE787"        # Хакерский зеленый для операторов
TEXT_NUM = "#C9D1D9"          # Цвет цифр (светло-серый)
ACCENT_COLOR = "#FF7B72"      # Розовый/Красный для C и =
CYAN_CYBER = "#00F0FF"        # Неоновый голубой для дисплея

class CyberMinimalCalc:
    def __init__(self, root):
        self.root = root
        self.root.title("CyberCalc v1.0.4")
        self.root.geometry("360x520")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)
        
        self.expression = ""
        self.buttons_dict = {}  # Для связи символов с объектами кнопок
        
        # Главный контейнер
        self.main_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.create_display()
        self.create_buttons()
        self.create_status_bar()
        
        # Биндинг клавиатуры
        self.root.bind("<Key>", self.on_key_press)

    def create_display(self):
        # Контейнер для дисплея с неоновой рамкой
        display_frame = tk.Frame(
            self.main_frame, 
            bg=PANEL_COLOR, 
            highlightbackground=BORDER_COLOR, 
            highlightthickness=2
        )
        display_frame.pack(fill="x", ipady=18, pady=(0, 15))
        
        self.display_label = tk.Label(
            display_frame, 
            text="0", 
            anchor="e", 
            bg=PANEL_COLOR, 
            fg=CYAN_CYBER, 
            font=("Courier", 26, "bold"),
            padx=15
        )
        self.display_label.pack(fill="x")

    def create_buttons(self):
        grid_frame = tk.Frame(self.main_frame, bg=BORDER_COLOR, bd=1)
        grid_frame.pack(fill="both", expand=True)

        button_layout = [
            ['C', '(', ')', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '⌫', '=']
        ]

        for i in range(5):
            grid_frame.rowconfigure(i, weight=1, uniform="equal")
        for i in range(4):
            grid_frame.columnconfigure(i, weight=1, uniform="equal")

        for r, row in enumerate(button_layout):
            for c, text in enumerate(row):
                self.create_flat_button(grid_frame, text, r, c)

    def create_flat_button(self, parent, text, row, col):
        if text in ['=', 'C']:
            fg_color = ACCENT_COLOR
        elif text in ['/', '*', '-', '+', '(', ')', '⌫']:
            fg_color = TEXT_GREEN
        else:
            fg_color = TEXT_NUM

        # highlightthickness=0 убирает уродливую дефолтную рамку фокуса Windows/Linux
        btn = tk.Button(
            parent, 
            text=text, 
            font=("Courier", 16, "bold"),
            bg=PANEL_COLOR, 
            fg=fg_color, 
            bd=0, 
            relief="flat",
            activebackground="#21262D",
            activeforeground=fg_color,
            highlightthickness=0,
            command=lambda: self.process_input(text)
        )
        btn.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

        # Сохраняем ссылку на кнопку, чтобы подсвечивать её при нажатии с клавиатуры
        self.buttons_dict[text] = btn

        # Эффект Hover
        btn.bind("<Enter>", lambda e: btn.config(bg="#30363D"))
        btn.bind("<Leave>", lambda e: btn.config(bg=PANEL_COLOR))

    def create_status_bar(self):
        # Хакерский статус-бар снизу для атмосферы
        status_label = tk.Label(
            self.main_frame,
            text="[SYSTEM: ONLINE]  [STATUS: READY]",
            font=("Courier", 9),
            bg=BG_COLOR,
            fg="#8B949E",
            anchor="w"
        )
        status_label.pack(fill="x", pady=(10, 0))

    def on_key_press(self, event):
        char = event.char
        key = event.keysym

        # Маппинг клавиш клавиатуры на символы калькулятора
        if char in "0123456789.+-*/()":
            self.flash_button(char)
            self.process_input(char)
        elif key in ("Return", "KP_Enter"):
            self.flash_button("=")
            self.process_input("=")
        elif key in ("BackSpace",):
            self.flash_button("⌫")
            self.process_input("⌫")
        elif key in ("Escape",):
            self.flash_button("C")
            self.process_input("C")

    def flash_button(self, char):
        # Визуальный отклик кнопки при нажатии с клавиатуры
        if char in self.buttons_dict:
            btn = self.buttons_dict[char]
            old_bg = btn.cget("bg")
            btn.config(bg="#30363D")
            # Возвращаем исходный цвет через 100 миллисекунд
            self.root.after(100, lambda: btn.config(bg=old_bg))

    def process_input(self, char):
        # Вся логика теперь в одном месте (и для кликов, и для клавиатуры)
        if char == 'C':
            self.expression = ""
        elif char == '⌫':
            self.expression = self.expression[:-1]
        elif char == '=':
            try:
                sanitized = self.expression.replace(' ', '')
                if sanitized:
                    result = str(eval(sanitized))
                    if '.' in result and len(result) > 12:
                        result = str(round(float(result), 6))
                    self.expression = result
            except ZeroDivisionError:
                messagebox.showerror("ERROR", "DIV_BY_ZERO")
                self.expression = ""
            except Exception:
                messagebox.showerror("ERROR", "SYNTAX_ERR")
                self.expression = ""
        else:
            if len(self.expression) < 14:
                self.expression += str(char)

        display_val = self.expression if self.expression != "" else "0"
        self.display_label.config(text=display_val)

if __name__ == "__main__":
    root = tk.Tk()
    app = CyberMinimalCalc(root)
    root.mainloop()