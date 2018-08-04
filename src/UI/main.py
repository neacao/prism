#!/usr/bin/env python3
import sys, time
import tkinter as tk


def window():
	root = tk.Tk()
	logo = tk.PhotoImage(file = "test.gif")
	explanation = """At present, only GIF and PPM/PGM
formats are supported, but an interface 
exists to allow additional image file
formats to be added easily."""
	w = tk.Label(root, 
          justify=tk.LEFT,
          compound = tk.LEFT,
          padx = 10, 
          text=explanation, 
          image=logo).pack(side="right")

	root.mainloop()


if __name__ == "__main__":
	window()
