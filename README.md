# 🚇 Sürücüsüz Metro Simülasyonu (Rota Optimizasyonu)

## 📝 Proje Hakkında

Bu proje, metro istasyonları arasında en kısa ve en hızlı rotaları bulan gelişmiş bir Python uygulamasıdır. Sistem, graf veri yapıları kullanarak metro ağını modellemekte ve iki farklı optimizasyon stratejisi sunmaktadır:

- 🎯 **En Az Aktarmalı Rota**: BFS (Breadth-First Search) algoritması kullanarak
- ⚡ **En Hızlı Rota**: A* algoritması kullanarak

### 🌟 Özellikler

- Çoklu metro hattı desteği
- İstasyon ve hatlar arasında aktarma noktaları
- Gerçek zamanlı rota hesaplama
- Detaylı süre hesaplaması
- Esnek istasyon ve hat yönetimi
- NetworkX ile gelişmiş görselleştirme
- Farklı metro hatları için renk kodlaması
- Bulunan rotaların görsel olarak vurgulanması

## 🔄 Sistem Yapısı

Sistem iki ana sınıftan oluşmaktadır:

1. **Istasyon**: Metro istasyonlarını temsil eder.
   - İstasyon kimlik numarası (idx)
   - İstasyon adı (ad)
   - Bulunduğu hat (hat)
   - Komşu istasyonlar ve aralarındaki seyahat süreleri

2. **MetroAgi**: Tüm metro ağını ve rotaları yönetir.
   - İstasyon ekleme ve yönetme
   - Hatlar arasında bağlantı kurma
   - En az aktarmalı rotayı bulma (BFS)
   - En hızlı rotayı bulma (A*)
   - Ağ görselleştirme

## 🛠️ Kullanılan Teknolojiler ve Kütüphaneler

### Ana Teknoloji
- **Python 3.x**: Modern ve yüksek performanslı programlama dili

### Kütüphaneler ve Kullanım Amaçları

| Kütüphane | Modül | Açıklama |
|-----------|--------|-----------|
| **collections** | `defaultdict` | Hat-istasyon eşleştirmelerini yönetmek için |
| | `deque` | BFS algoritması için optimize edilmiş kuyruk yapısı |
| **heapq** | - | A* algoritması için öncelikli kuyruk yapısı |
| **typing** | - | Tip güvenliği ve kod okunabilirliği için tip belirteçleri |
| **networkx** | - | Graf veri yapısı ve görselleştirme |
| **matplotlib** | `pyplot` | Graf görselleştirme ve grafik oluşturma |
| **random** | - | İstasyon konumlarını rastgele belirlemek için |

## 🔍 Algoritmaların Çalışma Mantığı

### 1. BFS (Breadth-First Search) Algoritması

BFS algoritması, en az aktarmalı rotayı bulmak için kullanılır. Algoritmanın çalışma mantığı:

1. **Başlangıç**: Başlangıç istasyonundan başlar
2. **Genişleme**: Her seviyede tüm komşu istasyonları ziyaret eder
3. **Takip**: Ziyaret edildi olarak işaretlenmiş istasyonlar tekrar ziyaret edilmez
4. **Kuyruk Yapısı**: FIFO (First In, First Out) mantığı ile istasyonlar işlenir
5. **Sonuç**: İlk bulunan rota, en az aktarmalı rotadır

```python
def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str):
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
```

### 2. A* Algoritması

A* algoritması, en hızlı rotayı bulmak için kullanılır. Algoritmanın çalışma mantığı:

1. **Maliyet Hesaplama**: Her adımda en düşük maliyetli yolu seçer
2. **Formül**: f(n) = g(n) + h(n)
   - g(n): Başlangıçtan mevcut noktaya kadar olan maliyet (süre)
   - h(n): Mevcut noktadan hedefe tahmini maliyet (heuristic)
