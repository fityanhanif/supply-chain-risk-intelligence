# Jurnal Penelitian Proyek

# Supply Chain Risk Intelligence Berbasis DataCo Smart Supply Chain

## Abstrak

Proyek ini membangun sistem analisis risiko rantai pasok menggunakan dataset publik DataCo Smart Supply Chain. Fokus utama penelitian adalah memahami risiko keterlambatan pengiriman, hubungan antara performa pengiriman dan profitabilitas, serta membangun model awal untuk memberi skor risiko keterlambatan sebelum proses fulfillment selesai. Dataset utama berisi 180.519 catatan order dengan 53 kolom awal. Dari data tersebut dibangun pipeline Python untuk membersihkan data, membuat tabel mart KPI, melatih model klasifikasi late delivery risk, dan mengekspor data ke dashboard statis berbasis HTML dan Chart.js.

Hasil utama menunjukkan bahwa 98.977 order atau 54,83% dari total catatan memiliki risiko keterlambatan pengiriman. Total sales pada dataset mencapai sekitar $36,78 juta dengan benefit atau profit proxy sekitar $3,97 juta. Model terbaik yang dipilih adalah Random Forest dengan accuracy 69,57%, precision late class 81,35%, recall late class 57,73%, F1 late class 67,54%, dan ROC-AUC 75,63%. Model ini tidak dipilih karena accuracy tertinggi, tetapi karena memiliki composite score terbaik ketika recall untuk kelas late risk dijadikan prioritas bisnis.

## 1. Latar Belakang

Supply chain modern tidak hanya membutuhkan laporan historis, tetapi juga sistem intelijen yang dapat memberi sinyal risiko secara lebih awal. Dalam operasi e-commerce atau distribusi barang, keterlambatan pengiriman dapat berdampak pada kepuasan pelanggan, biaya kompensasi, performa SLA, dan reputasi layanan. Di sisi lain, bisnis juga harus mempertimbangkan profitabilitas. Segmen dengan penjualan besar belum tentu sehat jika margin rendah atau risiko keterlambatan tinggi.

Berdasarkan masalah tersebut, proyek ini dirancang sebagai studi kasus portfolio Data Analyst dan Data Scientist. Tujuannya bukan hanya membuat visualisasi, tetapi membangun alur kerja end to end dari data mentah sampai dashboard yang dapat dipakai untuk menjelaskan keputusan operasional.

## 2. Rumusan Masalah

Penelitian ini menjawab beberapa pertanyaan utama:

1. Seberapa besar tingkat risiko keterlambatan pengiriman pada dataset?
2. Mode pengiriman, market, region, kategori produk, dan customer segment mana yang paling berkontribusi terhadap risiko?
3. Bagaimana hubungan antara sales, profit, margin, dan late delivery risk?
4. Apakah risiko keterlambatan dapat diberi skor sebelum fulfillment selesai?
5. Bagaimana hasil model harus dibaca secara bisnis, terutama ketika accuracy tidak menjadi satu satunya ukuran keberhasilan?
6. Rekomendasi operasional apa yang bisa diprioritaskan dari dashboard?

## 3. Sumber Data

Dataset yang digunakan adalah DataCo Smart Supply Chain for Big Data Analysis. File mentah utama yang digunakan secara lokal adalah:

- `data/raw/DataCoSupplyChainDataset.csv`
- `data/raw/DescriptionDataCoSupplyChain.csv`
- `data/raw/tokenized_access_logs.csv`

Dataset order utama memiliki 180.519 baris dan 53 kolom awal. Data ini bersifat publik dan historis, sehingga tidak merepresentasikan sistem supply chain live. Karena itu, hasil proyek diposisikan sebagai prototype decision support dan portfolio case study, bukan sistem produksi SLA.

## 4. Desain Pipeline

Pipeline proyek dibuat agar reproducible dan mudah dijelaskan saat interview. Alurnya terdiri dari empat tahap besar.

### 4.1 Persiapan Data

Script `scripts/prepare_data.py` membaca dataset mentah, membersihkan nama kolom, membuat fitur tanggal, menghapus atau menghindari field yang tidak sesuai untuk output publik, lalu menghasilkan file bersih dan KPI marts.

Output utama tahap ini:

- `data/processed/orders_clean.csv`
- `data/marts/delivery_kpis.csv`
- `data/marts/profitability_kpis.csv`
- `data/marts/region_shipping_kpis.csv`
- `data/marts/category_performance.csv`
- `data/marts/customer_market_kpis.csv`
- `data/marts/monthly_delivery_trend.csv`
- `data/marts/data_profile.json`

Tabel mart dibuat supaya dashboard tidak perlu membaca raw dataset besar. Ini penting untuk deployment statis di Vercel karena dashboard cukup membaca JSON kecil yang sudah diproses sebelumnya.

### 4.2 Exploratory Data Analysis

