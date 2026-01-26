"""
PC Controller - EXE Oluşturma Script'i (Güncel sürüm)
PyInstaller ile tek dosya EXE oluşturur.
"""

import os
import sys
import subprocess
import shutil


def check_requirements():
    """Gerekli modülleri kontrol eder"""
    print("=" * 60)
    print("EXE OLUŞTURMA - Gereksinim Kontrolü")
    print("=" * 60)
    print()

    required_modules = [
        'telegram',
        'PIL',
        'psutil',
        'pystray',
        'PyInstaller',
        'cv2',  # opencv-python (import adı cv2'dir)
        'plyer'
    ]

    missing = []

    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module} yüklü")
        except ImportError:
            print(f"✗ {module} eksik")
            missing.append(module)

    print()

    if missing:
        print("❌ Eksik modüller bulundu!")
        print("\nYüklemek için:")
        print("pip install -r requirements.txt")
        return False

    print("✅ Tüm modüller yüklü!")
    return True


def clean_previous_builds():
    """Önceki derleme dosyalarını temizler"""
    print("\n" + "=" * 60)
    print("🧹 Önceki Derlemeler Temizleniyor")
    print("=" * 60)
    print()

    folders_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['*.spec']

    for folder in folders_to_clean:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"✓ {folder}/ klasörü silindi")

    for pattern in files_to_clean:
        import glob
        for file in glob.glob(pattern):
            os.remove(file)
            print(f"✓ {file} silindi")

    print("\n✅ Temizlik tamamlandı!")


def create_icon():
    """Basit bir ikon oluşturur"""
    try:
        from PIL import Image, ImageDraw

        print("\n" + "=" * 60)
        print("🎨 İkon Oluşturuluyor")
        print("=" * 60)
        print()

        size = 256
        image = Image.new('RGB', (size, size), color=(0, 120, 215))
        draw = ImageDraw.Draw(image)

        margin = size // 4
        draw.rectangle([margin, margin, size - margin, size - margin],
                       fill=(255, 255, 255))
        screen_margin = size // 3
        draw.rectangle([screen_margin, screen_margin,
                        size - screen_margin, size - screen_margin - 20],
                       fill=(0, 120, 215))

        image.save('app_icon.ico', format='ICO')
        print("✓ app_icon.ico oluşturuldu")
        return True

    except Exception as e:
        print(f"⚠ İkon oluşturulamadı: {e}")
        print("  (İkon olmadan devam ediliyor)")
        return False


def build_exe():
    """PyInstaller ile EXE oluşturur (Spec dosyası kullanarak)"""
    print("\n" + "=" * 60)
    print("🚀 EXE OLUŞTURULUYOR (Spec Dosyası ile)")
    print("=" * 60)
    print()

    # Spec dosyası içeriği
    spec_content = """# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

# Ek dosyalar (Dosya, Hedef)
added_files = [
    ('config.py', '.')
]

# secret.json varsa ekle (yoksa program ilk açılışta oluşturur)
if os.path.exists('secret.json'):
    added_files.append(('secret.json', '.'))

# shots klasörü varsa ekle
if os.path.exists('shots'):
    added_files.append(('shots', 'shots'))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'telegram',
        'telegram.ext',
        'PIL._tkinter_finder',
        'pystray._win32',
        'plyer',
        'cv2',
        'asyncio',
        'tkinter'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PCController',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico' if os.path.exists('app_icon.ico') else None,
)
"""

    print("📝 PCController.spec dosyası oluşturuluyor...")
    try:
        with open('PCController.spec', 'w', encoding='utf-8') as f:
            f.write(spec_content)
        print("✓ Spec dosyası hazır.")
    except Exception as e:
        print(f"❌ Spec dosyası yazılamadı: {e}")
        return False

    cmd = ['pyinstaller', 'PCController.spec', '--clean']

    print("🧱 PyInstaller çalıştırılıyor...")
    print(" ".join(cmd))
    print("\nDerleme başlıyor... (Bu birkaç dakika sürebilir)\n")

    try:
        result = subprocess.run(cmd, check=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                text=True)
        print(result.stdout)
        print("✅ Derleme başarıyla tamamlandı!\n")
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Derleme hatası!")
        print(e.stdout)
        return False


def copy_config():
    """config.py dosyasını dist klasörüne kopyalar"""
    print("\n" + "=" * 60)
    print("⚙️ Yapılandırma Dosyası Kopyalanıyor")
    print("=" * 60)
    print()

    if not os.path.exists('dist'):
        print("⚠ dist/ klasörü bulunamadı!")
        return False

    try:
        shutil.copy('config.py', 'dist/config.py')
        print("✓ config.py → dist/config.py kopyalandı")
        return True
    except Exception as e:
        print(f"❌ Kopyalama hatası: {e}")
        return False


def create_readme():
    """Dist klasörüne README.txt oluşturur"""
    print("\n" + "=" * 60)
    print("📄 README Dosyası Oluşturuluyor")
    print("=" * 60)
    print()

    try:
        with open('dist/README.txt', 'w', encoding='utf-8') as f:
            f.write("Telegram PC Controller\n\nKullanım: PCController.exe\n"
                    "Bu program Telegram üzerinden bilgisayarınızı kontrol etmenizi sağlar.\n")
        print("✓ README.txt oluşturuldu")
        return True
    except Exception as e:
        print(f"❌ README oluşturulamadı: {e}")
        return False


def final_summary():
    """Derleme özeti"""
    print("\n" + "=" * 60)
    print("✅ DERLEME TAMAMLANDI")
    print("=" * 60)
    print("📂 Dosyalar dist/ klasöründe")
    print("\n   - PCController.exe\n   - config.py\n   - README.txt\n")
    exe_path = 'dist/PCController.exe'
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"💾 EXE Boyutu: {size_mb:.2f} MB\n")


def main():
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "PC CONTROLLER - EXE BUILDER" + " " * 20 + "║")
    print("╚" + "═" * 58 + "╝")
    print()

    if not check_requirements():
        input("\nEnter'a basarak çıkın...")
        return

    clean_previous_builds()
    create_icon()

    if not build_exe():
        print("\n❌ Derleme başarısız!")
        input("\nEnter'a basarak çıkın...")
        return

    copy_config()
    create_readme()
    final_summary()

    print("🎯 dist klasörünü istediğin yere taşıyabilirsin.")
    input("\nTamamlamak için Enter'a basın...")


if __name__ == "__main__":
    main()
