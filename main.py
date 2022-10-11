import tkinter as tk
import pandas as pd


def turn_commands_on_off(choice):
    def empty_fun():
        pass

    if choice == "on":
        studied_button.config(command=studied)
        not_studied_button.config(command=not_studied)
        reset_button.config(command=reset)
    elif choice == "off":
        studied_button.config(command=empty_fun)
        not_studied_button.config(command=empty_fun)
        reset_button.config(command=empty_fun)


def select_word(language):
    global word_num
    while True:
        if words["studied"][word_num] != "no":
            word_num += 1
        elif words["studied"][word_num] != "yes":
            return words[language][word_num]


def english_flash_card():
    turn_commands_on_off(choice="on")

    canvas.delete("all")

    english_word = select_word("english")

    canvas.create_image(405, 300, image=english_flash_card_img)

    title.config(text="English", bg=color_palette[3])
    word.config(text=english_word, bg=color_palette[3])


def german_flash_card():
    turn_commands_on_off(choice="off")

    canvas.delete("all")

    german_word = select_word("german")

    canvas.create_image(405, 300, image=german_flash_card_img)

    title.config(text="German", bg=color_palette[2])
    word.config(text=german_word, bg=color_palette[2])


def count():
    global global_studied_word
    global global_not_studied_word
    studied_word = 0
    not_studied_word = 0

    for index in words.index:
        if words.at[index, "studied"] == "no":
            not_studied_word += 1
        elif words.at[index, "studied"] == "yes":
            studied_word += 1

    global_studied_word = studied_word
    global_not_studied_word = not_studied_word

    counter_label.config(text=f"{studied_word}/{studied_word+not_studied_word}")
    counter_label.place(x=465, y=51)


def time():
    global timer_count
    global seconds

    if seconds >= 0:
        timer_label.config(text=f"00:0{seconds}")

    if seconds > 0:
        timer_count = root.after(1000, time)
        seconds -= 1

    else:
        seconds = 5
        english_flash_card()


def next_flash_card():
    global word_num
    count()

    if global_studied_word + global_not_studied_word < word_num+1:
        word_num = 0

    if global_not_studied_word != 0:
        german_flash_card()
        time()
    else:
        title.config(text="")
        word.config(text="Congratulations!")


def studied():
    global words
    global word_num

    words.at[word_num, "studied"] = "yes"
    words.to_csv("german_english_words.csv", sep=";", index=False)

    word_num += 1

    next_flash_card()


def not_studied():
    global words
    global word_num

    words.to_csv("german_english_words.csv", sep=";", index=False)

    word_num += 1

    next_flash_card()


def reset():
    global word_num
    global seconds
    global timer_count
    global global_studied_word
    global global_not_studied_word

    root.after_cancel(timer_count)
    seconds = 5

    global_studied_word = 0
    global_not_studied_word = 0

    for index in words.index:
        words.at[index, "studied"] = "no"
        words.to_csv("german_english_words.csv", sep=";", index=False)

    word_num = 0
    next_flash_card()


words = pd.read_csv("german_english_words.csv", sep=";")
word_num = 0
global_studied_word = 0
global_not_studied_word = 0
seconds = 5
timer_count = None

color_palette = ["#B1D0E0", "#6998AB", "#406882", "#1A374D"]

root = tk.Tk()
root.minsize(width=800, height=600)
root.config(bg=color_palette[0])
root.title("Flash Card App")

canvas = tk.Canvas(width=1000, height=1000, bg=color_palette[0])
canvas.place(x=0, y=0)

german_flash_card_img = tk.PhotoImage(file="flash_card_1.png")
english_flash_card_img = tk.PhotoImage(file="flash_card_2.png")

title = tk.Label(text="", font=("Arial", 32, "italic"), justify="center")
title.place(x=340, y=200)

word = tk.Label(text="", font=("Arial", 48, "bold"), justify="center")
word.place(x=300, y=280)

studied_img = tk.PhotoImage(file="studied.png")
studied_button = tk.Button(image=studied_img, bd=0)
studied_button.config(width=137, height=82)
studied_button.place(x=150, y=475)

not_studied_img = tk.PhotoImage(file="not_studied.png")
not_studied_button = tk.Button(image=not_studied_img, bd=0)
not_studied_button.config(width=137, height=82)
not_studied_button.place(x=345, y=475)

reset_img = tk.PhotoImage(file="reset.png")
reset_button = tk.Button(image=reset_img, bd=0)
reset_button.config(width=137, height=82)
reset_button.place(x=540, y=475)

counter_img = tk.PhotoImage(file="counter.png")
counter = tk.Button(image=counter_img, bd=0)
counter.config(width=137, height=82)
counter.place(x=430, y=30)
counter_label = tk.Label(font=("Arial", 30, "bold"), bg=color_palette[1])

timer_img = tk.PhotoImage(file="counter.png")
timer = tk.Button(image=timer_img, bd=0)
timer.config(width=137, height=82)
timer.place(x=235, y=30)
timer_label = tk.Label(font=("Arial", 30, "bold"), bg=color_palette[1])
timer_label.place(x=262.5, y=51)

next_flash_card()

root.mainloop()
