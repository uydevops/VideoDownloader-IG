import instaloader
import os
import tkinter as tk
from tkinter import messagebox, filedialog
import re
from tkinter import ttk

# Instagram video indirme fonksiyonu
def download_instagram_video(url, L, download_folder, progress_var, progress_max):
    try:
        # URL'den shortcode'yi çıkartıyoruz
        shortcode = url.split("/")[-2]
        
        # Postu al
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        if post.is_video:
            # Videoyu indir
            target_folder = os.path.join(download_folder, f"{post.owner_username}_video")
            # Klasör varsa, bir sonraki videoyu aynı isimle kaydedebilmek için benzersiz bir isim oluşturuluyor
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
            
            # Videoyu indir
            L.download_post(post, target=target_folder)
            
            # İlerleme çubuğunun güncellenmesi
            progress_var.set(progress_var.get() + 1)
            root.update_idletasks()

            print(f"Video başarıyla indirildi: {target_folder}")
        else:
            print(f"{url}: Bu içerik bir video değil.")
    except Exception as e:
        print(f"{url}: Hata oluştu: {e}")
        messagebox.showerror("İndirme Hatası", f"{url} adresindeki video indirilemedi!\nHata: {e}")

# Birden fazla video indirme fonksiyonu
def download_multiple_videos(urls, download_folder):
    L = instaloader.Instaloader()

    # Toplam video sayısını hesaplayıp ilerleme çubuğunu ayarlıyoruz
    progress_max.set(len(urls))  # Maksimum ilerleme değeri, video sayısına göre ayarlanır
    
    # URL'ler üzerinde döngü
    for url in urls:
        download_instagram_video(url, L, download_folder, progress_var, progress_max)

    messagebox.showinfo("Başarı", "Videolar başarıyla indirildi!")

# URL'yi doğrulama ve filtreleme fonksiyonu
def validate_urls(input_text):
    # Instagram URL'leri için regex deseni
    url_pattern = r'https?://(www\.)?instagram\.com/(p|reel)/[A-Za-z0-9_-]+/?'
    
    urls = input_text.strip().splitlines()
    valid_urls = []
    
    for url in urls:
        # URL'yi kontrol et
        if re.match(url_pattern, url):
            valid_urls.append(url)
        else:
            print(f"Geçersiz URL: {url}")
    
    return valid_urls

# Dosya yolu seçici fonksiyonu
def choose_download_folder():
    folder = filedialog.askdirectory()  # Klasör seçme penceresi
    if folder:
        folder_label.config(text=f"İndirilecek Klasör: {folder}")
    return folder

# İndirme işlemi başlatma fonksiyonu
def start_download():
    # URL'leri al
    input_text = entry_urls.get("1.0", tk.END)
    
    # Geçerli URL'leri doğrula
    urls = validate_urls(input_text)
    
    if not urls:
        messagebox.showerror("Hata", "Lütfen geçerli Instagram video URL'leri girin!")
        return
    
    # Kullanıcıya hangi klasöre kaydedeceğini sor
    download_folder = choose_download_folder()
    if not download_folder:
        return

    # Videoları indir
    download_multiple_videos(urls, download_folder)

# GUI (Form) oluşturma
root = tk.Tk()
root.title("Instagram Video İndirme Aracı")
root.geometry("500x600")  # Uygulama boyutu

# URL'ler için etiket
label_urls = tk.Label(root, text="Instagram Video URL'lerini Girin (Her bir URL yeni bir satıra):")
label_urls.pack(pady=10)

# URL'leri girebilmek için metin kutusu
entry_urls = tk.Text(root, height=10, width=50)
entry_urls.pack(pady=10)

# Klasör seçim butonu
choose_folder_button = tk.Button(root, text="İndirilecek Klasörü Seç", command=choose_download_folder)
choose_folder_button.pack(pady=10)

# Klasör yolu etiketi
folder_label = tk.Label(root, text="İndirilecek Klasör: Seçili değil")
folder_label.pack(pady=10)

# İlerleme çubuğu
progress_var = tk.DoubleVar()
progress_max = tk.IntVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=progress_max.get(), length=400)
progress_bar.pack(pady=10)

# İndirme butonu
download_button = tk.Button(root, text="Videoları İndir", command=start_download)
download_button.pack(pady=20)

# Footer ekleniyor
footer_label = tk.Label(root, text="Uğurcan Yaş ürünüdür", font=("Helvetica", 10, "italic"), fg="gray")
footer_label.pack(side="bottom", pady=10)

# Uygulamanın ana döngüsünü başlatma
root.mainloop()


