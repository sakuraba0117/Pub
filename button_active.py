from tkinter import *

root = Tk()
root.option_add('*font', ('FixedSys', 14))

var = StringVar()
var.set('normal')

# ボタン
b = Button(root, text = 'button',
           activeforeground = 'green', disabledforeground = 'red')
b.pack(fill = X)

# 状態の変更
def change_state(): b.configure(state = var.get())

# ラジオボタンの設定
for x in ('normal', 'active', 'disabled'):
    Radiobutton(root, text = x, value = x,
                variable = var, command = change_state).pack(anchor = W)

root.mainloop()
