#0717 サンプルで作った関数
#年・月・日データからその日の分で登録されている予定のタイトルを呼び出す。
#引数を、カレンダー本体のyear,month＋押された日のボタンを参照してやれば予定一覧出力はできる。
#back_buttonが押されたら、年＋月を参照して再度calendarを生成すればよさげ
#listboxの要素はダブルクリックで反応してくれているので、その後の処理を見出す

#0728 クラス実装を投げ捨てて関数だけでどうにかしようとしたやつ
#月ごとのカレンダーの部分を追加実装。動きに不備なし

import tkinter as tk
import datetime
import sqlite3
import calendar

def immediately(li):
    print (li.curselection())

def month_calendar(year=datetime.datetime.now().year,month=datetime.datetime.now().month):
    def create_calendar(year,month):
        try:
            for key,item in day.items():
                item.destroy()
        except:
            pass
        cal=calendar.Calendar()
        days=cal.monthdayscalendar(year,month)
        day={}
        for i in range(0,42):
            c = i - (7 * int(i/7))
            r = int(i/7)
            try:
                # 日付が0でなかったら、ボタン作成 cが曜日、rが週目
                if days[r][c] != 0:#祝日判定→あかんこれn週目の月曜日とかの判別できてへん… 月毎にn回目の月曜日を判定すればよい？
                    if (((month==1 and days[r][c]==1)or(month==1 and c==0 and r==1)or
                         (month==2 and days[r][c]==11)or(month==3 and days[r][c]==21)or
                         (month==4 and days[r][c]==29)or(month==5 and (days[r][c]==3 or days[r][c]==4 or days[r][c]==5))or
                         (month==7 and c==0 and r==3)or(month==8 and days[r][c]==11)or(month==9 and c==0 and r==3)or
                         (month==9 and days[r][c]==23)or(month==10 and r==2 and c==0)or(month==11 and days[r][c]==3)or
                         (month==11 and days[r][c]==23)or(month==12 and days[r][c]==23))and c!=5 and c!=6):
                        day[i] = tk.Button(frame_calendar,font=("",14),height=2,width=4,relief="flat",text = days[r][c],fg="red")
                        day[i].grid(column=c,row=r)
                    else:
                        day[i] = tk.Button(frame_calendar,font=("",14),height=2,width=4,relief="flat",text = days[r][c])
                        day[i].grid(column=c,row=r)
            except:
                """
                月によっては、i=41まで日付がないため、日付がないiのエラー回避が必要
                """
                break
    root=tk.Tk()
    root.title("%d年%d月 カレンダー"%(year,month))
    frame_top=tk.Frame(root)
    frame_top.pack(pady=5)
    previous_month=tk.Label(frame_top,text="<",font=("",14))
    #previous_month.bind("<1>",change_month)
    previous_month.pack(side="left",padx=10)
    current_year=tk.Label(frame_top,text=year,font=("",18))
    current_year.pack(side="left")
    current_month=tk.Label(frame_top,text=month,font=("",18))
    next_month=tk.Label(frame_top,text=">",font=("",14))
    #next_month.bind("<1>",change_month)
    next_month.pack(side="left",padx=10)

    frame_week=tk.Frame(root)
    frame_week.pack()
    button_mon = tk.Button(frame_week,font=("",14),height=2,width=4,relief="flat",text = "Mon")
    button_mon.grid(column=0,row=0)
    button_tue = tk.Button(frame_week,font=("",14),height=2,width=4,relief="flat",text = "Tue")
    button_tue.grid(column=1,row=0)
    button_wed = tk.Button(frame_week,font=("",14),height=2,width=4,relief="flat",text = "Wed")
    button_wed.grid(column=2,row=0)
    button_thu = tk.Button(frame_week,font=("",14),height=2,width=4,relief="flat", text = "Thu")
    button_thu.grid(column=3,row=0)
    button_fri = tk.Button(frame_week,font=("",14),height=2,width=4,relief="flat", text = "Fri")
    button_fri.grid(column=4,row=0)
    button_sta = tk.Button(frame_week,font=("",14),height=2,width=4,relief="flat", text = "Sat", fg = "blue")
    button_sta.grid(column=5,row=0)
    button_san = tk.Button(frame_week,font=("",14),height=2,width=4,relief="flat", text = "San", fg = "red")
    button_san.grid(column=6,row=0)

    frame_calendar=tk.Frame(root)
    frame_calendar.pack()
    create_calendar(year,month)

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
#day_schedule(date.year,7,17)
month_calendar()
