from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional
import networkx as nx
import matplotlib.pyplot as plt
import random

class Istasyon:
    """
    Metro istasyonunu temsil eden sınıf.
    
    Attributes:
        idx (str): İstasyonun benzersiz kimlik numarası
        ad (str): İstasyonun adı
        hat (str): İstasyonun bulunduğu metro hattı
        komsular (List[Tuple['Istasyon', int]]): Komşu istasyonlar ve aralarındaki süreler
    """
    def __init__(self, idx: str, ad: str, hat: str):
        if not idx or not ad or not hat:
            raise ValueError("İstasyon bilgileri boş olamaz")
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int) -> None:
        """
        Komşu istasyon ekler.
        
        Args:
            istasyon (Istasyon): Eklenecek komşu istasyon
            sure (int): İki istasyon arasındaki süre (dakika)
            
        Raises:
            ValueError: Süre negatif olduğunda
        """
        if sure < 0:
            raise ValueError("İstasyonlar arası süre negatif olamaz")
        self.komsular.append((istasyon, sure))

class MetroAgi:
    """
    Metro ağını temsil eden sınıf.
    
    Bu sınıf, metro istasyonlarını ve hatlarını yönetir, en kısa ve en hızlı rotaları bulur.
    """
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        """
        Yeni bir metro istasyonu ekler.
        
        Args:
            idx (str): İstasyonun benzersiz kimlik numarası
            ad (str): İstasyonun adı
            hat (str): İstasyonun bulunduğu metro hattı
            
        Raises:
            ValueError: İstasyon bilgileri boş olduğunda
        """
        if not idx or not ad or not hat:
            raise ValueError("İstasyon bilgileri boş olamaz")
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        """
        İki istasyon arasına bağlantı ekler.
        
        Args:
            istasyon1_id (str): Birinci istasyonun kimlik numarası
            istasyon2_id (str): İkinci istasyonun kimlik numarası
            sure (int): İki istasyon arasındaki süre (dakika)
            
        Raises:
            KeyError: İstasyon bulunamadığında
            ValueError: Süre negatif olduğunda
        """
        if sure < 0:
            raise ValueError("İstasyonlar arası süre negatif olamaz")
        if istasyon1_id not in self.istasyonlar or istasyon2_id not in self.istasyonlar:
            raise KeyError("İstasyon bulunamadı")
        
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)
    
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """
        BFS algoritması kullanarak en az aktarmalı rotayı bulur.
        
        Args:
            baslangic_id (str): Başlangıç istasyonunun kimlik numarası
            hedef_id (str): Hedef istasyonunun kimlik numarası
            
        Returns:
            Optional[List[Istasyon]]: Bulunan rota veya None (rota bulunamazsa)
            
        Raises:
            KeyError: İstasyon bulunamadığında
        """
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            raise KeyError("İstasyon bulunamadı")
            
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        
        kuyruk = deque([(baslangic, [baslangic])])
        ziyaret_edildi = {baslangic}
        
        while kuyruk:
            mevcut_istasyon, mevcut_rota = kuyruk.popleft()
            
            if mevcut_istasyon.idx == hedef_id:
                return mevcut_rota
                
            for komsu_istasyon, _ in mevcut_istasyon.komsular:
                if komsu_istasyon not in ziyaret_edildi:
                    ziyaret_edildi.add(komsu_istasyon)
                    yeni_rota = mevcut_rota + [komsu_istasyon]
                    kuyruk.append((komsu_istasyon, yeni_rota))
                    
        return None       


    def heuristic(self, istasyon: Istasyon, hedef: Istasyon) -> int:
        """
        A* algoritması için heuristic fonksiyonu.
        
        Args:
            istasyon (Istasyon): Mevcut istasyon
            hedef (Istasyon): Hedef istasyon
            
        Returns:
            int: Tahmini süre
        """
        return 1  # Basit bir heuristic: her istasyon arası 1 dakika

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """
        A* algoritması kullanarak en hızlı rotayı bulur.
        
        Args:
            baslangic_id (str): Başlangıç istasyonunun kimlik numarası
            hedef_id (str): Hedef istasyonunun kimlik numarası
            
        Returns:
            Optional[Tuple[List[Istasyon], int]]: (rota, toplam_süre) veya None (rota bulunamazsa)
            
        Raises:
            KeyError: İstasyon bulunamadığında
        """
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            raise KeyError("İstasyon bulunamadı")

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        ziyaret_edildi = set()
        
        # (toplam_süre + heuristic, istasyon_id, istasyon, rota, toplanan_süre)
        pq = [(0 + self.heuristic(baslangic, hedef), id(baslangic), baslangic, [baslangic], 0)]
        
        while pq:
            _, _, mevcut_istasyon, mevcut_rota, toplam_sure = heapq.heappop(pq)
            
            if mevcut_istasyon.idx == hedef_id:
                return (mevcut_rota, toplam_sure)
                
            if mevcut_istasyon in ziyaret_edildi:
                continue
                
            ziyaret_edildi.add(mevcut_istasyon)
            
            for komsu_istasyon, sure in mevcut_istasyon.komsular:
                if komsu_istasyon not in ziyaret_edildi:
                    yeni_sure = toplam_sure + sure
                    yeni_rota = mevcut_rota + [komsu_istasyon]
                    
                    heapq.heappush(pq, (yeni_sure + self.heuristic(komsu_istasyon, hedef), 
                                      id(komsu_istasyon), komsu_istasyon, yeni_rota, yeni_sure))
                    
        return None

    def gorsellestir(self, rota: Optional[List[Istasyon]] = None, rota_bilgisi: str = "", ax: Optional[plt.Axes] = None) -> None:
        """
        Metro ağını görselleştirir.
        
        Args:
            rota (Optional[List[Istasyon]]): Vurgulanacak rota (varsa)
            rota_bilgisi (str): Rota hakkında bilgi metni
            ax (Optional[plt.Axes]): Matplotlib ekseni
        """
        G = nx.Graph()
        
        # Her hat için sabit renkler kullan
        hat_renkleri = {
            "Kırmızı Hat": "#FF0000",
            "Mavi Hat": "#0000FF",
            "Turuncu Hat": "#FFA500"
        }
        
        # İstasyonları ve bağlantıları ekle
        for istasyon in self.istasyonlar.values():
            # İstasyonların pozisyonlarını hatlarına göre belirle
            if istasyon.hat == "Kırmızı Hat":
                pos_x = 0.2 + random.random() * 0.1  # Sol tarafta
            elif istasyon.hat == "Mavi Hat":
                pos_x = 0.4 + random.random() * 0.1  # Orta tarafta
            else:  # Turuncu Hat
                pos_x = 0.6 + random.random() * 0.1  # Sağ tarafta
            
            G.add_node(istasyon.idx, 
                      ad=istasyon.ad,
                      hat=istasyon.hat,
                      pos=(pos_x, random.random()))
            
            for komsu, sure in istasyon.komsular:
                G.add_edge(istasyon.idx, komsu.idx, 
                          sure=sure,
                          hat=istasyon.hat)
        
        # Eksen ayarları
        if ax is None:
            ax = plt.gca()
        
        # İstasyonları çiz
        pos = nx.get_node_attributes(G, 'pos')
        nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='white', 
                             edgecolors='black', linewidths=2, ax=ax)
        
        # İstasyon isimlerini ekle
        nx.draw_networkx_labels(G, pos, 
                              labels={node: G.nodes[node]['ad'] for node in G.nodes()},
                              font_size=10, font_weight='bold', ax=ax)
        
        # Bağlantıları çiz
        for hat in self.hatlar.keys():
            edges = [(u, v) for (u, v, d) in G.edges(data=True) if d['hat'] == hat]
            nx.draw_networkx_edges(G, pos, edgelist=edges, 
                                 edge_color=hat_renkleri[hat],
                                 width=3, ax=ax)
            
            # Hat isimlerini ekle
            if edges:
                edge = edges[0]
                pos1 = pos[edge[0]]
                pos2 = pos[edge[1]]
                pos_mid = ((pos1[0] + pos2[0])/2, (pos1[1] + pos2[1])/2)
                ax.text(pos_mid[0], pos_mid[1], hat,
                       color=hat_renkleri[hat],
                       fontsize=8, fontweight='bold',
                       bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
        
        # Rota varsa vurgula
        if rota:
            rota_edges = [(rota[i].idx, rota[i+1].idx) 
                         for i in range(len(rota)-1)]
            nx.draw_networkx_edges(G, pos, edgelist=rota_edges,
                                 edge_color='red',
                                 width=5, ax=ax)
            
            # Rota bilgisini ekle
            rota_detay = f"Başlangıç: {rota[0].ad}\n"
            rota_detay += f"Hedef: {rota[-1].ad}\n"
            rota_detay += f"{rota_bilgisi}"
            
            ax.text(0.02, 0.98, rota_detay,
                   transform=ax.transAxes,
                   fontsize=12,
                   bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'),
                   verticalalignment='top')
        
        ax.set_title("Metro Ağı Görselleştirmesi", fontsize=14, pad=20)
        ax.axis('off')

# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    
    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # Tüm görselleştirmeleri tek pencerede göster
    plt.figure(figsize=(20, 15))
    
    # Ana metro ağı
    plt.subplot(2, 2, 1)
    metro.gorsellestir()
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    plt.subplot(2, 2, 2)
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        rota_bilgisi = "En az aktarmalı rota:\n" + " -> ".join(i.ad for i in rota)
        print(rota_bilgisi)
        metro.gorsellestir(rota, rota_bilgisi)
    
    plt.subplot(2, 2, 3)
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        rota_bilgisi = f"En hızlı rota ({sure} dakika):\n" + " -> ".join(i.ad for i in rota)
        print(rota_bilgisi)
        metro.gorsellestir(rota, rota_bilgisi)
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    plt.subplot(2, 2, 4)
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        rota_bilgisi = "En az aktarmalı rota:\n" + " -> ".join(i.ad for i in rota)
        print(rota_bilgisi)
        metro.gorsellestir(rota, rota_bilgisi)
    
    # Yeni bir pencere aç
    plt.figure(figsize=(20, 15))
    
    # Senaryo 2'nin devamı
    plt.subplot(2, 2, 1)
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        rota_bilgisi = f"En hızlı rota ({sure} dakika):\n" + " -> ".join(i.ad for i in rota)
        print(rota_bilgisi)
        metro.gorsellestir(rota, rota_bilgisi)
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    plt.subplot(2, 2, 2)
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        rota_bilgisi = "En az aktarmalı rota:\n" + " -> ".join(i.ad for i in rota)
        print(rota_bilgisi)
        metro.gorsellestir(rota, rota_bilgisi)
    
    plt.subplot(2, 2, 3)
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        rota_bilgisi = f"En hızlı rota ({sure} dakika):\n" + " -> ".join(i.ad for i in rota)
        print(rota_bilgisi)
        metro.gorsellestir(rota, rota_bilgisi)
    
    # Tüm grafikleri göster
    plt.tight_layout()
    plt.show() 