
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog
from PIL import Image, ImageTk


#参照ボタン１のクリック時
def file_select():
    #ファイルダイアログから画像を選択
    idir = "image"
    global file_path
    file_path = tk.filedialog.askopenfilename(initialdir = idir)
    
    #キャンバス１に画像を表示
    global im
    read_img = Image.open(file_path)
    read_img = read_img.resize((150,150))
    im = ImageTk.PhotoImage(image=read_img)
    canvas_a.create_image(0,0, image = im, anchor = tk.NW)
    
    #画像ファイル名をエントリーに表示
    file_name = file_path[51:]
    entry_a.insert(tk.END, file_name)


#参照ボタン２のクリック時
def file_select2():
    #ファイルダイアログから画像を選択
    idir = "image"
    global file_path2
    file_path2 = tk.filedialog.askopenfilename(initialdir = idir)
    
    #キャンバス２に画像を表示
    global im2
    read_img2 = Image.open(file_path2)
    read_img2 = read_img2.resize((150,150))
    im2 = ImageTk.PhotoImage(image=read_img2)
    canvas_b.create_image(0,0, image = im2, anchor = tk.NW)
    
    #画像ファイル名をエントリーに表示
    file_name2 = file_path2[51:]
    entry_b.insert(tk.END, file_name2)


#実行ボタンのクリック時
def compair():
    import cv2

    #画像の読み込み※返り値ndarray配列
    image1 = cv2.imread(file_path)
    image2 = cv2.imread(file_path2)

    #画像リサイズ
    img_size = (100, 100)
    image1 = cv2.resize(image1, img_size)
    image2 = cv2.resize(image2, img_size)

    # 画像からヒストグラム計算
    image1_hist = cv2.calcHist([image1], [0], None, [256], [0, 256])
    image2_hist = cv2.calcHist([image2], [0], None, [256], [0, 256])

    # ヒストグラムした画像を比較,一致率(result)を算出
    orign = cv2.compareHist(image1_hist, image2_hist, 0)
    rounded = round(orign,3)
    result = '{:.1%}'.format(rounded)
    print(result)

    #一致率に応じて結果コメントを変更
    cm1 = '\n全く似ていません'
    cm2 = '\n似ているところもあります'
    cm3 = '\nそこそこ似ています'
    cm4 = '\nかなり似ています'
    cm5 = '\n非常によく似ています'
    cm6 = '\n完全に一致しています'

    if rounded < 0.40:
        gouhi = str(result).rjust(20) + cm1.center(20)
    elif rounded < 0.65:
        gouhi = str(result).rjust(20) + cm2.center(20)
    elif rounded < 0.80:
        gouhi = str(result).rjust(20) + cm3.center(20)
    elif rounded < 0.95:
        gouhi = str(result).rjust(20) + cm4.center(20)
    elif rounded < 1.00:
        gouhi = str(result).rjust(20) + cm5.center(20)
    else:
        gouhi = str(result).rjust(20) + cm6.center(20)
    
    #結果テキストを反映
    print(gouhi)
    final["text"] = gouhi



#---tkinterとttkを使ってGUIを作成---

# rootメインウィンドウを設定
root = tk.Tk()
root.title("ヒストグラムで画像を比較")
root.geometry("600x450")


#3つのフレームを作成,gridで配置
# メインフレーム1
frame1 = ttk.Frame(root)
frame1.grid(column=0, row=0, padx=5, pady=10)
# サブフレーム2(画像表示用)
frame2 = ttk.Frame(root)
frame2.grid(column=0, row=2)
# メインフレーム3
frame3 = ttk.Frame(root, width = 550, height = 300)
frame3.grid(row=3, padx=5, pady=3)


# 各フレーム上に各種ウィジェットの作成,配置
#メインフレーム1へ
dai = ttk.Label(frame1, text="二枚の画像の一致率は何％？ ",font=5)
label_a = ttk.Label(frame1, text="♦ 一枚目の画像",font=30)
file_a = ttk.Label(frame1, text="  ファイルを指定：  ")
entry_a = ttk.Entry(frame1)
button_a = ttk.Button(frame1, text="参照",command=file_select)
space = ttk.Label(frame1, text="--------")
label_b = ttk.Label(frame1, text="♦ 二枚目の画像",font=30)
file_b = ttk.Label(frame1, text="  ファイルを指定：  ")
entry_b = ttk.Entry(frame1)
button_b = ttk.Button(frame1, text="参照",command=file_select2)

#gridでウィジェットを配置
dai.grid(row=0, column=1)
label_a.grid(row=1, column=1)
file_a.grid(row=1, column=2)
entry_a.grid(row=1, column=3)
button_a.grid(row=1, column=4)
space.grid(row=2, column=2)
label_b.grid(row=3, column=1)
file_b.grid(row=3, column=2)
entry_b.grid(row=3, column=3)
button_b.grid(row=3, column=4)

# サブフレーム2へ,配置はpack
canvas_a = tk.Canvas(frame2, width = 150, height = 150, bg = "gray")
canvas_a.pack(side = tkinter.LEFT, padx = 40)
canvas_b = tk.Canvas(frame2, width = 150, height = 150, bg = "gray")
canvas_b.pack(side = tkinter.LEFT)

# メインフレーム3へ
style = ttk.Style()
style.configure("execute.TButton", font = ("", 14),)
button_execute = ttk.Button(frame3, text="一致率を算出",style = "execute.TButton",command=compair)
final = ttk.Label(frame3,text="",font=("MSゴシック","25","bold"))

#placeでウィジェットの配置
button_execute.place(x = 230, y = 15, width = 130, height = 50)
final.place(x = 115, y = 70, width = 500, height = 80)



root.mainloop()











