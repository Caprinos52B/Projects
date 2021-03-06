from tkinter import *
import random
import time
# Sorting algorithm visualiser
# Made by Adi Bozzhanov


class Display(Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.arr = [i for i in range(1, 11)]
        self.bars = []
        self.timeP = 1
        self.algs = {
            "Bubble Sort": self.bubble,
            "Insertion Sort": self.insertionSort,
            "Radix Sort": self.radixSort
        }
        self.spacing = (int(self["width"]) - 100) / 10
        self.w = self.spacing - 2
        self.scale = (int(self["heigh"]) - 100) / len(self.arr)

        for i in range(10):
            self.bars.append(self.create_rectangle(
                (50 + i * self.spacing, int(self["height"])),
                (50 + i * self.spacing + self.w,
                 int(self["height"]) - self.arr[i] * self.scale),
                fill="white"
            ))

    def displayBars(self):
        self.delete("all")
        self.bars = []
        self.spacing = (int(self["width"]) - 100) / len(self.arr)
        self.w = self.spacing - 2
        self.scale = (int(self["heigh"]) - 100) / len(self.arr)
        for i in range(len(self.arr)):
            self.bars.append(self.create_rectangle(
                (50 + i * self.spacing, int(self["height"])),
                (50 + i * self.spacing + self.w,
                 int(self["height"]) - self.arr[i] * self.scale),
                fill="white"
            ))
        pass

    def editBar(self, ind, val, clr="white"):
        self.delete(self.bars[ind])
        self.bars[ind] = self.create_rectangle(
            (50 + ind * self.spacing, int(self["height"])),
            (50 + ind * self.spacing + self.w,
             int(self["height"]) - val * self.scale),
            fill=clr
        )

    def shuffle(self):
        random.shuffle(self.arr)
        self.displayBars()

    def arraySize(self, n):
        self.arr = [i for i in range(1, int(n) + 1)]
        self.shuffle()

    def sort(self, alg):
        self.algs[alg]()

    def bubble(self):
        s = False
        for i in range(len(self.arr) - 1):
            if not s:
                s = True
                for j in range(len(self.arr) - i - 1):
                    if self.arr[j + 1] < self.arr[j]:
                        self.arr[j + 1], self.arr[j] = self.arr[j], self.arr[j + 1]
                        s = False

                    self.editBar(j, self.arr[j], "red")
                    self.editBar(j + 1, self.arr[j + 1])
                    time.sleep(self.timeP)
                    self.update()
                    self.editBar(j, self.arr[j])
                    self.editBar(j + 1, self.arr[j + 1])

    def insertionSort(self):
        for i in range(1, len(self.arr)):
            ind = i
            val = self.arr[ind]

            while self.arr[ind - 1] > val and ind > 0:
                self.arr[ind] = self.arr[ind - 1]
                self.editBar(ind, self.arr[ind], "red")
                time.sleep(self.timeP)
                self.update()
                self.editBar(ind, self.arr[ind])
                ind -= 1

            self.arr[ind] = val
            self.editBar(ind, self.arr[ind], "red")
            time.sleep(self.timeP)
            self.update()
            self.editBar(ind, self.arr[ind])

    def radixSort(self):
        colorScheme = ["#008000", "#008B00", "#009900", "#00AF33",
                       "#00C5CD", "#00CD00", "#00CED1", "#00EE76", "#00FA9A", "#00FF66"]
        colorScheme.reverse()
        #Each color in the colorScheme corresponds to a specific digit from 1 to 9

        for i in range(1, 4):
            #sort numbers by units, then by tens, then by hundreds
            newArr = [[] for i in range(10)]
            for j, each in enumerate(self.arr):
                #For each number in array put it into the corresponding list in newArr
                if len(str(each)) >= i:
                    ind = int(str(each)[-i])
                    newArr[ind].append(each)

                else:
                    ind = 0
                    newArr[0].append(each)
                self.editBar(j, each, "red")
                time.sleep(self.timeP)
                self.update()
                self.editBar(j, each, colorScheme[ind])

            self.arr = []
            k = 0
            for j, each in enumerate(newArr):
                if each:
                    for item in each:
                        self.arr.append(item)

                        self.editBar(k, item, "red")
                        time.sleep(self.timeP)
                        self.update()
                        if i == 3:
                            self.editBar(k, item)
                        else:
                            self.editBar(k, item, colorScheme[j])
                        k += 1

        pass


class UI(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.barColor = "LightBlue"
        self.configure(bg=self.barColor)
        self.master.update()
        self.font = ("Consolas", 18)
        self.can = Display(self, width=1600, height=800, bg="black")
        self.can.grid(row=0, column=0)
        self.btnFrame = Frame(self, bg=self.barColor)
        self.btnFrame.grid(row=1, column=0, sticky=W)
        self.alg = "Bubble Sort"
        self.pop = None

        self.shuffleBtn = Button(
            self.btnFrame,
            text="Shuffle",
            command=self.shuffle,
            font=self.font,
            bg=self.barColor
        )
        self.shuffleBtn.grid(row=0, column=0)

        self.slider = Scale(
            self.btnFrame,
            from_=10,
            to=300,
            orient=HORIZONTAL,
            font=self.font,
            label="Number of Elements",
            length=350,
            width=30,
            command=self.sliderUpdate,
            showvalue=0,
            bg=self.barColor,
            troughcolor=self.barColor
        )
        self.slider.grid(row=0, column=2)

        self.speedSlider = Scale(
            self.btnFrame,
            from_=1,
            to=10,
            orient=HORIZONTAL,
            font=self.font,
            label="Speed",
            length=350,
            width=30,
            command=self.updateSpeed,
            showvalue=0,
            bg=self.barColor,
            troughcolor=self.barColor
        )
        self.speedSlider.grid(row=0, column=4)

        self.speedLbl = Label(
            self.btnFrame,
            text="1",
            font=self.font,
            bg=self.barColor
        )
        self.speedLbl.grid(row=0, column=5)

        self.displayNum = Label(
            self.btnFrame,
            text="10",
            font=self.font,
            bg=self.barColor
        )
        self.displayNum.grid(row=0, column=3)

        self.sortBtn = Button(
            self.btnFrame,
            text="Sort",
            command=self.sort,
            font=self.font,
            bg=self.barColor
        )
        self.sortBtn.grid(row=0, column=1)

        self.algBtn = Button(
            self.btnFrame,
            text="Choose Algorithm",
            font=self.font,
            bg=self.barColor,
            command=self.chooseAlg
        )
        self.algBtn.grid(row=0, column=6)

        self.algLbl = Label(
            self.btnFrame,
            text="Bubble Sort",
            font=self.font,
            bg=self.barColor
        )
        self.algLbl.grid(row=0, column=7)

    def shuffle(self):
        self.can.shuffle()
        pass

    def sliderUpdate(self, val):
        self.displayNum["text"] = val
        self.can.arraySize(val)

    def sort(self):
        self.shuffleBtn["state"] = "disabled"
        self.slider["state"] = "disabled"
        self.sortBtn["state"] = "disabled"
        self.algBtn["state"] = "disabled"
        self.can.sort(self.alg)

        self.shuffleBtn["state"] = "normal"
        self.slider["state"] = "normal"
        self.sortBtn["state"] = "normal"
        self.algBtn["state"] = "normal"

    def updateSpeed(self, val):
        self.speedLbl["text"] = val
        self.can.timeP = (0.5)**(int(val) * 2)

    def chooseAlg(self):
        self.pop = Toplevel()
        btns = []
        var = StringVar()
        for i, alg in enumerate(self.can.algs):
            btns.append(Radiobutton(
                self.pop,
                text=alg,
                variable=var,
                value=alg,
                command=lambda: self.setAlg(var.get()),
                font=self.font
            ))
            btns[i].pack()

        self.pop.mainloop()

    def setAlg(self, val):
        self.alg = val
        self.algLbl["text"] = val
        self.pop.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Sorting Visualiser")
    ui = UI(root)
    ui.pack()

    root.mainloop()
