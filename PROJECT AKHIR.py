import json
import datetime
import pwinput
from prettytable import PrettyTable
import time
import os
from colorama import Fore



FILE_WISATA = "wisata.json"
FILE_USER = "akun.json"
FILE_TRANSAKSI = "transaksi.json"



#clear gunanya saat selesai input langsung bersih
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def ensure_files_exist():
    
    if not os.path.exists(FILE_WISATA):
        with open(FILE_WISATA, "w") as f:
            json.dump([], f, indent=4)
    
    if not os.path.exists(FILE_USER):
        with open(FILE_USER, "w") as f:
            json.dump({}, f, indent=4)
    
    if not os.path.exists(FILE_TRANSAKSI):
        with open(FILE_TRANSAKSI, "w") as f:
            json.dump([], f, indent=4)

#membaca Json
def baca_json(nama):
    """Baca file json, kembalikan struktur default kalau error."""
    try:
        with open(nama, "r") as f:
            return json.load(f)
    except Exception:
        if nama == FILE_USER:
            return {}
        else:
            return []

#simpan wisata
def simpan_json(nama, data):
    with open(nama, "w") as f:
        json.dump(data, f, indent=4)

def loading_dan_delay(msg="Mengecek", dots=3, delay=0.4):
    print(msg, end="")
    for _ in range(dots):
        print(".", end="", flush=True)
        time.sleep(delay)
    print()


def pilihan_kembali_menu():
    print()
    print("[1] Kembali ke menu")
    print("[2] lanjutkan aksi")
    pilih = input("Pilih: ").strip()
    return pilih == "2"

#wisata di tampilkan
def tampilkan_wisata():
    clear()
    wisata = baca_json(FILE_WISATA)
    if not wisata:
        print("Belum ada data wisata.\n")
        return
    tbl = PrettyTable(["No", "Nama Wisata", "Lokasi", "Tahun", "Harga Tiket"])
    for i, w in enumerate(wisata, 1):
        tbl.add_row([i, w.get("nama_wisata", "-"), w.get("lokasi", "-"), w.get("tahun", "-"), f"Rp{w.get('harga_tiket', 0):,}"])
    print(tbl)
    print()
    

#Menambahkan Wisata
def tambah_wisata():
    while True:
        clear()
        data = baca_json(FILE_WISATA)
        print("=== TAMBAH WISATA ===")
        nama = input("Nama wisata: ").strip()
        lokasi = input("Lokasi: ").strip()
        try:
            tahun = int(input("Tahun berdiri: ").strip())
            harga = int(input("Harga tiket (angka): ").strip())
            data.append({"nama_wisata": nama, "lokasi": lokasi, "tahun": tahun, "harga_tiket": harga})
            simpan_json(FILE_WISATA, data)
            print("\n Data berhasil ditambah.\n")
        except Exception:
            print("\n Tahun dan harga harus angka. Data tidak disimpan.\n")
        if not pilihan_kembali_menu():
            return

#mengubah wisata
def ubah_wisata():
    while True:
        clear()
        data = baca_json(FILE_WISATA)
        if not data:
            print("Belum ada data wisata.\n")
            return
        print("=== UBAH WISATA ===\n")
        tbl = PrettyTable(["No", "Nama Wisata", "Lokasi", "Tahun", "Harga Tiket"])
        for i, w in enumerate(data, 1):
            tbl.add_row([i, w.get("nama_wisata", "-"), w.get("lokasi", "-"), w.get("tahun", "-"), f"Rp{w.get('harga_tiket', 0):,}"])
        print(tbl)
        print()
        nama = input("Masukkan nama wisata yang mau diubah: ").strip()
        found = False
        for w in data:
            if w.get("nama_wisata", "").lower() == nama.lower():
                found = True
                print("\nData ditemukan. Kosongkan input untuk tidak mengubah field tersebut.")
                new_nama = input(f"Nama baru [{w['nama_wisata']}]: ").strip() or w["nama_wisata"]
                new_lokasi = input(f"Lokasi baru [{w['lokasi']}]: ").strip() or w["lokasi"]
                try:
                    t = input(f"Tahun baru [{w['tahun']}]: ").strip()
                    if t:
                        t = int(t)
                    else:
                        t = w['tahun']
                    h = input(f"Harga baru [{w['harga_tiket']}]: ").strip()
                    if h:
                        h = int(h)
                    else:
                        h = w['harga_tiket']
                except Exception:
                    print("\nTahun/harga harus angka. Perubahan dibatalkan untuk item ini.\n")
                    break
                w["nama_wisata"] = new_nama
                w["lokasi"] = new_lokasi
                w["tahun"] = t
                w["harga_tiket"] = h
                simpan_json(FILE_WISATA, data)
                print("\n Data berhasil diperbarui.\n")
                break
        if not found:
            print("\n Nama wisata tidak ditemukan.\n")
        if not pilihan_kembali_menu():
            return

