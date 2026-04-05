import pandas as pd
import matplotlib.pyplot as plt
import io

# Örnek veri (Kendi csv dosyanızı kullanmak için aşağıdaki okuma kısmını değiştirin)
csv_data = """TIME STAMP,GPU UTIL,GPU SCLK,GPU BRD PWR,GPU TEMP,GPU HOTSPOT TEMP,GPU FAN,GPU VOLTAGE,GPU MEM UTIL,GPU MCLK,GPU MEM TEMP,CPU UTIL,CPU FREQUENCY,CPU VOLTAGE,CPU TEMPERATURE,CPU POWER,CPU EDC,CPU TDC,SYSTEM MEM UTIL
N/A,7.00,123.50,48.67,51.00,53.00,0.00,702.33,2176.83,2505.00,58.00,7.16,3.08,1.12,54.75,13.97,24.75,12.27,8.22
2026-03-21 22:58:59.495,7.000,149.000,49,51.000,53.000,0.000,724.000,2176.000,2505.000,58.000,11.59,2.236,1.111,50.657,9.369,17.250,8.243,8.22
2026-03-21 22:59:00.493,8.000,157.000,50,51.000,53.000,0.000,721.000,2177.000,2505.000,58.000,7.57,2.676,1.125,53.159,13.547,25.250,11.879,8.21
2026-03-21 22:59:01.518,7.000,107.000,48,51.000,53.000,0.000,689.000,2177.000,2505.000,58.000,8.03,4.039,1.125,57.852,23.434,32.750,20.868,8.21
2026-03-21 22:59:02.510,6.000,113.000,48,51.000,53.000,0.000,699.000,2177.000,2505.000,58.000,7.78,2.320,1.124,51.880,10.646,22.750,9.281,8.21
2026-03-21 22:59:03.513,7.000,115.000,48,51.000,53.000,0.000,694.000,2177.000,2505.000,58.000,3.85,2.512,1.112,52.744,10.524,18.500,9.339,8.27
2026-03-21 22:59:04.509,7.000,100.000,49,51.000,53.000,0.000,687.000,2177.000,2505.000,58.000,4.17,4.672,1.117,62.217,16.314,32.000,14.035,8.22"""

# df = pd.read_csv('log_dosyaniz.csv') # Kendi dosyanız için buranın başındaki '#' işaretini kaldırın
df = pd.read_csv('log.csv')

# Veri Temizliği
df = df[df['TIME STAMP'] != 'N/A'].copy()
df['TIME STAMP'] = pd.to_datetime(df['TIME STAMP'])
df.set_index('TIME STAMP', inplace=True)
df = df.apply(pd.to_numeric, errors='coerce')

# Matplotlib karanlık tema ayarları
plt.style.use('dark_background')
arka_plan_rengi = '#1a1a1a'

# Çizilecek metrikleri ve renklerini belirliyoruz
metrics = [
    {"col": "GPU TEMP", "title": "GPU Sıcaklığı (°C)", "color": "#00d2ff"},        
    {"col": "CPU TEMPERATURE", "title": "CPU Sıcaklığı (°C)", "color": "#ff6d00"}, 
    {"col": "GPU UTIL", "title": "GPU Kullanımı (%)", "color": "#00e676"},         
    {"col": "CPU UTIL", "title": "CPU Kullanımı (%)", "color": "#ffea00"},         
    {"col": "GPU BRD PWR", "title": "GPU Güç Tüketimi (Watt)", "color": "#d500f9"},
    {"col": "CPU POWER", "title": "CPU Güç Tüketimi (Watt)", "color": "#ff1744"},  
    {"col": "SYSTEM MEM UTIL", "title": "Sistem Belleği (GB)", "color": "#29b6f6"} 
]

# Grafik figürünü oluştur (Genişlik: 18, Yükseklik: 10 olarak güncellendi)
fig, axes = plt.subplots(nrows=len(metrics), ncols=1, figsize=(18, 12), sharex=True)
fig.patch.set_facecolor(arka_plan_rengi)
#fig.suptitle("Sistem Performansı Log Kayıtları", fontsize=16, fontweight='bold', color='white', y=0.97)

# Her bir metrik için grafiği çiz
for ax, metric in zip(axes, metrics):
    col = metric["col"]
    color = metric["color"]
    title = metric["title"]
    
    ax.set_facecolor(arka_plan_rengi)
    
    if col in df.columns:
        x_data = df.index
        y_data = df[col]
        
        # Min, Max, Ort değerlerini hesapla
        c_min = y_data.min()
        c_max = y_data.max()
        c_mean = y_data.mean()
        stats_text = f"Min: {c_min:.1f}  |  Max: {c_max:.1f}  |  Ort: {c_mean:.1f}"
        
        # Düz çizgiyi çiz (Noktasız)
        ax.plot(x_data, y_data, color=color, linewidth=2)
        
        # Çizginin altını doldur
        ax.fill_between(x_data, y_data, color=color, alpha=0.25)
        
        # Başlık ve İstatistikleri yazdır
        ax.set_title(f"{title}    [{stats_text}]", fontsize=11, fontweight='bold', color=color, loc='left', pad=6)
        
        # Izgara ve Kenarlık Ayarları
        ax.grid(True, color='#444444', linestyle='--', alpha=0.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('#555555')
        ax.spines['left'].set_color('#555555')
        ax.tick_params(axis='x', colors='#aaaaaa', labelsize=9)
        ax.tick_params(axis='y', colors='#aaaaaa', labelsize=9)
        
        # Y ekseni limitlerini biraz esnet
        min_y, max_y = ax.get_ylim()
        ax.set_ylim(min_y, max_y + (max_y - min_y) * 0.1)

# X ekseni (Zaman) ayarları
plt.xlabel("Zaman", fontsize=11, fontweight='bold', color='white')
fig.autofmt_xdate(rotation=0) # Yatay genişlediği için tarihleri düz yazdırıyoruz, daha şık duruyor

# Grafikler arası boşlukları (hspace) ve kenar boşluklarını ayarla
plt.tight_layout()
plt.subplots_adjust(top=0.92, hspace=0.6) 

# Grafiği ekrana yansıt
plt.show()