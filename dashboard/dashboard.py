import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
sns.set(style='dark')

def load_data():
    df = pd.read_csv("./dashboard/main_data.csv")
    df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
    return df

df = load_data()


st.sidebar.title("Dashboard Kualitas Udara Stasiun Guanyuan")
option = st.sidebar.selectbox(
    'Pilih Analisis yang Ingin Ditampilkan:',
    [ 'Distribusi Polutan', 'Korelasi Antar Variabel', 'Hubungan Polutan dengan Faktor Meteorologi', 'Pengaruh Faktor Terhadap PM2.5', 'Rata-rata PM2.5 per Tahun',]
)

if option == 'Distribusi Polutan':
    st.title("Distribusi Polutan")
    pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    plt.figure(figsize=(15, 10))
    for i, column in enumerate(pollutants, 1):
        plt.subplot(2, 3, i)
        sns.histplot(df[column], bins=30)
        plt.title(f'Distribusi {column}')
        plt.xlabel(column)
        plt.ylabel('Frekuensi')
    plt.tight_layout()
    st.pyplot(plt)

elif option == 'Korelasi Antar Variabel':
    st.title("Korelasi Antar Variabel")
    correlation_matrix = df[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm')
    plt.title('Korelasi antara Polutan dan Faktor Meteorologi')
    st.pyplot(plt)

elif option == 'Hubungan Polutan dengan Faktor Meteorologi':
    st.title("Hubungan Polutan dengan Faktor Meteorologi")
    x_column = st.selectbox('Pilih Faktor Meteorologi:', ['TEMP', 'PRES', 'DEWP'])
    y_column = st.selectbox('Pilih Polutan:', ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'])
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x=x_column, y=y_column)
    plt.title(f'Hubungan antara {x_column} dan {y_column}')
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.grid()
    st.pyplot(plt)



elif option == 'Pengaruh Faktor Terhadap PM2.5':
    st.title("Pengaruh Faktor Terhadap PM2.5")
    x = df[['TEMP', 'PRES', 'DEWP', 'RAIN']]
    y = df['PM2.5']

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    coefficients = pd.DataFrame(model.coef_, x.columns, columns=['Koefisien'])

    plt.figure(figsize=(10, 6))
    sns.barplot(x=coefficients.index, y='Koefisien', data=coefficients)
    plt.title('Pengaruh Faktor Terhadap PM2.5')
    plt.xlabel('Faktor')
    plt.ylabel('Koefisien')
    plt.xticks(rotation=45)
    st.pyplot(plt)
    st.write(coefficients)

elif option == 'Rata-rata PM2.5 per Tahun':
    st.title("Rata-rata PM2.5 per Tahun")
    average_pm25_per_year_df = df.groupby('year')['PM2.5'].mean().reset_index()

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=average_pm25_per_year_df, x='year', y='PM2.5', marker='o')
    plt.title('Pola Kualitas Udara di Guanyuan Selama Tiap Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Rata-rata PM2.5 (µg/m³)')
    plt.grid()
    st.pyplot(plt)
    st.write(average_pm25_per_year_df)