3. **Önceliklendirme**: Öncelikli kuyruk (priority queue) kullanarak en düşük maliyetli yolları önceliklendirir
4. **Heuristic Fonksiyonu**: İstasyonlar arası tahmini süreyi hesaplar

```python
def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str):
    pq = [(0 + self.heuristic(baslangic, hedef), id(baslangic), baslangic, [baslangic], 0)]
    ziyaret_edildi = set()
    
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
```

### 🤔 Neden Bu Algoritmalar?

#### BFS Algoritması
- ✅ En az aktarmalı rotayı garantiler
- ✅ Basit ve anlaşılır yapı
- ✅ Aktarma sayısını optimize eder
- ✅ Her düğümü sadece bir kez ziyaret eder
- ✅ Bellek kullanımı dengeli

#### A* Algoritması
- ✅ En hızlı rotayı bulur (zaman optimize)
- ✅ Heuristic fonksiyonu ile performansı artırır
- ✅ Gerçek dünya metro sistemlerine uygun
- ✅ Dinamik rota optimizasyonu
- ✅ Öncelikli kuyruk yapısı ile verimli arama

## 📊 Görselleştirme Sistemi

Proje, NetworkX ve Matplotlib kullanarak kapsamlı bir görselleştirme sistemi içerir:

- **Hat Renkleri**: Her metro hattı benzersiz bir renkle temsil edilir
  - Kırmızı Hat: #FF0000
  - Mavi Hat: #0000FF
  - Turuncu Hat: #FFA500

- **İstasyon Yerleşimleri**: İstasyonlar, hatlarına göre belirli alanlara yerleştirilir
  - Kırmızı Hat: Sol tarafta
  - Mavi Hat: Ortada
  - Turuncu Hat: Sağ tarafta

- **Rota Vurgulama**: Bulunan rotalar, kalın kırmızı çizgilerle vurgulanır
- **Bilgi Paneli**: Rota detayları (başlangıç, hedef, süre/aktarma bilgileri)
- **Aktarma Noktaları**: Farklı hatlar arasındaki aktarma noktaları

```python
def gorsellestir(self, rota: Optional[List[Istasyon]] = None, rota_bilgisi: str = "", ax: Optional[plt.Axes] = None):
    G = nx.Graph()
    
    # İstasyonları ve bağlantıları ekle
    for istasyon in self.istasyonlar.values():
        G.add_node(istasyon.idx, ad=istasyon.ad, hat=istasyon.hat, pos=(pos_x, random.random()))
        
        for komsu, sure in istasyon.komsular:
            G.add_edge(istasyon.idx, komsu.idx, sure=sure, hat=istasyon.hat)
    
    # Rota varsa vurgula
    if rota:
        rota_edges = [(rota[i].idx, rota[i+1].idx) for i in range(len(rota)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=rota_edges, edge_color='red', width=5, ax=ax)
```

## 🚀 Örnek Kullanım ve Test Sonuçları

### Temel Kullanım

```python
# Metro ağı oluşturma
metro = MetroAgi()

# İstasyon ekleme
metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")

# Bağlantı ekleme
metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma

# Rota bulma
rota = metro.en_az_aktarma_bul("M1", "K4")
sonuc = metro.en_hizli_rota_bul("M1", "K4")
```

### 📊 Test Senaryoları ve Sonuçları

#### 1. AŞTİ'den OSB'ye
- **En az aktarmalı rota**: 
  ```
  AŞTİ -> Kızılay -> Ulus -> Demetevler -> OSB
  ```
- **En hızlı rota**: 
  ```
  AŞTİ -> Kızılay -> Ulus -> Demetevler -> OSB
  Süre: 23 dakika
  ```

#### 2. Batıkent'ten Keçiören'e
- **En az aktarmalı rota**: 
  ```
  Batıkent -> Demetevler -> Gar -> Keçiören
  ```
- **En hızlı rota**: 
  ```
  Batıkent -> Demetevler -> Gar -> Keçiören
  Süre: 21 dakika
  ```