EDA dilakukan untuk memahami distribusi order, status pengiriman, shipping mode, market, region, kategori produk, dan performa profit. Hasil EDA kemudian diterjemahkan ke dalam visual dashboard. Fokus EDA bukan hanya mencari grafik menarik, tetapi menemukan cerita bisnis yang bisa dipakai recruiter untuk menilai kemampuan analisis.

Beberapa temuan penting:

- Total order: 180.519
- Late delivery risk order: 98.977
- Late delivery risk rate: 54,83%
- Total sales: sekitar $36,78 juta
- Total benefit atau profit proxy: sekitar $3,97 juta
- Shipping mode terbesar: Standard Class
- Market terbesar: LATAM

### 4.3 Modeling

Target model adalah `late_delivery_risk`, dengan arti:

- 1 berarti order memiliki risiko keterlambatan
- 0 berarti order tidak memiliki risiko keterlambatan

Model yang dibandingkan:

1. Logistic Regression sebagai baseline yang lebih interpretable
2. Random Forest sebagai benchmark non-linear yang lebih fleksibel

Model dibuat sebagai operational prediction model. Artinya model hanya boleh menggunakan informasi yang secara wajar tersedia sebelum pengiriman selesai.

Kolom yang sengaja dikeluarkan karena berpotensi leakage:

- `delivery_status`
- `days_for_shipping_real`
- `shipping_gap`
- `shipping_date_dateorders`
- `order_status`
- `late_delivery_risk` dan turunan targetnya

Keputusan ini membuat skor model lebih realistis. Jika kolom seperti `days_for_shipping_real` dipakai, model akan terlihat lebih akurat, tetapi itu bukan prediksi operasional karena informasi tersebut baru diketahui setelah pengiriman terjadi.

### 4.4 Dashboard Data

Script `scripts/build_dashboard_data.py` menggabungkan KPI marts dan output model ke dalam `dashboard/assets/dashboard_data.json`. Dashboard dibuat statis dengan HTML, CSS, JavaScript, dan Chart.js. Keputusan ini dipilih agar project mudah dibuka, ringan, dan dapat dideploy tanpa backend.

## 5. Penjelasan Dashboard

Dashboard terdiri dari beberapa menu utama.

### 5.1 Overview

Menu Overview menampilkan ringkasan eksekutif. Hero dashboard menekankan masalah utama yaitu menemukan delivery risk sebelum menjadi service problem. KPI utama yang ditampilkan meliputi total order, sales, profit, late risk rate, dan model recall.

Bagian ini juga menampilkan distribusi delivery status, tren monthly late delivery rate, dan insight penting seperti:

- Late delivery adalah risiko operasional utama
- Standard Class mendominasi volume shipment
- Profit dan delivery risk harus dianalisis bersama
- Model perlu menghindari leakage agar realistis

### 5.2 Delivery Risk

Menu Delivery Risk fokus pada performa pengiriman. Visual yang digunakan antara lain late rate by shipping mode dan tabel region x shipping mode yang paling berisiko. Tujuannya adalah membantu operator menemukan kombinasi area dan metode pengiriman yang perlu prioritas monitoring.

### 5.3 Profitability

Menu Profitability melihat hubungan antara kategori, market, region, sales, profit margin, dan late rate. Insight penting dari menu ini adalah bahwa revenue tinggi belum tentu berarti performa bisnis sehat. Jika revenue tinggi terjadi pada segmen dengan margin rendah dan delay risk tinggi, maka segmen tersebut harus ditinjau ulang.

### 5.4 Customer Region

Menu Customer Region menunjukkan performa berdasarkan customer segment dan market. Bagian ini membantu melihat apakah risiko dan profitabilitas berbeda antar segmen pelanggan dan lokasi pasar.

### 5.5 Model Insights

Menu Model Insights menjelaskan model scoring. Terdapat feature importance, risk score sample, dan daftar order dengan probability risk paling tinggi. Menu ini menegaskan bahwa model tidak menggunakan field post shipment seperti actual shipping days dan final delivery status.

### 5.6 Recommendations

Menu Recommendations menerjemahkan insight menjadi tindakan. Rekomendasi diarahkan pada monitoring fulfillment queue, prioritas area dengan risiko tinggi, evaluasi shipping mode, dan pemisahan analisis revenue dari profit quality.

### 5.7 Jurnal Riset

Menu Jurnal Riset ditambahkan untuk menjelaskan proyek dari awal sampai akhir dalam bahasa Indonesia. Bagian ini dibuat agar dashboard tidak hanya menjadi visual BI, tetapi juga dokumentasi penelitian yang bisa dibaca recruiter, dosen, atau stakeholder non-teknis.

## 6. Kenapa Random Forest Dipilih

Random Forest dipilih bukan karena accuracy tertinggi. Logistic Regression memiliki accuracy 70,02%, sedangkan Random Forest memiliki accuracy 69,57%. Jika hanya melihat accuracy, Logistic Regression terlihat sedikit lebih baik.

Namun tujuan bisnis proyek ini adalah menangkap order yang berisiko telat. Dalam konteks supply chain, missed risky shipment lebih mahal daripada over-flagging order aman. Karena itu, pemilihan model menggunakan composite score:

- 50% recall late class
- 30% F1 late class
- 20% ROC-AUC

Hasil perbandingan:

Logistic Regression:

- Accuracy: 70,02%
- Precision late class: 82,96%
- Recall late class: 57,02%
- F1 late class: 67,59%
- ROC-AUC: 75,83%
- Composite score: 63,9523%

Random Forest:

- Accuracy: 69,57%
- Precision late class: 81,35%
- Recall late class: 57,73%
- F1 late class: 67,54%
- ROC-AUC: 75,63%
- Composite score: 64,2520%

Random Forest menang tipis karena recall untuk kelas late lebih tinggi. Dengan kata lain, Random Forest sedikit lebih baik dalam menangkap kasus order yang benar benar berisiko telat.

## 7. Kenapa Accuracy 69,57% Masuk Akal

Accuracy 69,57% harus dibaca dalam konteks model anti leakage. Model tidak diberi informasi yang baru diketahui setelah pengiriman selesai. Ini membuat hasilnya tidak terlihat terlalu tinggi, tetapi lebih jujur untuk use case operasional.

Ada beberapa alasan kenapa accuracy tidak mencapai angka sangat tinggi:

1. Banyak faktor penting tidak tersedia di dataset, seperti cuaca, kapasitas gudang, kapasitas carrier, jarak rute aktual, inventory issue, backlog harian, dan promosi besar.
2. Late delivery risk adalah masalah operasional yang kompleks dan noisy.
3. Target late risk cukup besar, yaitu 54,83%, sehingga baseline mayoritas kelas juga tidak rendah.
4. Model sengaja menghindari target leakage dari field post shipment.
5. Accuracy bukan metric utama karena yang lebih penting adalah kemampuan menangkap order yang berisiko telat.

Dengan demikian, angka 69,57% bukan tanda project gagal. Angka tersebut menunjukkan baseline realistis yang masih bisa dikembangkan dengan threshold tuning, LightGBM atau XGBoost, feature engineering tambahan, dan data operasional live.

## 8. Interpretasi Bisnis

Dari sisi bisnis, dashboard ini bisa digunakan sebagai decision support untuk tiga area.

Pertama, operational control. Tim fulfillment dapat memonitor kombinasi shipping mode, market, dan region dengan late rate tinggi.

Kedua, profit quality. Tim bisnis dapat membedakan segmen yang sekadar menghasilkan sales besar dari segmen yang benar benar memberikan margin sehat.

Ketiga, risk queue. Model scoring dapat menjadi baseline untuk membuat antrian order yang perlu dicek lebih awal. Misalnya order dengan probability risk tinggi dapat masuk monitoring queue sebelum dikirim.

## 9. Limitasi

Project ini memiliki beberapa limitasi.

- Dataset bersifat publik dan historis, bukan sistem live.
- Tidak ada data cuaca, kapasitas gudang, kapasitas carrier, live inventory, atau jarak rute aktual.
- Model masih baseline dan belum melalui hyperparameter tuning mendalam.
- Random Forest dipilih berdasarkan composite score sederhana, bukan cost function produksi.
- Dashboard adalah static portfolio dashboard, bukan aplikasi operasional dengan user login dan alert real time.
- Financial metrics mengikuti field dataset dan harus dibaca sebagai proxy, bukan laporan keuangan audited.

## 10. Pengembangan Lanjutan

Pengembangan berikutnya yang paling masuk akal:

1. Threshold tuning untuk menyesuaikan tradeoff recall dan workload.
2. PR-AUC untuk mengevaluasi kelas late risk dengan lebih fokus.
3. Cost-sensitive evaluation untuk membedakan biaya false negative dan false positive.
4. LightGBM atau XGBoost jika dependency stabil.
5. Calibration curve agar probability score lebih dapat dipercaya.
6. Dashboard simulator untuk melihat dampak threshold terhadap jumlah order yang masuk risk queue.
7. Integrasi data eksternal seperti cuaca, jarak pengiriman, kapasitas carrier, dan warehouse backlog.

## 11. Kesimpulan

Proyek Supply Chain Risk Intelligence menunjukkan bagaimana dataset publik dapat diubah menjadi portfolio analytics project yang lengkap. Proyek ini mencakup data engineering, exploratory analysis, machine learning, business intelligence, dashboard design, deployment, dan storytelling. Nilai utama project bukan hanya pada accuracy model, tetapi pada cara model dan dashboard disusun agar menjawab masalah bisnis yang realistis.

Random Forest dipilih karena lebih sesuai dengan prioritas operasional, yaitu menangkap order yang berisiko telat. Accuracy 69,57% dijelaskan sebagai konsekuensi dari pendekatan anti leakage dan penggunaan data publik yang tidak memuat seluruh faktor operasional. Dashboard kemudian digunakan untuk menerjemahkan hasil tersebut menjadi insight dan rekomendasi yang dapat dipahami oleh stakeholder.