#hapus wisata
def hapus_wisata():
    while True:
        clear()
        data = baca_json(FILE_WISATA)
        if not data:
            print("Belum ada data wisata.\n")
            return
        print("=== HAPUS WISATA ===\n")
        tbl = PrettyTable(["No", "Nama Wisata", "Lokasi", "Tahun", "Harga Tiket"])
        for i, w in enumerate(data, 1):
            tbl.add_row([i, w.get("nama_wisata", "-"), w.get("lokasi", "-"), w.get("tahun", "-"), f"Rp{w.get('harga_tiket', 0):,}"])
        print(tbl)
        print()
        nama = input("Masukkan nama wisata yang mau dihapus: ").strip()
        baru = [w for w in data if w.get("nama_wisata", "").lower() != nama.lower()]
        if len(baru) != len(data):
            konfirmasi = input(f"Yakin ingin menghapus '{nama}'? (y/n): ").strip().lower()
            if konfirmasi == "y":
                simpan_json(FILE_WISATA, baru)
                print("\n Data berhasil dihapus.\n")
            else:
                print("\nDibatalkan.\n")
        else:
            print("\n Nama wisata tidak ditemukan.\n")
        if not pilihan_kembali_menu():
            return

#mencari wisata
def cari_wisata():
    while True:
        clear()
        data = baca_json(FILE_WISATA)
        if not data:
            print("Belum ada data wisata.\n")
            return
        print("=== CARI WISATA ===\n")
        keyword = input("Masukkan kata kunci nama/lokasi: ").strip().lower()
        hasil = [w for w in data if keyword in w.get("nama_wisata", "").lower() or keyword in w.get("lokasi", "").lower()]
        if hasil:
            tbl = PrettyTable(["No", "Nama Wisata", "Lokasi", "Tahun", "Harga Tiket"])
            for i, w in enumerate(hasil, 1):
                tbl.add_row([i, w.get("nama_wisata", "-"), w.get("lokasi", "-"), w.get("tahun", "-"), f"Rp{w.get('harga_tiket', 0):,}"])
            print(tbl)
        else:
            print("\n Data tidak ditemukan.\n")
        if not pilihan_kembali_menu():
            return

#REgristrasi akun
def daftar_akun():
    clear()
    print("=== REGISTRASI AKUN USER ===")
    users = baca_json(FILE_USER)

    username = input("Masukkan username baru: ").strip()
    if username in users:
        print("Username sudah terdaftar!\n")
        return

    password = pwinput.pwinput("Masukkan password: ").strip()
    users[username] = {
        "password": password,
        "role": "User",
        "saldo": 0
    }

    simpan_json(FILE_USER, users)
    print("\nAkun berhasil!\n")
    time.sleep(1)

#masukkan user/admin
def login(role_login):
    clear()
    users = baca_json(FILE_USER)
    print(f"\n=== LOGIN SEBAGAI {role_login.upper()} ===")
    user = input("Username: ").strip()
    pw = pwinput.pwinput("Password: ")
    loading_dan_delay("Mengecek akun", dots=3, delay=0.3)
    if user in users and users[user]["password"] == pw:
        if users[user]["role"].lower() == role_login.lower():
            print(f"\n Login berhasil sebagai {users[user]['role']}.\n")
            return user
        else:
            print("\n Role akun tidak sesuai.\n")
    else:
        print("\n Login gagal, periksa kembali username/password.\n")
    return None

#menghapus akun
def hapus_akun():
    while True:
        clear()
        users = baca_json(FILE_USER)
        if not users:
            print("Belum ada akun.\n")
            return
        print("=== HAPUS AKUN ===\n")
        tampil = PrettyTable(["No", "Username", "Role", "Saldo"])
        for i, (u, d) in enumerate(users.items(), 1):
            tampil.add_row([i, u, d.get("role", "-"), f"Rp{d.get('saldo', 0):,}"])
        print(tampil)
        print()
        target = input("Masukkan username akun yang ingin dihapus: ").strip()
        if target in users:
            konfirmasi = input(f"Yakin ingin menghapus akun '{target}'? (y/n): ").strip().lower()
            if konfirmasi == "y":
                del users[target]
                simpan_json(FILE_USER, users)
                print("\n Akun berhasil dihapus.\n")
            else:
                print("\nDibatalkan.\n")
        else:
            print("\n Username tidak ditemukan.\n")
        if not pilihan_kembali_menu():
            return

