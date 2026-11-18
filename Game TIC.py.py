"""
ARENA PERTARUNGAN - Game RPG berbasis teks
Project tugas OOP (Python)

Konsep OOP yang dicakup:
 1. Class & Object
 2. Constructor (__init__)
 3. Attribute (instance & class attribute)
 4. Method (instance, @classmethod, @staticmethod)
 5. Encapsulation (atribut private + @property & setter)
 6. Inheritance (pewarisan) + super()
 7. Polymorphism (method sama, perilaku beda)
 8. Abstraction (ABC & @abstractmethod)
 9. Magic / Dunder method (__str__, __repr__, __lt__, __len__)
10. Composition (Karakter "punya" Inventaris, Inventaris "punya" Item)
"""

import random
from abc import ABC, abstractmethod


# ======================================================================
# COMPOSITION: Item & Inventaris
# ======================================================================
class Item:
    """Item penyembuh yang bisa disimpan di inventaris."""

    def __init__(self, nama, pemulihan_hp):
        self.nama = nama
        self.pemulihan_hp = pemulihan_hp

    def __str__(self):
        return f"{self.nama} (+{self.pemulihan_hp} HP)"


class Inventaris:
    """Tempat menyimpan item. Daftar item bersifat private (encapsulation)."""

    def __init__(self):
        self.__items = []

    def tambah(self, item):
        self.__items.append(item)

    def pakai(self, nomor):
        """Mengambil item berdasarkan nomor (mulai dari 1). None jika salah."""
        if 1 <= nomor <= len(self.__items):
            return self.__items.pop(nomor - 1)
        return None

    def tampilkan(self):
        if not self.__items:
            print("   (inventaris kosong)")
        for i, item in enumerate(self.__items, start=1):
            print(f"   {i}. {item}")

    def __len__(self):  # magic method
        return len(self.__items)


# ======================================================================
# ABSTRACTION: Karakter (abstract class)
# ======================================================================
class Karakter(ABC):
    jumlah_karakter = 0  # class attribute

    def __init__(self, nama, hp, kekuatan):  # constructor
        self.nama = nama
        self.__hp = hp            # private attribute
        self.__hp_maks = hp       # private attribute
        self.kekuatan = kekuatan
        self.inventaris = Inventaris()  # composition
        Karakter.jumlah_karakter += 1

    # ---------- Encapsulation: property & setter ----------
    @property
    def hp(self):
        return self.__hp

    @hp.setter
    def hp(self, nilai):
        # HP tidak boleh kurang dari 0 atau lebih dari HP maksimal
        self.__hp = max(0, min(nilai, self.__hp_maks))

    @property
    def hp_maks(self):
        return self.__hp_maks

    @property
    def hidup(self):
        return self.__hp > 0

    # ---------- Abstract methods (wajib di-override) ----------
    @abstractmethod
    def serang(self, target):
        pass

    @abstractmethod
    def skill_khusus(self, target):
        pass

    # ---------- Instance method ----------
    def terima_damage(self, damage):
        self.hp -= damage
        print(f"   >> {self.nama} menerima {damage} damage "
              f"(HP: {self.hp}/{self.hp_maks})")

    def pulihkan(self, jumlah):
        self.hp += jumlah
        print(f"   >> {self.nama} pulih {jumlah} HP "
              f"(HP: {self.hp}/{self.hp_maks})")

    # ---------- Static method ----------
    @staticmethod
    def hitung_kritis(damage, peluang=0.2):
        """Tidak butuh self/cls. Return (damage, apakah_kritis)."""
        if random.random() < peluang:
            return damage * 2, True
        return damage, False

    # ---------- Class method ----------
    @classmethod
    def total_karakter(cls):
        return cls.jumlah_karakter

    # ---------- Magic methods ----------
    def __str__(self):
        return f"{self.nama} [HP: {self.hp}/{self.hp_maks}]"

    def __repr__(self):
        return f"{self.__class__.__name__}(nama='{self.nama}', hp={self.hp})"

    def __lt__(self, other):
        return self.hp < other.hp


# ======================================================================
# INHERITANCE: Pahlawan (turunan Karakter)
# ======================================================================
class Pahlawan(Karakter):
    BIAYA_SKILL = 15

    def __init__(self, nama, hp, kekuatan):
        super().__init__(nama, hp, kekuatan)
        self.energi = 30

    def serang(self, target):
        dasar = random.randint(self.kekuatan - 3, self.kekuatan + 3)
        damage, kritis = self.hitung_kritis(dasar)
        print(f"{self.nama} menyerang {target.nama}!" +
              (" KRITIS!" if kritis else ""))
        target.terima_damage(damage)

    def skill_khusus(self, target):
        raise NotImplementedError

    def bisa_skill(self):
        if self.energi < self.BIAYA_SKILL:
            print("   Energi tidak cukup untuk skill!")
            return False
        self.energi -= self.BIAYA_SKILL
        return True

    def istirahat_ringan(self):
        self.energi = min(30, self.energi + 5)


# ---------- Polymorphism: tiap kelas punya skill berbeda ----------
class Prajurit(Pahlawan):
    def __init__(self, nama):
        super().__init__(nama, hp=120, kekuatan=14)

    def skill_khusus(self, target):
        if not self.bisa_skill():
            return False
        print(f"{self.nama} memakai TEBASAN KERAS!")
        target.terima_damage(self.kekuatan * 2)
        return True