#### 3. Keçiören'den AŞTİ'ye
- **En az aktarmalı rota**: 
  ```
  Keçiören -> Gar -> Sıhhiye -> Kızılay -> AŞTİ
  ```
- **En hızlı rota**:
  ```
  Keçiören -> Gar -> Sıhhiye -> Kızılay -> AŞTİ
  Süre: 17 dakika
  ```

## 💡 Projeyi Geliştirme Fikirleri

### 1. 🎨 Görsel Arayüz İyileştirmeleri
- İnteraktif metro haritası (tıklanabilir istasyonlar)
- Gerçek zamanlı rota animasyonu
- Mobil uyumlu web arayüzü
- 3D metro haritası görüntüleme
- Daha gerçekçi istasyon yerleşimi

### 2. 📊 Veri Yönetimi ve Entegrasyonu
- Gerçek metro verilerini JSON/CSV formatında yükleme
- Veritabanı entegrasyonu (SQLite, PostgreSQL)
- Dinamik istasyon ve hat ekleme/düzenleme arayüzü
- Veri doğrulama ve hata kontrolü mekanizmaları
- Otomatik veri güncelleme sistemi

### 3. ⚡ Algoritma ve Optimizasyon İyileştirmeleri
- Gelişmiş heuristic fonksiyonları
  ```python
  def heuristic(self, istasyon: Istasyon, hedef: Istasyon) -> int:
      # Şu anki uygulama:
      return 1  # Basit bir heuristic: her istasyon arası 1 dakika
      
      # Potansiyel iyileştirme:
      # return self.manhattan_distance(istasyon, hedef)
  ```
- Çoklu hedef noktası optimizasyonu
- Alternatif rotalar sunma kabiliyeti
- Dijkstra ve diğer algoritmaların implementasyonu
- Yoğunluk bazlı rota optimizasyonu

### 4. 🔧 Özellik Eklemeleri
- İstasyon bilgileri ve özellikleri (aktarma noktaları, çıkışlar)
- Hat kesintileri ve bakım durumları sistemi
- Yoğun saatlerde alternatif rota önerileri
- Engelli erişim bilgileri ve erişilebilir rota hesaplama
- İstasyon yakınındaki önemli noktalar (POI)
- Zaman bazlı rota hesaplama (gece/gündüz rotaları)

### 5. 🚀 Performans İyileştirmeleri
- Paralel rota hesaplama
  ```python
  # Paralel hesaplama örneği
  import concurrent.futures
  
  def paralel_rota_hesapla(self, baslangic_id, hedef_id):
      with concurrent.futures.ProcessPoolExecutor() as executor:
          bfs_future = executor.submit(self.en_az_aktarma_bul, baslangic_id, hedef_id)
          astar_future = executor.submit(self.en_hizli_rota_bul, baslangic_id, hedef_id)
          
          return bfs_future.result(), astar_future.result()
  ```
- Önbellek mekanizması (cache)
- Bellek optimizasyonu
- Daha verimli veri yapıları
- Hızlı arama algoritmaları

## 🛠️ Gelecek Sürüm Planı

### Versiyon 1.1
- Gelişmiş heuristic fonksiyonları
- Metro ağı yerleşiminin iyileştirilmesi
- Aktarma analizini geliştirme

### Versiyon 1.2
- Alternatif rotalar gösterimi
- İnteraktif kullanıcı arayüzü
- Yoğunluk verisi entegrasyonu

### Versiyon 2.0
- Web tabanlı arayüz
- Gerçek zamanlı veri entegrasyonu
- Mobil uygulama desteği

## 👥 Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeniOzellik`)
5. Pull Request oluşturun

## 📞 İletişim

Proje ile ilgili sorularınız için:
- GitHub Issues
- E-posta: [eren_ali_koca@hotmail.com]

---

<div align="center">
Made with ❤️ by Eren Ali Koca
</div>
