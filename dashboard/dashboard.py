import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi tampilan
sns.set(style='dark')

# Memuat dataset
day_df = pd.read_csv('https://raw.githubusercontent.com/DcCode46/dicoding/refs/heads/main/day.csv')
hour_df = pd.read_csv('https://raw.githubusercontent.com/DcCode46/dicoding/refs/heads/main/hour.csv')

# Konversi tanggal
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

# Sidebar untuk rentang waktu filter
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date, max_value=max_date, value=[min_date, max_date]
    )

# Filter data berdasarkan rentang waktu
filtered_df = day_df[(day_df['dteday'] >= str(start_date)) & (day_df['dteday'] <= str(end_date))]

# Mapping nama musim dan cuaca
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
weather_mapping = {1: "Clear", 2: "Cloudy", 3: "Rainy", 4: "Bad Weather"}
filtered_df['season'] = filtered_df['season'].map(season_mapping)
filtered_df['weathersit'] = filtered_df['weathersit'].map(weather_mapping)

# Informasi dataset
st.header('📊 Bike Rental Analysis 🚴‍♂️')
st.subheader('Informasi Dataset')
st.write(filtered_df.describe())

# Fungsi untuk plot penyewaan berdasarkan musim
def plot_rentals_by_season(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='season', y='cnt', data=df, estimator=np.mean, palette='coolwarm', ax=ax)
    ax.set_xlabel('Musim')
    ax.set_ylabel('Rata-rata Penyewaan Sepeda')
    ax.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Musim')
    st.pyplot(fig)

st.subheader('Penyewaan Sepeda Berdasarkan Musim')
plot_rentals_by_season(filtered_df)

# Fungsi untuk plot pengaruh cuaca terhadap penyewaan sepeda
def plot_weather_effect(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='weathersit', y='cnt', data=df, palette='Set2', ax=ax)
    ax.set_xlabel('Kondisi Cuaca')
    ax.set_ylabel('Jumlah Penyewaan')
    ax.set_title('Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda')
    st.pyplot(fig)

st.subheader('Pengaruh Cuaca terhadap Penyewaan Sepeda')
plot_weather_effect(filtered_df)

# Penyewaan berdasarkan hari dalam seminggu
def plot_rentals_by_weekday(df):
    weekday_mapping = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
                       4: "Thursday", 5: "Friday", 6: "Saturday"}
    df['weekday'] = df['weekday'].map(weekday_mapping)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='weekday', y='cnt', data=df, estimator=np.mean, palette='viridis', ax=ax)
    ax.set_xlabel('Hari dalam Seminggu')
    ax.set_ylabel('Rata-rata Penyewaan')
    ax.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Hari')
    st.pyplot(fig)

st.subheader('Penyewaan Sepeda Berdasarkan Hari dalam Seminggu')
plot_rentals_by_weekday(filtered_df)

# Penyewaan berdasarkan jam (data hourly)
def plot_rentals_by_hour(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x='hr', y='cnt', data=df, ci=None, marker='o', color='red', ax=ax)
    ax.set_xlabel('Jam')
    ax.set_ylabel('Jumlah Penyewaan')
    ax.set_title('Tren Penyewaan Sepeda Berdasarkan Jam')
    st.pyplot(fig)

st.subheader('Penyewaan Sepeda Berdasarkan Jam')
plot_rentals_by_hour(hour_df)

# Insight
st.subheader('📌 Insight')
st.write("1. Pola Penyewaan Sepeda Musiman \nJumlah penyewaan sepeda tertinggi terjadi pada musim gugur, diikuti oleh musim panas dan musim dingin. \nMusim semi memiliki penyewaan terendah, mungkin karena cuaca yang tidak stabil dengan suhu yang lebih rendah dan kemungkinan hujan yang lebih besar. \nMusim dingin memiliki jumlah penyewaan sepeda terendah.")
st.write("2. Pengaruh Cuaca terhadap Penyewaan Sepeda \nCuaca cerah memiliki jumlah penyewaan sepeda tertinggi, menunjukkan bahwa orang lebih suka bersepeda ketika cuaca baik.\nJika cuaca mendung, jumlah penyewaan sepeda sedikit turun dibandingkan dengan cuaca cerah, tetapi masih cukup tinggi.\nHujan secara signifikan menurunkan jumlah penyewaan sepeda, yang masuk akal karena kondisi jalan basah yang membuat bersepeda kurang nyaman.\nIni menunjukkan bahwa cuaca sangat memengaruhi keputusan pelanggan untuk menyewa sepeda, dengan preferensi yang jelas untuk kondisi yang lebih kering dan nyaman.")
st.write("3. Pola Umum Penggunaan Sepeda:\nMusim-musim menentukan penyewaan sepeda, dengan peningkatan pada musim panas dan gugur dan penurunan pada musim dingin dan semi.\nFaktor-faktor cuaca sangat memengaruhi keputusan pelanggan, dengan hujan sebagai faktor utama yang menyebabkan penurunan signifikan dalam penyewaan.\nSelain musim dan cuaca, ada pola harian dan jam tertentu di mana penyewaan meningkat, terutama pada pagi dan sore hari, ketika kemungkinan besar penyewaan akan berkurang.")
st.write("Dengan mempertimbangkan temuan ini, pengelola layanan penyewaan sepeda dapat mempertimbangkan cara yang lebih baik untuk beradaptasi dengan perubahan musiman dan kondisi cuaca. Misalnya, mereka dapat meningkatkan promosi musim semi untuk meningkatkan penyewaan, atau mereka dapat menyediakan fasilitas seperti jas hujan atau rute khusus untuk meningkatkan kenyamanan bersepeda saat cuaca mendung atau gerimis.")