class Penyihir(Pahlawan):
    def __init__(self, nama):
        super().__init__(nama, hp=80, kekuatan=18)

    def skill_khusus(self, target):
        if not self.bisa_skill():
            return False
        print(f"{self.nama} merapal BOLA API dan menyerap tenaga!")
        target.terima_damage(int(self.kekuatan * 2.5))
        self.pulihkan(10)
        return True


class Pemanah(Pahlawan):
    def __init__(self, nama):
        super().__init__(nama, hp=95, kekuatan=15)

    def skill_khusus(self, target):
        if not self.bisa_skill():
            return False
        print(f"{self.nama} melepaskan HUJAN PANAH (2x tembakan)!")
        for _ in range(2):
            target.terima_damage(self.kekuatan)
        return True


# ======================================================================
# INHERITANCE: Monster (turunan Karakter)
# ======================================================================
class Monster(Karakter):
    def __init__(self, nama, hp, kekuatan):
        super().__init__(nama, hp, kekuatan)

    def serang(self, target):
        damage = random.randint(self.kekuatan - 3, self.kekuatan + 3)
        print(f"{self.nama} menyerang {target.nama}!")
        target.terima_damage(damage)

    def skill_khusus(self, target):
        print(f"{self.nama} mengamuk dengan SERANGAN BRUTAL!")
        target.terima_damage(self.kekuatan * 2)

    @classmethod
    def buat_gelombang(cls):
        """Factory method: membuat daftar monster untuk satu permainan."""
        return [
            cls("Slime", 40, 8),
            cls("Goblin", 65, 11),
            cls("Naga Kecil", 110, 16),
        ]


# ======================================================================
# KELAS GAME
# ======================================================================
class Game:
    def __init__(self):
        self.pemain = None
        self.monsters = Monster.buat_gelombang()

    def pilih_karakter(self):
        print("=" * 45)
        print("        ARENA PERTARUNGAN (OOP Game)")
        print("=" * 45)
        nama = input("Masukkan nama pahlawan: ").strip() or "Pahlawan"
        print("\nPilih kelas:")
        print(" 1. Prajurit  (HP besar, serangan kuat)")
        print(" 2. Penyihir  (HP kecil, skill sangat kuat)")
        print(" 3. Pemanah   (seimbang, skill 2x tembak)")

        kelas = {"1": Prajurit, "2": Penyihir, "3": Pemanah}
        pilihan = input("Pilihan (1/2/3): ").strip()
        self.pemain = kelas.get(pilihan, Prajurit)(nama)

        # isi inventaris awal
        self.pemain.inventaris.tambah(Item("Ramuan Kecil", 25))
        self.pemain.inventaris.tambah(Item("Ramuan Besar", 50))
        print(f"\nSelamat datang, {self.pemain.nama} sang "
              f"{self.pemain.__class__.__name__}!")

    def pakai_item(self):
        if len(self.pemain.inventaris) == 0:
            print("   Inventaris kosong!")
            return False
        print("   Inventaris:")
        self.pemain.inventaris.tampilkan()
        try:
            nomor = int(input("   Pilih nomor item: "))
        except ValueError:
            print("   Input tidak valid.")
            return False
        item = self.pemain.inventaris.pakai(nomor)
        if item is None:
            print("   Item tidak ditemukan.")
            return False
        self.pemain.pulihkan(item.pemulihan_hp)
        return True

    def giliran_pemain(self, monster):
        while True:
            print(f"\n[{self.pemain}] Energi: {self.pemain.energi}")
            print(f"[{monster}]")
            print("1. Serang  2. Skill Khusus  3. Pakai Item")
            aksi = input("Aksi: ").strip()
            if aksi == "1":
                self.pemain.serang(monster)
                return
            elif aksi == "2":
                if self.pemain.skill_khusus(monster):
                    return
            elif aksi == "3":
                if self.pakai_item():
                    return
            else:
                print("   Pilihan tidak valid.")

    def giliran_monster(self, monster):
        # Polymorphism: monster memilih serang biasa atau skill
        if random.random() < 0.25:
            monster.skill_khusus(self.pemain)
        else:
            monster.serang(self.pemain)

    def pertarungan(self, monster):
        print(f"\n===== {monster.nama} muncul! =====")
        while self.pemain.hidup and monster.hidup:
            self.giliran_pemain(monster)
            if not monster.hidup:
                break
            self.giliran_monster(monster)
            self.pemain.istirahat_ringan()

        if self.pemain.hidup:
            print(f"\n*** {monster.nama} dikalahkan! ***")
            self.pemain.pulihkan(20)
            self.pemain.inventaris.tambah(Item("Ramuan Kecil", 25))
            print("   Kamu mendapat 1 Ramuan Kecil.")

    def mulai(self):
        self.pilih_karakter()
        for monster in self.monsters:
            self.pertarungan(monster)
            if not self.pemain.hidup:
                print("\nKamu kalah... GAME OVER.")
                break
        else:
            print("\nSELAMAT! Kamu menaklukkan semua monster di arena!")

        print(f"\nTotal karakter yang dibuat: {Karakter.total_karakter()}")
        # Memakai __lt__ : bandingkan siapa yang HP-nya lebih sedikit
        print(f"{self.pemain.nama} < {self.monsters[0].nama} ? "
              f"{self.pemain < self.monsters[0]}")


if __name__ == "__main__":
    Game().mulai()
