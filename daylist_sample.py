#0717 サンプルで作った関数
#年・月・日データからその日の分で登録されている予定のタイトルを呼び出す。
#引数を、カレンダー本体のyear,month＋押された日のボタンを参照してやれば予定一覧出力はできる。
#back_buttonが押されたら、年＋月を参照して再度calendarを生成すればよさげ
#listboxの要素はダブルクリックで反応してくれているので、その後の処理を見出す


import tkinter as tk
import datetime
import sqlite3

def immediately(li):
    print (li.curselection())

def day_schedule(year,month,day):
    def back_button():
        root.destroy()
    def append_item():
        root.destroy()
    def item_selected(number):
        sql = "SELECT * from schedule where rowid=%d"
        conn.execute(sql,number)
        data=c.fetchall()
        root.destroy()
    root=tk.Tk()
    root.title("%d年%d月%d日 予定一覧"% (year,month,day))

    c=sqlite3.connect("post_test.db")
    conn= c.cursor()
    conn.execute("SELECT title,time from schedule")
    #conn.execute("SELECT title,time from schedule where year = %d AND month = %d AND day = %d"%(year,month,day))
    data = conn.fetchall();

    #frame=tk.Frame(root,bd=2,relief="ridge")
    #frame.pack()
    button=tk.Button(root,text="戻る",command=back_button)
    button.pack(anchor="nw")
    
    frame1 = tk.Frame(root,pady=10)
    frame1.pack(anchor=tk.N)
    listbox = tk.Listbox(frame1,selectmode='BROWSE')
    listbox.pack(side="top")
    
    #データ数のくくりは、dataの長さの半分。それぞれセットにしてリストボックスへ出力
    print(len(data))
    for i in range(0,(len(data))):
        words = data[i]
        listbox.insert(tk.END,words)
    item = map(int,listbox.curselection())
    listbox.bind('<<ListboxSelect>>',immediately(listbox))

    frame2 = tk.Frame(root,pady=10)
    frame2.pack(anchor=tk.S)
    button = tk.Button(frame2,text="予定追加",command=append_item)
    button.pack(side="right")
    root.mainloop()

date = datetime.datetime.now()
print(date.year)
day_schedule(date.year,7,17)

