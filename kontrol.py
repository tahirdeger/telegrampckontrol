import winreg
import os

def kontrol_et():
    print("🔍 Windows Başlangıç Kayıtları Kontrol Ediliyor...\n")
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Run",
                            0, winreg.KEY_READ)
        
        try:
            deger, tur = winreg.QueryValueEx(key, "PCControllerBot")
            print("✅ KAYIT BULUNDU!")
            print(f"📂 Kayıtlı Komut: {deger}")
            
            # Yolun doğruluğunu kontrol et
            temiz_yol = deger.replace('"', '').split('.exe"')[0] + '.exe'
            if "python" in temiz_yol.lower():
                # Python ile çalışıyorsa script yolunu bulmaya çalış (basit kontrol)
                print("ℹ️  Python yorumlayıcısı ile çalışıyor.")
            elif os.path.exists(temiz_yol):
                print("✅ Dosya belirtilen yolda mevcut.")
            else:
                print(f"⚠️  UYARI: Kayıtlı yoldaki dosya bulunamadı!\n    Aranan: {temiz_yol}")
                
        except FileNotFoundError:
            print("❌ KAYIT BULUNAMADI: 'PCControllerBot' adında bir kayıt yok.")
            
        winreg.CloseKey(key)
    except Exception as e:
        print(f"⚠️ Hata oluştu: {e}")

    input("\nÇıkmak için Enter'a basın...")

if __name__ == "__main__":
    kontrol_et()
