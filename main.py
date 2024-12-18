import instaloader
import os
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import re
from threading import Thread

# Instagram video indirme fonksiyonu
class InstagramDownloader:
    def __init__(self, urls, download_folder, progress_var, progress_max):
        self.urls = urls
        self.download_folder = download_folder
        self.progress_var = progress_var
        self.progress_max = progress_max
        self.L = instaloader.Instaloader()

    def download_video(self, url):
        try:
            # URL'den shortcode'yi çıkartıyoruz
            shortcode = url.split("/")[-2]
            post = instaloader.Post.from_shortcode(self.L.context, shortcode)
            
            if post.is_video:
                target_folder = os.path.join(self.download_folder, f"{post.owner_username}_video")
                
                # Klasör varsa, bir sonraki videoyu aynı isimle kaydedebilmek için benzersiz bir isim oluşturuluyor
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)

                # Videoyu indir
                self.L.download_post(post, target=target_folder)

                # İlerleme çubuğunun güncellenmesi
                self.progress_var.set(self.progress_var.get() + 1)
                root.update_idletasks()

                print(f"Video başarıyla indirildi: {target_folder}")
            else:
                print(f"{url}: Bu içerik bir video değil.")
        except Exception as e:
            print(f"{url}: Hata oluştu: {e}")
            messagebox.showerror("İndirme Hatası", f"{url} adresindeki video indirilemedi!\nHata: {e}")
    
    def download_videos(self):
        for url in self.urls:
            self.download_video(url)
        
        messagebox.showinfo("Başarı", "Videolar başarıyla indirildi!")


# URL'yi doğrulama ve filtreleme fonksiyonu
def validate_urls(input_text):
    url_pattern = r'https?://(www\.)?instagram\.com/(p|reel)/[A-Za-z0-9_-]+/?'
    urls = input_text.strip().splitlines()
    valid_urls = []

    for url in urls:
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
    input_text = entry_urls.get("1.0", tk.END)
    
    urls = validate_urls(input_text)
    if not urls:
        messagebox.showerror("Hata", "Lütfen geçerli Instagram video URL'leri girin!")
        return

    download_folder = choose_download_folder()
    if not download_folder:
        return

    downloader = InstagramDownloader(urls, download_folder, progress_var, progress_max)
    
    # İndirme işlemi için ayrı bir thread başlatıyoruz, UI'yi donmaktan korur
    download_thread = Thread(target=downloader.download_videos)
    download_thread.start()


# GUI (Form) oluşturma
root = tk.Tk()
root.title("Instagram Video İndirme Aracı")
root.geometry("600x700")  # Daha geniş bir pencere

# URL'ler için etiket
label_urls = tk.Label(root, text="Instagram Video URL'lerini Girin (Her bir URL yeni bir satıra):")
label_urls.pack(pady=15)

# URL'leri girebilmek için metin kutusu
entry_urls = tk.Text(root, height=10, width=60)
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
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=progress_max.get(), length=500)
progress_bar.pack(pady=15)

# İndirme butonu
download_button = tk.Button(root, text="Videoları İndir", command=start_download, height=2, width=20)
download_button.pack(pady=20)

# Footer ekleniyor
footer_label = tk.Label(root, text="Uğurcan Yaş ürünüdür", font=("Helvetica", 10, "italic"), fg="gray")
footer_label.pack(side="bottom", pady=10)

# Uygulamanın ana döngüsünü başlatma
root.mainloop()