#Top up min 10.000 Max 2.000.000
def topup(username):
    while True:
        clear()
        users = baca_json(FILE_USER)
        if username not in users:
            print("Akun tidak ditemukan.\n")
            return
        print("=== TOP UP SALDO ===\n")
        try:
            nominal = int(input("Masukkan nominal top up (min Rp10.000, max Rp2.000.000): ").strip())
            if nominal < 10000:
                print(" Minimal top up Rp10.000.\n")
            elif nominal > 2000000:
                print(" Maksimal top up Rp2.000.000.\n")
            else:
                users[username]["saldo"] += nominal
                simpan_json(FILE_USER, users)
                print(f"\n Top up berhasil! Saldo sekarang: Rp{users[username]['saldo']:,}\n")
        except Exception:
            print("\n Nominal harus berupa angka.\n")
        if not pilihan_kembali_menu():
            return

#beli tiket sesuai saldo
def beli_tiket(username):
    while True:
        clear()
        wisata = baca_json(FILE_WISATA)
        users = baca_json(FILE_USER)
        transaksi = baca_json(FILE_TRANSAKSI)
        if username not in users:
            print("Akun tidak ditemukan.\n")
            return
        if not wisata:
            print("Belum ada data wisata.\n")
            return
        print("=== BELI TIKET ===\n")

        tbl = PrettyTable(["No", "Nama Wisata", "Lokasi", "Harga Tiket"])
        for i, w in enumerate(wisata, 1):
            tbl.add_row([i, w.get("nama_wisata", "-"), w.get("lokasi", "-"), f"Rp{w.get('harga_tiket', 0):,}"])
        print(tbl)
        print()
        nama = input("Masukkan nama wisata yang ingin dikunjungi: ").strip()
        for w in wisata:
            if w.get("nama_wisata", "").lower() == nama.lower():
                harga = w.get("harga_tiket", 0)
                saldo = users[username].get("saldo", 0)
                try:
                    jumlah = int(input("Masukkan jumlah tiket: ").strip())
                    if jumlah <= 0:
                        print("\n Jumlah tiket harus lebih dari 0.\n")
                        break
                except Exception:
                    print("\n Jumlah tiket harus angka.\n")
                    break
                total = harga * jumlah
                if saldo < total:
                    print(f"\n Saldo tidak cukup. Saldo: Rp{saldo:,}, Total: Rp{total:,}\n")
                    break
                
                users[username]["saldo"] -= total
                simpan_json(FILE_USER, users)
                
                transaksi.append({
                    "username": username,
                    "nama_wisata": w.get("nama_wisata"),
                    "harga_satuan": harga,
                    "jumlah_tiket": jumlah,
                    "total_harga": total,
                    "tanggal": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                simpan_json(FILE_TRANSAKSI, transaksi)
                
                print("\n=== INVOICE PEMBELIAN ===")
                print(f"Nama Pembeli  : {username}")
                print(f"Nama Wisata   : {w.get('nama_wisata')}")
                print(f"Harga Satuan  : Rp{harga:,}")
                print(f"Jumlah Tiket  : {jumlah}")
                print(f"Total Bayar   : Rp{total:,}")
                print(f"Tanggal       : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Sisa Saldo    : Rp{users[username]['saldo']:,}")
                print("==========================================\n")
                break
        else:
            print("\n Nama wisata tidak ditemukan.\n")
        if not pilihan_kembali_menu():
            return

#riwayat tranksaksi tiket yang sudah kita beli
def riwayat_transaksi(username):
    while True:
        clear()
        transaksi = baca_json(FILE_TRANSAKSI)
        data_user = [t for t in transaksi if t.get("username") == username]
        if not data_user:
            print("Belum ada transaksi.\n")
            return
        tbl = PrettyTable(["No", "Nama Wisata", "Harga Satuan", "Jumlah", "Total", "Tanggal"])
        for i, t in enumerate(data_user, 1):
            tbl.add_row([
                i,
                t.get("nama_wisata", "-"),
                f"Rp{t.get('harga_satuan', 0):,}",
                t.get("jumlah_tiket", 0),
                f"Rp{t.get('total_harga', 0):,}",
                t.get("tanggal", "-")
            ])
        print("============================================================")
        print("|                                                          |")
        print("|                  RIWAYAT TRANSAKSI                       |")
        print("|                                                          |")
        print("============================================================")
        print(tbl)
        print()
        if not pilihan_kembali_menu():
            return

#laporan seberapa banyak seluruh user beli tiket
def laporan_transaksi():
    while True:
        clear()
        transaksi = baca_json(FILE_TRANSAKSI)
        if not transaksi:
            print("Belum ada transaksi yang tercatat.\n")
            return
        total = sum(t.get("total_harga", 0) for t in transaksi)
        print("============================================================")
        print("|                                                          |")
        print("|                 LAPORAN PENJUALAN TIKET                  |")
        print("|                                                          |")
        print("============================================================")
        print(f"Total Transaksi : {len(transaksi)} kali")
        print(f"Total Pendapatan: Rp{total:,}\n")
        
        summary = {}
        for t in transaksi:
            key = t.get("nama_wisata", "Unknown")
            summary.setdefault(key, 0)
            summary[key] += t.get("total_harga", 0)
        print("Pendapatan per Wisata:")
        tbl = PrettyTable(["Nama Wisata", "Pendapatan"])
        for k, v in summary.items():
            tbl.add_row([k, f"Rp{v:,}"])
        print(tbl)
        if not pilihan_kembali_menu():
            return

#menu admin ada 8 plihsn
def menu_admin(username):
    while True:
        print("============================================================")
        print("|                                                          |")
        print("|                     MENU ADMIN                           |")
        print("|                                                          |")
        print("============================================================")
        print("[1]. Lihat wisata")
        print("[2]. Tambah wisata")
        print("[3]. Ubah wisata")
        print("[4]. Hapus wisata")
        print("[5]. Cari wisata")
        print("[6]. Laporan transaksi")
        print("[7]. Hapus akun")
        print("[8]. Logout")
        pilih = input("Pilih: ").strip()
        if pilih == "1":
            
            while True:
                clear()
                tampilkan_wisata()
                if not pilihan_kembali_menu():
                    break
        elif pilih == "2":
            tambah_wisata()
        elif pilih == "3":
            ubah_wisata()
        elif pilih == "4":
            hapus_wisata()
        elif pilih == "5":
            cari_wisata()
        elif pilih == "6":
            laporan_transaksi()
        elif pilih == "7":
            hapus_akun()
        elif pilih == "8":
            print("\nLogout berhasil.\n")
            return
        else:
            print("\nPilihan tidak valid.\n")

#menu user ada 6 pilihsn
def menu_user(username):
    while True:
        print("============================================================")
        print("|                                                          |")
        print("|                        MENU USER                         |")
        print("|                                                          |")
        print("============================================================")
        print("[1]. Lihat wisata")
        print("[2]. Cari wisata")
        print("[3]. Beli tiket (e-money)")
        print("[4]. Top up saldo")
        print("[5]. Riwayat transaksi")
        print("[6]. Logout")
        pilih = input("Pilih: ").strip()
        if pilih == "1":
            while True:
                clear()
                tampilkan_wisata()
                if not pilihan_kembali_menu():
                    break
        elif pilih == "2":
            cari_wisata()
        elif pilih == "3":
            beli_tiket(username)
        elif pilih == "4":
            topup(username)
        elif pilih == "5":
            riwayat_transaksi(username)
        elif pilih == "6":
            print("\nLogout berhasil.\n")
            return
        else: 
            print("\nPilihan tidak valid.\n")

#piihan login atau mendaftar 
def main():
    ensure_files_exist()
    
    users = baca_json(FILE_USER)
    if "admin" not in users:
        users["admin"] = {"password": "admin123", "role": "Admin", "saldo": 0}
        simpan_json(FILE_USER, users)

    while True:
        print("============================================================")
        print("|                                                          |")
        print("|                    SISTEM WISATA                         |")
        print("|                                                          |")
        print("============================================================")
        print("[1]. Login sebagai Admin")
        print("[2]. Login sebagai User")
        print("[3]. Registrasi Akun")
        print("[4]. Keluar")
        pilih = input("Pilih: ").strip()
        if pilih == "1":
            user = login("Admin")
            if user:
                menu_admin(user)
        elif pilih == "2":
            user = login("User")
            if user:
                menu_user(user)
        elif pilih == "3":
            daftar_akun()
        elif pilih == "4":
            print("\nTerima kasih telah menggunakan sistem wisata!")
            break
        else:
            print("\nPilihan tidak ada.\n")

if __name__ == "__main__":
    main()
