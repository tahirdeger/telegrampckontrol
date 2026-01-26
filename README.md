# 🖥️ Telegram PC Controller

Windows bilgisayarınızı Telegram üzerinden uzaktan kontrol etmenizi sağlayan, kullanıcı dostu arayüze (GUI) sahip Python tabanlı bir araç.

Bu proje ile bilgisayarınızın performansını izleyebilir, ekran görüntüsü alabilir, webcam'e erişebilir ve bilgisayarı uzaktan kapatabilirsiniz.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-win.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Özellikler

- **📊 Sistem Durumu:** CPU, RAM ve Disk kullanımını anlık görüntüleme.
- **📸 Ekran Görüntüsü:** Bilgisayarın o anki ekran görüntüsünü alıp Telegram'a gönderme.
- **📷 Webcam Erişimi:** Bağlı kameradan fotoğraf çekip gönderme.
- **💬 Çift Yönlü Sohbet:** Telegram'dan bilgisayara mesaj gönderme (veya tam tersi).
- **🔌 Güç Yönetimi:** Uzaktan bilgisayarı kapatma veya oturumu sonlandırma.
- **⚙️ Kolay Kurulum:** İlk açılışta çalışan "Kurulum Sihirbazı" ile kod bilgisi gerektirmeden ayar yapma.
- **🚀 Otomatik Başlatma:** Windows açılışında otomatik çalışma ve sistem tepsisine (System Tray) küçülme.
- **🔒 Güvenlik:** Sadece yetkilendirilmiş tek bir Telegram hesabı (Chat ID) komut gönderebilir.

## 🛠️ Kurulum

### 1. Projeyi İndirin

```bash
git clone https://github.com/KULLANICI_ADINIZ/telegram-pc-controller.git
cd telegram-pc-controller
```

### 2. Gereksinimleri Yükleyin

```bash
pip install -r requirements.txt
```

### 3. Uygulamayı Başlatın

```bash
python main.py
```

## ⚙️ Yapılandırma (İlk Kurulum)

Program ilk kez çalıştırıldığında **Kurulum Sihirbazı** otomatik olarak açılacaktır.

1. **Bot Token:** Telegram'da [@BotFather](https://t.me/botfather) üzerinden yeni bir bot oluşturun ve verilen Token'ı girin.
2. **Chat ID:** Oluşturduğunuz bota bir mesaj atın ve sihirbazdaki yönlendirmeyi kullanarak Chat ID'nizi öğrenip girin.
3. **Ayarlar:** Windows başlangıcında çalışma ayarlarını seçin.

> **Not:** Hassas bilgileriniz (`secret.json`) bilgisayarınızda yerel olarak saklanır ve GitHub'a yüklenmez.

## 📱 Kullanım (Telegram Komutları)

Botunuza aşağıdaki komutları gönderebilirsiniz:

| Komut | Açıklama |
|-------|----------|
| `/start` | Botu başlatır ve yardım menüsünü gösterir. |
| `/pcdurum` | İşlemci, RAM, Disk ve Uptime bilgilerini gösterir. |
| `/ekrangoruntu` | Bilgisayarın anlık ekran görüntüsünü çeker. |
| `/kameragoruntu` | Webcam'den fotoğraf çeker. |
| `/oturumkapat` | Mevcut Windows oturumunu kapatır. |
| `/pckapat` | Bilgisayarı tamamen kapatır. |

Ayrıca bot'a yazdığınız herhangi bir düz metin, bilgisayardaki uygulamanın "Sohbet" penceresinde görünür.

## 📦 EXE Oluşturma (Derleme)

Uygulamayı tek bir `.exe` dosyası haline getirmek için hazır script'i kullanabilirsiniz:

```bash
python build_exe.py
```

Bu işlem sonucunda `dist/` klasörü içinde taşınabilir `PCController.exe` dosyası oluşacaktır.

## 📂 Proje Yapısı

```
telegram-pc-controller/
├── main.py             # Uygulama giriş noktası
├── gui.py              # Grafik arayüz (Tkinter) kodları
├── bot_handler.py      # Telegram bot mantığı ve komutlar
├── system_control.py   # Sistem işlemleri (Screenshot, Shutdown vb.)
├── setup_wizard.py     # İlk kurulum sihirbazı
├── config.py           # Ayarlar ve sabitler
├── build_exe.py        # PyInstaller derleme aracı
├── requirements.txt    # Kütüphane listesi
└── secret.json         # (Otomatik oluşur) Token ve ID saklar
```

## 🤝 Katkıda Bulunma

1. Bu depoyu Fork'layın.
2. Yeni bir özellik dalı (branch) oluşturun (`git checkout -b yeni-ozellik`).
3. Değişikliklerinizi yapın ve Commit'leyin (`git commit -m 'Yeni özellik eklendi'`).
4. Dalınızı Push'layın (`git push origin yeni-ozellik`).
5. Bir Pull Request oluşturun.

## ⚠️ Yasal Uyarı

Bu yazılım sadece **kendi bilgisayarınızı** veya **izniniz olan cihazları** yönetmek için tasarlanmıştır. Başkalarının bilgisayarlarını izinsiz kontrol etmek yasalara aykırıdır ve etik değildir. Geliştirici, yazılımın kötüye kullanımından sorumlu tutulamaz.

## 

[https:// islematolyesi.odoo.com](https://islematolyesi.odoo.com/)

