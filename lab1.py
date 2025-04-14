# ===== Импорты =====
import customtkinter as ctk
from datetime import datetime


# ===== Базовые классы интерфейса =====
class UIElement(ctk.CTkFrame):
    """Базовый класс для элементов интерфейса."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._create_widget()

    def _create_widget(self):
        pass


# ===== Элементы интерфейса =====
class ColorButtonPanel(UIElement):
    """Класс с панелью кнопок, изменяющих цвет display_panel"""
    def __init__(self, master, logger, display_panel, **kwargs):
        self.logger = logger
        self.display_panel = display_panel
        super().__init__(master, **kwargs)

    def _create_widget(self):
        colors = ["Red", "Green", "Blue"]
        frame = ctk.CTkFrame(self)
        frame.pack(pady=5)

        for color in colors:
            ctk.CTkButton(
                frame,
                text=color,
                width=100,
                command=lambda c=color.lower(): self._change_color(c)
            ).pack(side="left", padx=10)

    def _change_color(self, color):
        self.display_panel.configure(fg_color=color)
        self.logger.log(f"Цвет панели изменён на: {color}")

class ColorDisplayPanel(UIElement):
    """Отображает цвет, изменённый ColorButtonPanel"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def _create_widget(self):
        self.panel = ctk.CTkFrame(self, height=50)
        self.panel.pack(pady=10, fill="x")

    def configure(self, **kwargs):
        self.panel.configure(**kwargs)

class ButtonElement(UIElement):
    """Базовый элемент кнопки"""
    def __init__(self, master, text, logger, **kwargs):
        self.text = text
        self.logger = logger
        super().__init__(master, **kwargs)

    def _create_widget(self):
        self.button = ctk.CTkButton(self, text=self.text, command=self._on_click)
        self.button.pack(padx=5, pady=5)

    def _on_click(self):
        self.logger.log(f"Нажата кнопка: '{self.text}'")

class CheckboxElement(UIElement):
    """Базовый чекбокс"""
    def __init__(self, master, text, logger, **kwargs):
        self.text = text
        self.logger = logger
        super().__init__(master, **kwargs)

    def _create_widget(self):
        self.checkbox = ctk.CTkCheckBox(self, text=self.text, command=self._on_change)
        self.checkbox.pack(padx=5, pady=5)

    def _on_change(self):
        state = "включен" if self.checkbox.get() else "выключен"
        self.logger.log(f"Чекбокс '{self.text}' {state}")

class RadiobuttonGroup(UIElement):
    """Базовая группа радиокнопок"""
    def __init__(self, master, options, logger, **kwargs):
        self.options = options
        self.logger = logger
        self.var = ctk.StringVar()
        self.var.trace_add("write", self._on_change)
        super().__init__(master, **kwargs)

    def _create_widget(self):
        for i, (text, value) in enumerate(self.options.items()):
            rb = ctk.CTkRadioButton(self, text=text, variable=self.var, value=value)
            rb.pack(padx=5, pady=2 if i > 0 else 5, anchor="w")

    def _on_change(self, *args):
        selected_text = [k for k, v in self.options.items() if v == self.var.get()][0]
        self.logger.log(f"Выбрана радиокнопка: '{selected_text}'")

class ComboboxElement(UIElement):
    """Базовый выпадающий список"""
    def __init__(self, master, values, logger, **kwargs):
        self.values = values
        self.logger = logger
        super().__init__(master, **kwargs)

    def _create_widget(self):
        self.combobox = ctk.CTkComboBox(self, values=self.values, command=self._on_select)
        self.combobox.pack(padx=5, pady=5)

    def _on_select(self, value):
        self.logger.log(f"Выбрано значение в выпадающем списке: '{value}'")

