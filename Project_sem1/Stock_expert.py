from tkinter import *
from tkinter import messagebox
import urllib.request


def find_word(String, pat, first, k=0):
    if(k == 0): k = len(String)
    i = first
    while(i < k):
        if((String[i] == pat[0]) or (String[i] == pat[0].upper())):
            j = 1
            while ((j < len(pat)) and (i + j < len(String)) and (String[i + j] == pat[j])):
                j += 1
                if (j == len(pat)): return i + j
            i = i + j
        else:
            i += 1
    return i


def extraction(pat_start, pat_end, text, start):
    arr = []
    i = 0
    end = 0
    ch0 = find_word(text, start, end)
    while(i < len(text)):
        start = find_word(text, pat_start, ch0)
        end = find_word(text, pat_end, start)
        ch0 = end
        i = end
        tmp = text[start:end - len(pat_end)]
        tmp0 = tmp.split(">")
        try:
            lol = float(tmp0[len(tmp0) - 1])
            if(lol < 0):
                lol = float("%.5f" % lol)
            elif(lol < 10):
                lol = float("%.3f" % lol)
            else:
                lol = float("%.2f" % lol)
            arr += [lol]
        except ValueError:
            print(tmp0[len(tmp0) - 1])
            #pass
    return arr


def array_pars(symb):
    page = urllib.request.urlopen("https://finance.yahoo.com/quote/" + symb + "/history?p=" + symb)
    mass = str(page.read())
    return extraction(',"open":', ',"high"', mass, "HistoricalPriceStore")


