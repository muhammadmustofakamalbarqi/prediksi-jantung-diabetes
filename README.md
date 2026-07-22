# Prediksi Jantung & Diabetes

Aplikasi web skrining kesehatan berbasis Machine Learning menggunakan [Streamlit](https://streamlit.io/) untuk memperkirakan risiko **diabetes** dan **penyakit jantung** dari data klinis pasien.

## Fitur

- **Prediksi Diabetes** — model Decision Tree dengan 7 fitur (jumlah kehamilan, glukosa, tekanan darah, insulin, BMI, diabetes pedigree function, usia).
- **Prediksi Penyakit Jantung** — model Random Forest dengan 4 fitur (usia, jenis kelamin, tekanan darah, kolesterol).

## Cara Menjalankan

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Jalankan aplikasi:
   ```bash
   streamlit run web.py
   ```
3. Buka `http://localhost:8501` di browser (biasanya terbuka otomatis).

## Struktur File

| File | Keterangan |
|---|---|
| `web.py` | Aplikasi Streamlit utama |
| `jantung` | Model Random Forest (joblib) untuk prediksi jantung |
| `diabetes` | Model Decision Tree (joblib) untuk prediksi diabetes |
| `requirements.txt` | Daftar dependency Python |

## Disclaimer

Hasil prediksi bersifat indikatif untuk skrining awal dan **tidak menggantikan** diagnosis medis profesional. Konsultasikan ke dokter untuk pemeriksaan lebih lanjut.
