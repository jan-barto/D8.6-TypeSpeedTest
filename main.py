from tkinter import *
from tkinter import messagebox
from data import words_list


class TypingSpeedTester:
    def __init__(self):
        self.window = Tk()
        self.window.title("Typing Speed Tester")
        self.window.config(padx=70, pady=70)
        self.canvas = Canvas(width=700, height=500)

        # word bank
        self.word_bank = words_list

        # formatting options
        self.FONT = "Verdana"
        self.SIZE = 14

        # counting and time
        self.timer_on = False
        self.word_num = 0
        self.score = 0
        self.seconds_limit = 20
        self.seconds_actual = None

        # setting the widgets on the grid
        self.time_text = Label()
        self.time_text.grid(row=0, column=2, sticky="e")

        self.feedback_text = Label()
        self.feedback_text.grid(row=0, column=0, sticky="w")

        self.label_file = Label()
        self.label_file.grid(row=0, column=1, sticky="ew", columnspan=1)

        self.text = Text()
        self.text.grid(row=1, column=0, sticky="ew", columnspan=3)

        self.label_text = Label()
        self.label_text.grid(row=3, column=0, sticky="ew", columnspan=3)

        self.entry_text = Entry()
        self.entry_text.grid(row=4, column=0, sticky="w", columnspan=3)

        self.button_perform = Button()
        self.button_perform.grid(row=5, column=0, sticky="s")

        self.button_reset = Button()
        self.button_reset.grid(row=5, column=2, sticky="s")

        self.score_text = Label()
        self.score_text.grid(row=6, column=0, sticky="w", columnspan=3)

        # running set
        self.set_widgets_to_start_condition()
        self.window.mainloop()

    def set_widgets_to_start_condition(self):
        self.seconds_actual = self.seconds_limit
        self.score = 0
        self.time_text.config(text=f"Zbývající čas: {self.seconds_actual}", font=(self.FONT, int(self.SIZE / 1.5)))
        self.feedback_text.config(text="", font=(self.FONT, int(self.SIZE / 2)), fg="white", bg=self.window.cget('bg'))
        self.label_file.config(text="Text k reprodukci:", font=(self.FONT, self.SIZE))
        self.text.config(height=5, width=30, font=(self.FONT, self.SIZE))
        self.text.insert(END, f"stisknětě tlačítko spustit\na objeví se text k přepisu.")
        self.label_text.config(text="Sem zadávejte svůj text:", font=(self.FONT, self.SIZE))
        self.entry_text.config(width=40, font=(self.FONT, self.SIZE), state="normal")
        self.entry_text.insert(END, "")
        self.entry_text.delete(0, END)
        self.entry_text.focus()
        self.button_perform.config(text="Spustit", command=self.start_the_type_speed_test, font=(self.FONT, self.SIZE),
                                   state="active")
        self.button_reset.config(text="Resetovat", command=self.reset_the_type_speed_test, font=(self.FONT, self.SIZE),
                                 state="active")
        self.score_text.config(text=f"Skóre: {self.score}", font=(self.FONT, self.SIZE - 2))

    def start_timer(self):
        if self.timer_on:
            self.window.bind("<space>", self.evaluate_word)
            self.time_text.config(text=f"Čas: {self.seconds_actual}")
            self.seconds_actual -= 1
            if self.seconds_actual >= 0:
                self.window.after(1000, self.start_timer)
            else:
                self.show_result()

    def show_result(self):
        self.entry_text.config(state="disabled")
        result = self.score / self.seconds_limit * 60
        msg = f"Váš výsledek je: ---{round(result, 2)}--- slov za minutu."
        messagebox.showinfo(title="Test rychlosti psaní je u konce.",
                            message=msg)
        self.text.insert(END, f"\n\n {msg}")
        self.timer_on = False

    def start_the_type_speed_test(self):
        self.timer_on = True
        self.update_text_and_score()
        self.button_perform.config(state="disabled")
        self.start_timer()

    def reset_the_type_speed_test(self):
        self.text.delete(1.0, END)
        self.entry_text.delete(0, END)
        self.set_widgets_to_start_condition()
        self.timer_on = False

    def update_text_and_score(self):
        self.text.delete(1.0, END)
        self.text.insert(END, self.word_bank[self.word_num:self.word_num + 15])
        self.score_text.config(text=f"Skóre: {self.score}")

    def evaluate_word(self, event):
        written = self.entry_text.get()[:-1]
        if written == self.word_bank[self.word_num]:
            self.score += 1
            self.feedback_text.config(text="dobře", bg="green")
        else:
            self.feedback_text.config(text="špatně", bg="red")
        self.entry_text.delete(0, END)
        self.word_num += 1
        self.update_text_and_score()


app = TypingSpeedTester()
