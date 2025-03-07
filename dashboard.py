import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi tampilan
sns.set(style='dark')

# Memuat dataset
day_df = pd.read_csv('/mnt/data/day.csv')
hour_df = pd.read_csv('/mnt/data/hour.csv')

# Sidebar untuk rentang waktu filter
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date, max_value=max_date, value=[min_date, max_date]
    )

# Filter data berdasarkan rentang waktu
filtered_df = day_df[(day_df['dteday'] >= str(start_date)) & (day_df['dteday'] <= str(end_date))]

# Informasi dataset
st.header('Bike Rental Analysis 🚴‍♂️')
st.subheader('Informasi Dataset')
st.write(filtered_df.describe())

# Fungsi untuk plot penyewaan berdasarkan musim
def plot_rentals_by_season(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='season', y='cnt', data=df, estimator=np.mean, palette='coolwarm', ax=ax)
    ax.set_xlabel('Musim')
    ax.set_ylabel('Rata-rata Penyewaan Sepeda')
    ax.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Musim')
    ax.set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'])
    st.pyplot(fig)

st.subheader('Penyewaan Sepeda Berdasarkan Musim')
plot_rentals_by_season(filtered_df)

# Fungsi untuk plot pengaruh cuaca terhadap penyewaan sepeda
def plot_weather_effect(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(x='weathersit', y='cnt', data=df, palette='Set2', ax=ax)
    ax.set_xlabel('Kondisi Cuaca')
    ax.set_ylabel('Jumlah Penyewaan')
    ax.set_title('Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda')
    ax.set_xticklabels(['Cerah', 'Berkabut', 'Hujan Ringan', 'Hujan Lebat'])
    st.pyplot(fig)

st.subheader('Pengaruh Cuaca terhadap Penyewaan Sepeda')
plot_weather_effect(filtered_df)

# Insight
st.subheader('Insight')
st.write("1. Penyewaan sepeda cenderung lebih tinggi pada musim gugur dan lebih rendah di musim semi.")
st.write("2. Kondisi cuaca yang lebih cerah meningkatkan jumlah penyewaan sepeda, sedangkan hujan lebat menguranginya secara signifikan.")

st.caption('Copyright © Dicoding 2023')
