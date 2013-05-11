from ScrolledText import ScrolledText
import Tkinter as tk

from trace_json import traceparse
from parsley_json import jsonGrammar

jsonData = open('337141-steamcube.json').read()


class Tracer(object):

    def __init__(self, grammarWin, inputWin, logWin, trace):
        self.grammarWin = grammarWin
        self.inputWin = inputWin
        self.logWin = logWin
        self.trace = trace
        self.position = 0

    def advance(self):
        if self.position < len(self.trace):
            self.position += 1
            self.display()

    def rewind(self):
        if self.position > 0:
            self.position -= 1
            self.display()

    def display(self):
        def updateHighlight(w, start, end=None):
            w.tag_remove("highlight", "1.0", tk.END)
            start = "1.0+%sc" % (start,)
            if end is not None:
                end = "1.0+%sc" % (end,)
            w.tag_add("highlight", start, end)
            w.tag_configure("highlight", background="yellow")

        _, (grammarStart, grammarEnd), inputPos = self.trace[self.position]
        updateHighlight(self.grammarWin, grammarStart, grammarEnd)
        updateHighlight(self.inputWin, inputPos)


def display(grammar, src, trace):
    r = tk.Tk()
    f = tk.Frame(master=r)
    lt = ScrolledText(master=f)
    rt = ScrolledText(master=f)
    lt.pack(side="left", expand=True, fill="both")
    rt.pack(side="right", expand=True, fill="both")

    bot = ScrolledText(master=r, height=5)
    tracer = Tracer(lt, rt, bot, trace)
    toolbar = tk.Frame(master=r)
    tk.Button(toolbar, text="Next", width=5, command=tracer.advance).pack(
        side="left")
    tk.Button(toolbar, text="Prev", width=5, command=tracer.rewind).pack(
        side="left")
    f.pack(expand=1, fill="both")
    toolbar.pack(fill=tk.X)
    bot.pack(fill=tk.X)

    lt.insert(tk.END, grammar)
    rt.insert(tk.END, src)
    tracer.display()
    return r

_, trace = traceparse(jsonData)
root = display(jsonGrammar, jsonData, trace)

root.mainloop()