def reordering(arr):
    for i in range(0, len(arr)//2 + 1):
        if(i != len(arr) - i - 1):
            tmp = arr[i]
            arr[i] = arr[len(arr) - i - 1]
            arr[len(arr) - i - 1] = tmp

def max_min(a):
    max = a[0]
    min = a[0]
    for i in range(1, len(a)):
        if(max < a[i]):
            max = a[i]
        if(min > a[i]):
            min = a[i]
    return [min, max]


def dif_average(a):
    Average = 0
    for i in range(0, len(a)):
        Average += a[i]

    return(a[len(a) - 1] - float(Average)/len(a))


#average_growth(a) returns the value of average growth between a[i] and a[i+1]
# and total increase and decrease
def average_growth(a):
    increase = 0
    decrease = 0
    for i in range(0, len(a) - 2):
        if(a[i + 1] > a[i]):
            increase += (a[i + 1] - a[i])
        if(a[i + 1] < a[i]):
            decrease += (a[i + 1] - a[i])

    return [increase, decrease, (increase + decrease)/(len(a) - 1)]


def extremal_values_BEST(a):
    i = 1
    extr_val = []
    while(i < len(a)):
        #ascending interval
        if((i < len(a)) and (a[i] > a[i - 1])):
            extr_val += [[i, 1]]
            i += 1
            while((i < len(a)) and (a[i] >= a[i - 1])):
                extr_val[len(extr_val) - 1][0] = i
                i += 1
        #descending interval
        if((i < len(a)) and (a[i] < a[i - 1])):
            extr_val += [[i, -1]]
            i += 1
            while ((i < len(a)) and (a[i] <= a[i - 1])):
                extr_val[len(extr_val) - 1][0] = i
                i += 1
        if((i < len(a)) and (a[i] == a[i - 1])):
            i += 1
    return extr_val


def define_trend(extr, arr):
    aver_pos = 0
    c_pos = 0
    aver_neg = 0
    c_neg = 0
    t = extr[0][1]
    av_d_incr = 0
    av_d_decr = 0

    for i in range(0, len(extr)-2):
        if(extr[i][1] == 1):
            aver_pos += (arr[extr[i+2][0]] - arr[extr[i][0]])/(extr[i+2][0] - extr[i][0])
            av_d_incr += extr[i+2][0] - extr[i][0]
            c_pos += 1
        if (extr[i][1] == -1):
            aver_neg += (arr[extr[i+2][0]] - arr[extr[i][0]])/(extr[i+2][0] - extr[i][0])
            av_d_decr += extr[i+2][0] - extr[i][0]
            c_neg += 1
    aver_pos /= c_pos
    aver_neg /= c_neg
    av_d_incr /= c_pos
    av_d_decr /= c_neg
    last = extr[len(extr)-2][1]
    trend = extr[len(extr)-2][0]
    trend = 199 - trend

    return [aver_pos, aver_neg, av_d_incr, av_d_decr, trend, last]



Crypts = ['BTC-USD', 'XRP-USD', 'ETH-USD', 'BCH-USD', 'XLM-USD', 'LTC-USD', 'EOS-USD',
          'USDT-USD', 'TRX-USD', 'ADA-USD', 'BNB-USD', 'IOT-USD', 'XNR-USD', 'NEO-USD',
          'DASH-USD', 'XEM-USD', 'VEN-USD', 'ETC-USD', 'WAVES-USD', 'ZEC-USD', 'ZRX-USD',
          'XRB-USD', 'LINK-USD', 'DOGE-USD', 'BTG-USD']

Stocks = {'General Electric': 'GE',   'Bank of American Corporation': 'BAC',   'Kinross Gold Corporation': 'KGC',
          'Advances Micro Devices, Inc.': 'AMD',   'Microsoft Company': 'MSFT',   'Apple Inc': 'AAPL',
          'AT&T Inc.': 'T',   'Cisco Systems, Inc.': 'CSCO',   'Chesapeake Energy Corporation': 'CHK',
          'Oracle Corporation': 'ORCL',   'Pfizer Inc.': 'PFE',   'Ford Motor Company': 'F',
          'Facebook, Inc.': 'FB',   'Verzion Communications Inc.': 'VZ',
          'Enbridge Energy Partners, L.P.': 'EEP',   'Micron Technology, Inc.': 'MU',   'Intel Corporation': 'INTC',
          'Citigroup Inc.': 'C',   'JD.com, Inc.': 'JD',   'Exxon Mobil Corporation': 'XOM',
          'Huntington Bancshares Incorporated': 'HBAN',   'JPMorgan Chase & Co.': 'JPM',   'Comcast Corporation': 'CMCSA',
          'Twitter, Inc.': 'TWTR', 'Canada Goose Holdings, Inc.': 'GOOS',   'ANGI Homeservices Inc.': 'ANGI',
          'Red Eagle Mining Corporation': 'RDEMF',   'Suzano Papel e Celulose S.A.': 'SUZ',   'Federal National Mortgage Association': 'FNMAM',
          'Freddie Mac': 'FMCCO',   'AmTrust Financial Services, Inc.': 'AFSS',   'Uxin Limited': 'UXIN',
          'NIKE, Inc.': 'NKE',   'Grupo Mexico S.A.B. de C.V.': 'GMBXF',   'Genworth Financial, Inc.': 'GNW',
          'Ashmore Group PLC': 'AJMPF',   'The Stars Group Inc.': 'TSG',   'ASOS Plc': 'ASOMY',
          'Immunomedics, Inc.': 'IMMU',   'Hengan International Group Compamy Limited': 'HEGIY',   'Valeo SA': 'VLEEY',
          'Just Eat plc': 'JSTTY', 'MFA Financial, Inc.': 'MFA-PB',
          'Perrigo Company plc': 'PRGO',   'ZhongAn Online P&C Insurance Co., Ltd.': 'ZZHGF',   'Hutchison China MediTech Limited': 'HCM',
          'Telecom Italia S.p.A.': 'TIAOF',   'Jazz Pharmaceuticals plc': 'JAZZ',   'Amarin Corporation plc': 'AMRN',
          'Etsy, Inc': 'ETSY', '2U, Inc': 'TWOU',   'Bilibili, Inc.': 'BILI',
          'The Trade Desk': 'TTD',   'Coupa Software Incorporated': 'COUP',   'Conagra Brands, Inc.': 'CAG', 'MSA Safety Incorporated': 'MSA',
          'Akcea Therapeutics, Inc.': 'AKCA', 'MongoDB, Inc.': 'MDB', 'Blueprint Medecines Corporation': 'BPMC',
          'Delek US Holdings, Inc.': 'DK',   'BlackBerry Limited': 'BB',   "BJ's Wholesale Club Holdings, Inc.": 'BJ',
          'Nine Dragons Paper (Holdings) Limited': 'NDGPF',   'Pluralsight, Inc.': 'PS',   'LiveRamp Holdings, Inc.': 'RAMP'}

name = [""]
type = [""]

def start_page():
    c.place_forget()
    bt_back_stoc.place_forget()
    bt_back_cryp.place_forget()
    bt_back_entr.place_forget()
    bt_back_start.place_forget()
    bt_choose_stoc.place_forget()
    bt_choose_cryp.place_forget()
    bt_choose_entr.place_forget()
    list_stoc.place_forget()
    list_cryp.place_forget()
    scroll_stoc.place_forget()
    scroll_cryp.place_forget()
    en_field.place_forget()
    lb_stoc.pack_forget()
    lb_cryp.pack_forget()
    lb_entr.place_forget()
    lb_name.pack_forget()
    output.place_forget()

    lb_main.pack()
    lb.pack()
    bt_cryp.place(x=525, y=340, height=50, width=150)
    bt_stoc.place(x=525, y=280, height=50, width=150)
    bt_entr.place(x=525, y=220, height=50, width=150)


def stocks():
    c.place_forget()
    output.place_forget()
    bt_back_stoc.place_forget()
    bt_cryp.place_forget()
    bt_entr.place_forget()
    bt_stoc.place_forget()
    lb_main.pack_forget()
    lb.pack_forget()
    lb_name.pack_forget()

    type[0] = "stoc"
    lb_stoc.pack()
    list_stoc.place(x=10, y=50, height=200, width=250)
    scroll_stoc.place(x=260, y=50, height=200, width=20)
    bt_choose_stoc.place(x=10, y=250, height=30, width=270)
    bt_back_start.place(x=1130, y=600, height=30, width=50)


def crypts():
    c.place_forget()
    output.place_forget()
    bt_back_cryp.place_forget()
    bt_cryp.place_forget()
    bt_back_entr.place_forget()
    bt_entr.place_forget()
    bt_stoc.place_forget()
    lb_main.pack_forget()
    lb.pack_forget()
    lb_name.pack_forget()

    type[0] = "cryp"
    lb_cryp.pack()
    list_cryp.place(x=10, y=50, height=200, width=80)
    scroll_cryp.place(x=90, y=50, height=200, width=20)
    bt_choose_cryp.place(x=10, y=250, height=30, width=100)
    bt_back_start.place(x=1130, y=600, height=30, width=50)


def man_ent():
    c.place_forget()
    output.place_forget()
    bt_back_entr.place_forget()
    bt_cryp.place_forget()
    bt_stoc.place_forget()
    bt_entr.place_forget()
    lb_main.pack_forget()
    lb.pack_forget()
    lb_name.pack_forget()

    type[0] = "entr"
    out.set("Here you can choose any market by typing it's symbol")
    output.pack()
    lb_entr.place(x=10, y=235, height=30, width=200)
    en_field.place(x=220, y=235, height=30, width=100)
    bt_choose_entr.place(x=220, y=285, height=30, width=60)
    bt_back_start.place(x=1130, y=600, height=30, width=50)



def analysis():
    a=[]
    if (type[0] == "cryp"):
        sel = list_cryp.curselection()
        if(sel == ()):
            messagebox.showinfo("Help", "Please choose currency\nby click")
            return

    if (type[0] == "stoc"):
        sel = list_stoc.curselection()
        if(sel == ()):
            messagebox.showinfo("Help", "Please choose stock\nby click")
            return

    if(type[0] == "entr"):
        name[0] = en_field.get()
        a = array_pars(name[0])
        if(a == []):
            messagebox.showinfo("Help", "Sorry there's no market\nwith such symbol")
            return

    c.place_forget()
    list_stoc.place_forget()
    list_cryp.place_forget()
    scroll_stoc.place_forget()
    scroll_cryp.place_forget()
    en_field.place_forget()
    lb_stoc.pack_forget()
    lb_cryp.pack_forget()
    lb_entr.place_forget()
    lb_name.pack_forget()
    bt_choose_stoc.place_forget()
    bt_choose_cryp.place_forget()
    bt_choose_entr.place_forget()
    bt_back_start.place_forget()

    text = ""

    if(type[0] == "cryp"):
        sel = list_cryp.curselection()
        name[0] = list_cryp.get(first=sel)
        a = array_pars(name[0])
        reordering(a)
        text += 'difference: ' + str("%.3f" % dif_average(a)) + "\n"
        p = average_growth(a)
        text += 'average growth: ' + str("%.5f" % p[2]) + "\n"
        bt_back_cryp.place(x=1040, y=610, height=30, width=50)

    if(type[0] == "stoc"):
        sel = list_stoc.curselection()
        name[0] = list_stoc.get(first=sel)
        a = array_pars(Stocks[name[0]])
        reordering(a)
        text += 'difference: ' + str("%.3f" % dif_average(a)) + "\n"
        p = average_growth(a)
        text += 'average growth: ' + str("%.5f" % p[2]) + "\n"
        bt_back_stoc.place(x=1040, y=610, height=30, width=50)

    if(type[0] == "entr"):
        reordering(a)
        text += 'difference: ' + str("%.3f" % dif_average(a)) + "\n"
        p = average_growth(a)
        text += 'average growth: ' + str("%.5f" % p[2])
        bt_back_entr.place(x=1040, y=610, height=30, width=50)

    if (len(a) > 200):
        b = a[len(a) - 200:]
    else:
        b = a
    MM = max_min(b)
    k = (MM[1] - MM[0]) / 480
    c.delete("all")
    c.create_line(100, 500, 900, 500, fill="#00e")
    c.create_line(100, 500, 100, 0, fill="#00e")
    for i in range(1, 25):
        c.create_line(95, 500 - i*20, 900, 500 - i*20, fill="black", activefill="white")
        c.create_line(95, 500 - i*20, 105, 500 - i*20, fill="#00e")
        if (MM[0] + (i * 20) * k < 10):
            lol = "%.5f" % (MM[0] + (i*20)*k)
        else:
            lol = "%.2f" % (MM[0] + (i*20)*k)
        c.create_text(50, 500 - i*20, text=lol, fill="white", font="Veranda 8")

    for i in range(0, len(b) - 1):
        if (i%4 == 0 and i != 0):
            c.create_line(100 + i*4, 505, 100 + i*4, 495, fill="#00e")
        c.create_line(99 + i*4, 490 - (b[i] - MM[0])/k, 99 + (i + 1)*4, 490 - (b[i + 1] - MM[0])/k,
                      fill="white")

    c.place(x=290, y=50)

    extr = extremal_values_BEST(b)
    TMP = define_trend(extr, b)
    text+="\n\nAverage increace coef:  " + str("%.4f"%TMP[0]) + "\n"
    text+="Average increace dist:  " + str("%.1f"%TMP[2]) + "\n\n"
    text+="Average decreace coef:  " + str("%.4f"%TMP[1]) + "\n"
    text+="Average decreace dist:  " + str("%.1f"%TMP[3]) + "\n\n"
    if(TMP[5] == -1):
        text+="Current trend is incresing for " + str(TMP[4]) + " day"
    if(TMP[5] == 1):
        text += "Current trend is decresing for " + str(TMP[4]) + " day"
    if(TMP[4] > 1): text+="s"
    Name.set(name[0])
    lb_name.pack()
    out.set(text)
    output.place(x=10, y=50, height=550, width=280)

root = Tk()
root.title("Stock expert")
root.geometry("1200x650")


#MENU
menu = Menu(font="Veranda 40", tearoff=0)

SubFile = Menu(tearoff=0)
SubFile.add_separator()
SubFile.add_command(label="Exit", command=exit, font="Veranda 10")

SubEdit = Menu(tearoff=0)
SubEdit.add_command(label="sart page", command=start_page, font="Veranda 10")

menu.add_cascade(label="File", font="Veranda 10", menu=SubFile)
menu.add_cascade(label="Edit", font="Veranda 10", menu=SubEdit)

root.config(menu=menu)


#LABELS
txt1 = "Welcome to the Stock expert!\n"
txt2 = "Choose your market"
out = StringVar()
Name = StringVar()
lb_main =           Label(text=txt1, justify=CENTER, font="Veranda 20")
lb =                Label(text=txt2, justify=CENTER, font="Veranda 15")
lb_stoc =           Label(text="Choose yor stock", font="Veranda 15")
lb_cryp =           Label(text="Choose yor crypto currency", font="Veranda 15")
lb_entr =           Label(text="Enter any symbol:", font="Veranda 15")
output =            Label(textvariable=out, font="Veranda 12", justify=LEFT)
lb_name =           Label(textvariable=Name, font="Veranda 15")


#BUTTONS
bt_cryp =           Button(text="Cryptocurrencies", font="Veranda 12", command=crypts)
bt_stoc =           Button(text="Stocks", font="Veranda 12", command=stocks)
bt_entr =           Button(text="Manual selection", font="Veranda 12", command=man_ent)
bt_choose_cryp =    Button(text="choose", font="Veranda 10", command=analysis)
bt_choose_stoc =    Button(text="choose", font="Veranda 10", command=analysis)
bt_choose_entr =    Button(text="search", font="Veranda 10", command=analysis)
bt_back_cryp =      Button(text="back", font="Veranda 10", command=crypts)
bt_back_stoc =      Button(text="back", font="Veranda 10", command=stocks)
bt_back_entr =      Button(text="back", font="Veranda 10", command=man_ent)
bt_back_start =     Button(text="back", font="Veranda 10", command=start_page)


#LISTS
scroll_stoc = Scrollbar(root)
list_stoc = Listbox(yscrollcommand=scroll_stoc.set, width=20)
for i in Stocks:
    list_stoc.insert(END, i)
scroll_stoc.config(command=list_stoc.yview)

scroll_cryp = Scrollbar(root)
list_cryp = Listbox(yscrollcommand=scroll_cryp.set, width=20)
for i in Crypts:
    list_cryp.insert(END, i)
scroll_cryp.config(command=list_cryp.yview)


#ENTRY
en_field = Entry()


#CANVAS
c = Canvas(root, height=550, width=900, bg="black")


start_page()

root.mainloop()
