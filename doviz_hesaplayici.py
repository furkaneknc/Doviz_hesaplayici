import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox


def fiyatlari_getir():
    url = 'https://bigpara.hurriyet.com.tr/doviz'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content,'html.parser') 
        ul_list = soup.find_all('ul',style = True ) 
        fiyatlar =  []
        for ul in ul_list:
            doviz_cinsi_element = ul.find('li',class_ = 'cell010 tal')
            if doviz_cinsi_element: 
                doviz_cinsi = doviz_cinsi_element.text.strip()
                satis_fiyati_element = ul.find_all('li',class_= 'cell015')
                if satis_fiyati_element and len(satis_fiyati_element) > 1: 
                    satis_fiyatı= float(satis_fiyati_element[1].text.strip().replace(',','.')) 
                    fiyatlar.append((doviz_cinsi,satis_fiyatı))
        return fiyatlar
    
    else:
        messagebox.showerror("Hata","Döviz fiyatları çekilemedi")
        return None
    

def hesapla():
    try:
        tl_miktari = float(entry_yatirim.get())
        fiyatlar = fiyatlari_getir()

        if fiyatlar:
            for widget in result_canvas_frame.winfo_children(): 
                widget.destroy()#tasarım alanındaki oncekı tum cocukları(veriler) temizliyorum
            for i, (doviz_cinsi , satis_fiyati) in enumerate(fiyatlar):
                alinabilecek_miktar = tl_miktari/satis_fiyati

                doviz_label = tk.Label(result_canvas_frame , text=doviz_cinsi , font=("Arial",12), anchor="w")
                doviz_label.grid(row=i,column=0,padx=10,pady=5,sticky="e")

                miktar_label = tk.Label(result_canvas_frame,text=f"{alinabilecek_miktar:.2f}",font=("Arial",12),anchor="e")
                miktar_label.grid(row=i , column=1,padx=10,pady=5,sticky="e")
            
            #scroll ayarları
            result_canvas.update_idletasks()
            result_canvas.config(scrollregion=result_canvas.bbox("all"))
    
    except ValueError:
        messagebox.showerror("Hata","Lütfen Geçerli Bir TL Miktarı Giriniz.")

#TKİNTER Arayüzü
root = tk.Tk()
root.title("Döviz Hesaplayıcı")
root.geometry("600x500")
root.config(bg='#e6e6fa')

#baslık
title_label = tk.Label(root, text="Döviz Hesaplayıcısı",font=("Arial", 24 ,"bold"),bg="#e6e6fa")
title_label.pack(pady=20)

#yatırım miktarı girişi
entry_frame = tk.Frame(root,bg="#e6e6fa")
entry_frame.pack(pady=10)

entry_label=tk.Label(entry_frame, text="Yatırım Miktarı (TL): ", font=("Arial",14),bg="#e6e6fa")
entry_label.grid(row=0,column=0,padx=0)

entry_yatirim = tk.Entry(entry_frame, font=("Arial",14),width=10)
entry_yatirim.grid(row=0,column=1,padx=5)


#hesapla butonu
calculate_button = tk.Button(root, text="Hesapla",font=("Arial",14),command=hesapla ,bg="#4CAF50",fg="white")
calculate_button.pack(pady=20)

#sonuclar icin frame olustur 
result_frame = tk.Frame(root,bg="#f0f0f0",bd=2,relief="solid")
result_frame.pack(pady=10,fill="both")

#canvası ekliyorum
#Altta yaptıklarımla verileri frame içine gömücem
result_canvas = tk.Canvas(result_frame,bg="#f0f0f0")
result_canvas.pack(side="left",fill="both",expand=True)

#scroll bar ekliyorum
scrollbar = tk.Scrollbar(result_frame, orient="vertical",command=result_canvas.yview) 
scrollbar.pack(side="right",fill="y") 

#scrollbar'ı canvasa ekle
result_canvas.configure(yscrollcommand=scrollbar.set)
result_canvas_frame = tk.Frame(result_canvas, bg="#f0f0f0")
result_canvas.create_window((0,0),window=result_canvas_frame,anchor="nw")


root.mainloop()