class SliderElement(UIElement):
    """Базовый ползунок"""
    def __init__(self, master, from_, to, logger, **kwargs):
        self.from_ = from_
        self.to = to
        self.logger = logger
        super().__init__(master, **kwargs)

    def _create_widget(self):
        self.slider = ctk.CTkSlider(self, from_=self.from_, to=self.to, command=self._on_slide)
        self.slider.pack(padx=5, pady=5, fill="x")

    def _on_slide(self, value):
        self.logger.log(f"Ползунок перемещен: значение {value:.1f}")

class SwitchElement(UIElement):
    """Базовый переключатель"""
    def __init__(self, master, text, logger, command=None, **kwargs):
        self.text = text
        self.logger = logger
        self.command = command
        super().__init__(master, **kwargs)

    def _create_widget(self):
        self.switch = ctk.CTkSwitch(self, text=self.text, command=self._on_switch)
        self.switch.pack(padx=5, pady=5)

    def _on_switch(self):
        state = "включен" if self.switch.get() else "выключен"
        self.logger.log(f"Переключатель '{self.text}' {state}")
        if self.command:
            self.command(self.switch.get())

class SeparatorElement(UIElement):
    """Базовый разделитель"""
    def __init__(self, master, orientation="vertical", **kwargs):
        self.orientation = orientation
        super().__init__(master, **kwargs)

    def _create_widget(self):
        if self.orientation == "vertical":
            self.separator = ctk.CTkFrame(self, width=2, height=400, fg_color="gray")
        else:
            self.separator = ctk.CTkFrame(self, width=400, height=2, fg_color="gray")
        self.separator.pack(padx=5, pady=5)

class LabelElement(UIElement):
    """Базовый обычный текст"""
    def __init__(self, master, text, font_size=14, **kwargs):
        self.text = text
        self.font_size = font_size
        super().__init__(master, **kwargs)

    def _create_widget(self):
        self.label = ctk.CTkLabel(self, text=self.text, font=("Arial", self.font_size))
        self.label.pack(padx=5, pady=5)


# ===== Служебные классы =====
class TimerPanel:
    def __init__(self, label):
        self.label = label
        self.start_time = datetime.now()
        self._update()

    def _update(self):
        elapsed = (datetime.now() - self.start_time).seconds
        self.label.configure(text=f"С момента запуска прошло: {elapsed} секунд")
        self.label.after(5000, self._update)

class Logger:
    def __init__(self, text_widget, progressbar):
        self.text_widget = text_widget
        self.progressbar = progressbar

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"  # добавлен явный перенос строки
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", log_message)
        self.text_widget.configure(state="disabled")
        self.text_widget.see("end")
        self._update_progressbar()

    def _update_progressbar(self):
        log_content = self.text_widget.get("1.0", "end-1c")
        line_count = len(log_content.strip().split("\n"))
        progress = min(line_count / 1000, 1.0)
        self.progressbar.set(progress)

class MouseTracker:
    def __init__(self, logger):
        self.logger = logger
        self.enabled = False
        self.last_position = None

    def enable(self):
        self.enabled = True
        self.logger.log("Включено отслеживание мыши")

    def disable(self):
        self.enabled = False
        self.logger.log("Отключено отслеживание мыши")

    def track(self, event):
        if self.enabled:
            current_position = (event.x, event.y)
            if current_position != self.last_position:
                self.last_position = current_position
                self.logger.log(f"Курсор: X={event.x}, Y={event.y}")


# ===== Главный класс приложения =====
class Lab1App(ctk.CTk):
    """Основной класс приложения."""

    def __init__(self):
        super().__init__()
        self._configure_window()
        self._create_widgets()

    # --- Настройка окна ---
    def _configure_window(self):
        self.title("Лабораторная работа №1")
        self.geometry("1000x800")
        self.resizable(False, False)

    # --- Создание главных вкладок и интерфейса ---
    def _create_tabs(self):
        self.tabview = ctk.CTkTabview(self, width=900, height=700)
        self.tabview.pack(pady=20)
        self.ui_tab = self.tabview.add("Элементы интерфейса")
        self.rgb_tab = self.tabview.add("RGB")
        self.timer_tab = self.tabview.add("Таймер")
        self.log_tab = self.tabview.add("Логи")
    def _create_widgets(self):
        self._create_tabs()
        self._init_progressbar()
        self._init_logger()
        self._init_mouse_tracker()
        self._create_ui_panels()
        self._create_timer_panel()

    # --- Инициализация компонентов ---
    def _init_progressbar(self):
        self.progressbar = ctk.CTkProgressBar(self.ui_tab, width=200)
        self.progressbar.set(0)

    def _init_logger(self):
        self.log_textbox = ctk.CTkTextbox(
            self.log_tab,
            width=860,
            height=650,
            state="disabled"
        )
        self.log_textbox.pack(pady=10)
        self.logger = Logger(self.log_textbox, self.progressbar)
        self.logger.log("Приложение запущено")

    def _init_mouse_tracker(self):
        self.mouse_tracker = MouseTracker(self.logger)
        self.bind("<Motion>", self.mouse_tracker.track)

    def _toggle_mouse_tracking(self, state):
        if state:
            self.mouse_tracker.enable()
        else:
            self.mouse_tracker.disable()

    # --- Построение интерфейса вкладки ---
    def _create_ui_panels(self):
        # Панель 1: прогрессбар
        panel1 = ctk.CTkFrame(self.ui_tab)
        panel1.pack(pady=10, fill="x")

        label = ctk.CTkLabel(panel1, text="Заполненность логов (до 1000)", font=("Arial", 14))
        label.pack(pady=(10, 5))

        self.progressbar.master = panel1
        self.progressbar.pack(pady=5)

        SeparatorElement(self.ui_tab, orientation="horizontal", width=800).pack(pady=10)

        # Панель 2: кнопка, чекбокс, радиокнопки
        panel2 = ctk.CTkFrame(self.ui_tab)
        panel2.pack(pady=10, fill="x")

        ButtonElement(panel2, text="Кнопка", logger=self.logger, width=200).pack(pady=5)
        CheckboxElement(panel2, text="Чекбокс", logger=self.logger, width=200).pack(pady=5)
        RadiobuttonGroup(
            panel2,
            options={"Опция 1": "option1", "Опция 2": "option2"},
            logger=self.logger,
            width=200
        ).pack(pady=5)

        SeparatorElement(self.ui_tab, orientation="horizontal", width=800).pack(pady=10)

        # Панель 3: комбобокс, переключатели
        panel3 = ctk.CTkFrame(self.ui_tab)
        panel3.pack(pady=10, fill="x")

        ComboboxElement(
            panel3,
            values=["Вариант 1", "Вариант 2", "Вариант 3"],
            logger=self.logger,
            width=200
        ).pack(pady=5)

        SwitchElement(panel3, text="Переключатель", logger=self.logger, width=200).pack(pady=5)
        SwitchElement(
            panel3,
            text="Отслеживать мышь",
            logger=self.logger,
            command=self._toggle_mouse_tracking,
            width=200
        ).pack(pady=5)

        SeparatorElement(self.ui_tab, orientation="horizontal", width=800).pack(pady=10)

        # Панель 4: цветовые кнопки и панель
        panel4 = ctk.CTkFrame(self.rgb_tab)
        panel4.pack(pady=10, fill="x")

        self.color_display = ColorDisplayPanel(panel4)
        self.color_display.pack(pady=5, fill="x")

        ColorButtonPanel(panel4, logger=self.logger, display_panel=self.color_display).pack(pady=5)
        
    def _create_timer_panel(self):
        panel = ctk.CTkFrame(self.timer_tab)
        panel.pack(pady=20, fill="x")

        self.timer_label = ctk.CTkLabel(panel, text="С момента запуска прошло:", font=("Arial", 16))
        self.timer_label.pack(pady=20)
        self.timer = TimerPanel(self.timer_label)


# ===== Запуск приложения =====
if __name__ == "__main__":
    ctk.set_default_color_theme("green")
    app = Lab1App()
    app.mainloop()
