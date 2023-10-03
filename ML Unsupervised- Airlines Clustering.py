#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import datetime
import plotly.express as px
warnings.filterwarnings('ignore')

# menhhapus limit max column
pd.set_option('display.max_columns', None)

get_ipython().run_line_magic('matplotlib', 'inline')


# # Load and Describe Data

# -------------

# ## Load Data

# In[2]:


dfraw = pd.read_csv('flight.csv')
dfraw.head(3)


# In[3]:


# Mengubah nama kolom menjadi lower case
dfraw.columns = dfraw.columns.str.lower()


# **List Fitur pada Dataset**  
# 
# `member_no` : ID member  
# `ffp_date` : Frequent Flyer Program join date  
# `first_flight_date` : Tanggal penerbangan pertama  
# `gender` : Jenis kelamin  
# `ffp_tier` : Tier dari Frequent Flyer Program  
# `work_city` : Kota asal  
# `work_province` : Provinsi asal  
# `work_country` : Negara asal  
# `age` : Umur customer  
# `load_time` : Tanggal data diambil  
# `flight_count` : Jumlah penerbangan customer  
# `bp_sum` : Rencana perjalanan  
# `sum_yr_1` : Fare revenue  
# `sum_yr_2` : Votes prices  
# `seg_km_sum` : Total jarak(km) penerbangan yang sudah dilakukan  
# `last_flight_date` : Tanggal penerbangan terakhir  
# `last_to_end` : Jarak waktu penerbangan terakhir ke pesanan penerbangan paling akhir  
# `avg_internal` : Rata-rata jarak waktu  
# `max_interval` : Maksimal jarak waktu  
# `exchange_count` : Jumlah penukaran  
# `avg_discount` : Rata-rata discount yang didapat customer  
# `points_sum` : Jumlah poin yang didapat customer  
# `point_notflight` : Poin yang tidak digunakan oleh member

# ## Describe Data

# In[4]:


dfraw.info()


# 1. Terdapat 23 fitur dengan 62988 baris data  
# 2. Fitur dengan keterangan waktu (date) dirasa perlu diubah dari tipe data object ke tipe data datetime  
# 3. Fitur `member_no` sebaiknya diubah dari tipe data numerik ke object karena angka yang dimaksud hanyalah sebagai ID, bukan operasi matematika.
# 4. Fitur `age` sebaiknya diubah dari tipe data float ke integer
# 5. Terdapat beberapa fitur yang memiliki null value 

# In[5]:


# Mengubah tipe data int ke object
dfraw['member_no'] = dfraw['member_no'].astype(str)


# Dikarenakan sebelumnya pada saat mengubah tipe data ke datetime terdapat error seperti dibawah,  
# **ParserError: day is out of range for month: 2014/2/29  0:00:00 present at position 65**  
# 
# Maka, kita akan mengecek terlebih dahulu nilai yang dimaksud.

# In[6]:


dfraw[dfraw.last_flight_date.str.contains('2014/2/29')]


# Ternyata memang terdapat penulisan format tanggal yang berbeda pada fitur `last_flight_date`. Terdapat sebanyak 421 dari 62988 data atau hanya 0.006%, maka kita bisa menghapus baris error input ini.

# In[7]:


dfraw.drop(dfraw[dfraw.last_flight_date.str.contains('2014/2/29')].index, inplace = True)


# In[8]:


# Mengubah tipe data ke datetime
cols = ['ffp_date', 'first_flight_date', 'load_time','last_flight_date']
for col in cols:
    dfraw[col] = pd.to_datetime(dfraw[col])


# In[9]:


# Mengecek null value
dfraw.isnull().sum()


# In[10]:


dfraw.dtypes


# 1. Terdapat 6 fitur, yaitu `work_city`, `work_province`, `work_country`, `age`, `sum_yr_1`, dan `sum_yr_2` memiliki null value di dalamnya.
# 2. Semua fitur dirasa sudah tepat sesuai dengan tipe data nya.  
# 3. Untuk fitur `age`, dikarenakan terdapat NA values, maka tipe data akan diubah ketika sudah handle missing values. 

# In[11]:


# Mengecek duplicated rows
dfraw.duplicated().sum()


# In[12]:


# Mengkategorikan fitur sesuai dari tipe data
num = ['ffp_tier', 'age', 'flight_count', 'bp_sum', 'sum_yr_1', 'sum_yr_2', 'seg_km_sum', 'last_to_end', 'avg_interval', 'max_interval', 'exchange_count', 'avg_discount', 'points_sum', 'point_notflight']
cat = ['member_no','ffp_date', 'first_flight_date', 'gender', 'work_city', 'work_province', 'work_country', 'load_time', 'last_flight_date']

# Membatasi angka setelah koma hingga hanya 3 angka
pd.set_option('display.float_format', lambda x: '%.3f' % x)

dfraw[num].describe()


# Secara keseluruhan, dataset tidak memiliki distribusi data yang terlalu luas. Meskipun ada beberapa fitur yang memiliki nilai min-max yang sangat jauh, namun hal ini terkesan wajar jika kita bandingkan dengan kasus di dunia nyata dimana pasti ada orang-orang yang sering melakukan penerbangan dan di sisi lain juga ada orang-orang yang jarang melakukan penerbangan.  
# 
# Beberapa hal yang mungkin perlu perhatian adalah :  
# 1. Kebanyakan fitur numerik memiliki nilai Mean > Median dan nilai Min-Max yang cukup jauh  
# 2. Fitur `age` kelihatan tidak normal dimana nilai maksimum umur nya adalah 110 tahun  
# 3. Fitur `avg_discount` yang sepertinya juga tidak normal yaitu nilai maksimum nya 1.5 atau bisa diartikan 150% diskon.  
# 4. Fare revenue yang terlihat di fitur `sum_yr_1` dan `sum_yr_2` memiliki nilai 0. Hal ini perlu dianalisis lebih lanjut.

# In[13]:


dfraw[cat].describe()


# 1. Kebanyakan data nya adalah data waktu (date/time) dimana hal tersebut pasti bervariasi yang menyebabkan unique value terhitung banyak. Namun hanya terdapat 1 unique value pada fitur load_time dimana hal tersebut merupakan tanggal data diambil, yaitu 3/31/2014.  
# 2. Kebanyakan penumpang berasal dari China dan berjenis kelamin laki-laki.  
# 3. Sudah dipastikan bahwa tidak ada data duplikat atau semua unique value dari `member_no` sudah sesuai.  
# 4. Output first dan last hanya terlihat untuk fitur yang bertipe datetime.

# --------

# # EDA (Exploratory Data Analysis

# --------

# ## Univariate Analysis

# ### Check unique Values

# In[14]:


dfraw['ffp_tier'].unique()


# Ada 3 tipe tier, yaitu 4, 5, dan 6

# In[15]:


dfraw['work_city'].unique()


# In[16]:


dfraw['work_province'].unique()


# Terdapat fitur-fitur kategorical yang perlu dilakukan data cleansing berupa penyamarataan penulisan string.

# ### Distribusi Data

# In[17]:


# Melihat grafik distribusi

plt.figure(figsize=(20, 16))
for i in range(0, len(num)):
    plt.subplot(4, 4, i+1)
    sns.distplot(dfraw[num[i]], color='blue')
    plt.tight_layout()


# ### Check Outliers

# In[18]:


# Melihat penampilan outlier

plt.figure(figsize=(12, 6))
for i in range(0, len(num)):
    plt.subplot(2, 7, i+1)
    sns.boxplot(dfraw[num[i]], color='red', orient='v')
    plt.title(num[i])
    plt.tight_layout()


# 1. Fitur `ffp_tier` pada dasarnya tidak memiliki outlier dikarenakan hanya memiliki 3 nilai yaitu 4, 5, dan 6.  
# 2. Fitur lainnya memiliki distribusi right-skewed dan outliers.  
# 3. Hampir semua fitur memiliki outliers. Hal ini mungkin bisa ditangani dengan menghapus nilai ekstrim dan juga feature selection yang tepat.

# ### Abnormal Value

# **1. Avg Discount**

# In[19]:


# Membuat Plot Avg_Diskon yang memiliki nilai terkesan janggal
plt.figure(figsize=(6, 4))
sns.distplot(dfraw.avg_discount)
plt.title('Avg Discount')


# In[20]:


dfraw[dfraw['avg_discount'] > 1.0]


# In[21]:


dfraw[dfraw['avg_discount'] == 0.0]


# Mendapatkan diskon 100% saja mungkin jarang terdengar, terlebih lagi jika mendapatkan diskon lebih dari 100% (read: > 1.0). Terdapat 3684 customer yang mendapatkan diskon >=1. Jika kita mengasumsikan diskon didapat karena penerbangan-penerbangan yang mereka lakukan, maka juga tidak bisa dikatakan benar karena customer tersebut juga ada yang memiliki total poin rendah dan jarak waktu dari penerbangan terakhir yang cukup lama. Oleh karena itu, dikarenakan hanya terdapat (2927+8) dari 62k++ data (0.06%) maka data ini akan dianggap sebagai error input dan akan dihapus.  
# 
# Hal yang sama juga terkesan tidak wajar pada avg_discount yang 0, dimana total penerbangan nya (`seg_km_sum`) tidak 0 dan ada yang memiliki poin (`points_sum`). Maka, data-data ini akan dihapus karena dianggap tidak wajar dan error input.

# **2. Age**

# In[22]:


plt.figure(figsize=(30,6))
sns.set(style='whitegrid')
ax = sns.countplot(x='age', width = 0.5, data=dfraw, palette='rocket')
ax.set_title('Age Distribution', fontsize=8, fontweight='bold')
ax.set_xlabel('Age', fontsize=7, fontweight='medium')


# In[23]:


dfraw[dfraw.age > 100]


# Customer yang berusia antara 28-56 tahun cenderung sering melakukan perjalanan menggunakan pesawat.  
# Namun, juga tidak wajar jika ada customer yang berusia lebih dari 100 tahun, sehingga kita menganggap bahwa ini adalah error input yang masuk sebagai kategori outliers.

# **3. Fare Revenue**

# In[24]:


dfraw[(dfraw.sum_yr_1 == 0) & (dfraw.sum_yr_2 == 0) & (dfraw.seg_km_sum > 0)]


# Kita menemukan lagi indikasi error input dimana fare revenue `sum_yr_1`, `sum_yr_2` yang memiliki nilai 0 padahal penumpang melakukan perjalanan `seg_km_sum`. Hal ini tentu tidak wajar jika ada perjalanan namun tidak ada revenue. Dikarenakan terdapat 245 dari 52931 data (0.004%) data, maka kita akan menghapusnya.

# ## Multivariate Analysis

# ### Korelasi Fitur Numerik

# In[25]:


# Plot korelasi heatmap
corr_matrix = dfraw.corr()
plt.figure(figsize=(8, 8))
sns.heatmap(corr_matrix, annot=True, annot_kws={'size': 10}, fmt='.2f', cmap='coolwarm', center=0)
plt.title('Correlation Heatmap')
plt.show()


# 1. Fitur `age`, `last_to_end`, `avg_interval`, `max_interval`, `avg_discount`, `point_notflight` terlihat tidak memiliki korelasi yang kuat (<0.5)  
# 2. Fitur-fitur yang memiliki korelasi kuat yaitu `flight_count`, `bp_sum`, `sum_yr_1`, `sum_yr_2`, `seg_km_sum`, `points_sum`.  
# 3. Fitur `bp_sum`, `seg_km_sum`, dan `points_sum` memiliki korelasi yang sangat kuat, redundan.  

# In[26]:


# Visualisasi Fare Revenue dari Jumlah Penerbangan Berdasarkan Total Poin

plt.figure(figsize=(12, 6))
scatter = sns.scatterplot(data=dfraw, x='sum_yr_1', y='flight_count', hue='age', size='age', palette='rocket_r')
plt.title('Fare Revenue')
plt.show()


# 1. Sama seperti analisis sebelumnya dimana umur customer yang aktif melakukan perjalanan adalah usian 20-an keatas hingga 60 tahun. 
# 2. Jumlah fare revenue yang didapat juga berbanding lurus dengan jumlah penerbangan yang dilakukan.  
# 3. Fare revenue yang sering didapatkan adalah dibawah 50000.

# ----------

# # Data Preparation

# ----------

# ## Data Cleansing

# ### Dropping

# **Duplicated Rows**

# Pada tahap Data Exploration sebelumnya, terlihat bahwa tidak ada duplicate rows sehingga tidak perlu penanganan.

# ### Rows with Abnormal Value (Outliers)

# Pada tahap sebelumnya kita sudah menandai fitur-fitur yang memiliki nilai tidak normal, sehingga perlu dilakukan pengecekan dan penanganan lebih lanjut dikarenakan dapat terindikasi sebagai outliers. Nilai-nilai tersebut adalah :  
# 1. `avg_discount` yang memiliki nilai 0 dan lebih dari 1.    
# 2. `age` yang berumur 110 atau lebih dari 100 tahun.  
# 3. `sum_yr_1` dan `sum_yr_2` yang memiliki fare revenue 0.

# In[27]:


df_clean = dfraw.copy()


# In[28]:


df_clean.head(3)


# In[29]:


# Drop 0 avg_discount
nol_disc = df_clean[((df_clean.avg_discount == 0.0))].index
df_clean = df_clean.drop(nol_disc)


# In[30]:


# Drop >1 avg_discount
satu_disc = df_clean[((df_clean.avg_discount > 1.0))].index
df_clean = df_clean.drop(satu_disc)


# In[31]:


# Drop >100 age
abn_age = df_clean[((df_clean.age > 100))].index
df_clean = df_clean.drop(abn_age)


# In[32]:


# Drop rows
abn_fare = df_clean[(df_clean.sum_yr_1 == 0) & (df_clean.sum_yr_2 == 0) & (df_clean.seg_km_sum > 0)].index
df_clean = df_clean.drop(abn_fare)


# In[33]:


df_clean.shape


# ### Handle Missing Value

# In[34]:


# Mengecek kembali null value
df_clean.isnull().sum()


# Terdapat 7 fitur yang memiliki Null value, yaitu `gender`, `work_city`, `work_province`, `work_country`, `age`, `sum_yr_1`, `sum_yr_2`. 
#  
# 1. Fitur `gender` yang hanya memiliki 1 null value akan dihapus.
# 2. Fitur `work_city`, `work_province`, `work_country` akan diisi dengan nilai modus.  
# 2. `age` yang memiliki persebaran data yang lumayan normal, maka akan diisi dengan nilai mean. 
# 3. `sum_yr_1` dan `sum_yr_2` akan diisi dengan nilai median.

# In[35]:


mode_value = df_clean.filter(['work_city', 'work_province', 'work_country']).mode()
cols = ['work_city', 'work_province', 'work_country']

df_clean[cols] = df_clean[cols].fillna(df_clean.mode().iloc[0])


# In[36]:


df_clean['age'] = df_clean['age'].fillna(df_clean['age'].mean())


# In[37]:


df_clean['sum_yr_1'] = df_clean['sum_yr_1'].fillna(df_clean['sum_yr_1'].median())


# In[38]:


df_clean['sum_yr_2'] = df_clean['sum_yr_2'].fillna(df_clean['sum_yr_2'].median())


# In[39]:


df_clean.dropna(axis=0, inplace=True)
df_clean.isnull().sum()


# In[40]:


df_clean['age'] = df_clean['age'].astype(int) 


# ## Feature Engineering

# ### Feature Extraction

# #### Durasi Menjadi Member

# Dibuat untuk mengetahui sudah berapa lama setiap user telah bergabung ke program FFP (Frequent Flyer Program) dengan menghitung jarak dari `load_time` (data diambil) dan `ffp_date` (kapan join).

# In[41]:


df_clean['day_as_member'] = (df_clean['load_time'] - df_clean['ffp_date']).dt.days
df_clean.head(2)


# In[42]:


df_clean.shape


# ### Feature Selection

# #### RFM ANALYSIS

# Pada proses Feature Selection kali ini, akan dilakukan analisa RFM (Recency, Frequency, Monetary value) sebagai patokan dalam pemilihan fitur-fitur yang akan digunakan selanjutnya. <br>
# * Recency mengacu pada waktu terakhir pengguna melakukan transaksi <br>
# `last_to_end`: Dipilih karena berisi informasi mengenai selisih hari antara tainggal pengambilan data dengan tanggal penerbangan terakhir <br> <br>
# * Frequency mengacu pada seberapa sering pengguna melakukan transaksi <br>
# `flight_count` : Dipilih karena berisi data jumlah penerbangan yang telah dilakukan pengguna <br> <br>
# * Monetary value mengacu pada seberapa banyak yang dikeluarkan tiap pengguna pada keseluruhan transaksi <br>
# `seg_km_sum` : Dipilih karena memuat data total jarak penerbangan yang telah ditempuh setiap pengguna yang dapat menggambarkan banyaknya transaksi dan pengeluaran yang telah dikeluarkan, karena jarak sangat mempengaruhi biaya setiap tiket yang harus dikeluarkan.

# #### OTHER CONSIDERATION

# Selain dari fitur-fitur yang telah dipilih berdasarkan pada RFM Analysis, dipilih beberapa fitur tambahan yang dianggap memiliki pengaruh yang cukup besar, beberapa diantaranya : <br>
# * `day_as_member` : Dipilih karena menunjukkan seberapa lama pengguna telah bergabung menjadi member
# * `points_sum` : Dipilih karena berisi jumlah poin yang dimiliki oleh tiap pengguna yang pada umumnya diperoleh setiap melakukan transaksi

# #### Handle Outliers 

# In[43]:


def outlier_del(df, column, mode):
    q1 = df.iloc[:,column].quantile(0.25)
    q3 = df.iloc[:,column].quantile(0.75)
    iqr = q3-q1
    lower_tail = q1 - (1.5 * iqr)
    upper_tail = q3 + (1.5 * iqr)
    nama_kolom = df.columns[column]
    jumlah_outliers = df[(df.iloc[:,column] <= lower_tail)|(df.iloc[:,column] >= upper_tail)].iloc[:,column].count()
    total_row = df.iloc[:,column].count()
    persentase_outliers = round(((jumlah_outliers/total_row)*100),2)
    if mode == 'summary':
        return print('Jumlah Outliers pada kolom ', nama_kolom, ' :', jumlah_outliers, ' dan persentase outliers:', persentase_outliers, '%')
    elif mode == 'df':
        return df[(df.iloc[:,column] >= lower_tail)&(df.iloc[:,column] <= upper_tail)]
    else :
        return print('periksa mode yang diinputkan')


# In[44]:


# Memeriksa presentase outlier setiap kolom
column = [10, 14, 16, 21, 23]

for i in range(0, len(column)):
    outlier_del(df_clean, column[i], 'summary')


# In[45]:


# Penghapusan Outlier
df_clean = df_clean[df_clean.index.isin(outlier_del(df_clean, 10, 'df').reset_index()['index'])]
df_clean = df_clean[df_clean.index.isin(outlier_del(df_clean, 14, 'df').reset_index()['index'])]
df_clean = df_clean[df_clean.index.isin(outlier_del(df_clean, 16, 'df').reset_index()['index'])]
df_clean = df_clean[df_clean.index.isin(outlier_del(df_clean, 21, 'df').reset_index()['index'])]

print(f'Total baris setelah menghapus outlier: {len(df_clean)}')


# In[46]:


df_select = df_clean.copy()


# In[47]:


df_select = df_select[['flight_count', 'seg_km_sum', 'last_to_end', 'points_sum', 'day_as_member']]
df_select.head(2)


# ## Normalisasi Data

# In[48]:


from sklearn.preprocessing import StandardScaler

# Proses normalisasi Data
scaler = StandardScaler()
feat_std = scaler.fit_transform(df_select)

# Memasukkan hasil normalisasi ke dalam DataFrame df_std
for i, col in enumerate(df_select):
    df_select['std_' + col] = feat_std[:, i]


# In[49]:


df_select.describe()


# In[50]:


df_std = df_select.copy()


# In[51]:


# Menghapus Kolom 

df_std.drop(columns= ['last_to_end', 'flight_count', 'seg_km_sum', 'day_as_member', 'points_sum'], inplace= True)
df_std.head(3)


# ------------

# # Clustering

# ------------

# ## Inertia Check

# In[52]:


from sklearn.cluster import KMeans

# Mnghitung nilai inertia untuk 2 hingga 10 cluster
inertia = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=0)
    kmeans.fit(df_std)
    inertia.append(kmeans.inertia_)

    
# Visualisasi inertia
sns.set_style('white')
plt.figure(figsize= (10, 5))
sns.lineplot(x= range(1, 11), y= inertia, marker='o', color = '#000087', linewidth = 3)
sns.scatterplot(x=range(1, 11), y=inertia, s=300, color='#800000',  linestyle='--')
plt.title('Visualisasi Inertia')


# In[53]:


# Melihat perbedaan presentase inertia untuk setiap penambahan cluster

((pd.Series(inertia) - pd.Series(inertia).shift(-1)) / pd.Series(inertia) * 100).dropna()


# ## Silhouette Score

# In[54]:


from sklearn.metrics import silhouette_score

# Menghitung silhouette score untuk 2 hingga 10 cluster
range_n_clusters = list(range(2,11))
arr_silhouette_score_euclidean = []
for i in range_n_clusters:
    kmeans = KMeans(n_clusters=i).fit(df_std)
    cluster_labels = kmeans.predict(df_std)
     
    score_euclidean = silhouette_score(df_std, cluster_labels, metric='euclidean')
    arr_silhouette_score_euclidean.append(score_euclidean)

# Plot hasil Silhouette Score
sns.set_style('white')
plt.figure(figsize=(8, 6))
sns.lineplot(x=range(2,11), y=arr_silhouette_score_euclidean,  marker='o', color='#000087', linewidth = 4)
sns.scatterplot(x=range(2,11), y=arr_silhouette_score_euclidean, s=300, color='#800000',  linestyle='--')
plt.xlabel('Jumlah Cluster')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Score')
plt.show()


# Dari hasil Silhouette score diatas, terlihat bahwa jumlah cluster yang optimal adalah 4 clusters.

# ## Clusters

# In[55]:


from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=4, random_state=0).fit(df_std) 

clusters = kmeans.labels_


# ## Evaluasi Cluster

# In[56]:


# PCA dan Visualisasi Cluster yang Dihasilkan

from sklearn.decomposition import PCA 

pca = PCA(n_components=2)
pca.fit(df_std)
pcs = pca.transform(df_std)

df_pca = pd.DataFrame(data = pcs, columns = ['PC 1', 'PC 2'])
df_pca.head()


# In[57]:


# Visualisasi hasil cluster menggunakan Silhouette Visualizer
from yellowbrick.cluster import SilhouetteVisualizer

model = KMeans(4)
visualizer = SilhouetteVisualizer(model)

visualizer.fit(df_pca)    
visualizer.show()   


# Dari gambar diatas terlihat bahwa seluruh clusters memiliki koefisien value yang bagus. Artinya model yang dibuat sudah sangat ideal.

# In[58]:


df_pca['clusters'] = clusters
df_pca.sample(5)


# In[59]:


# Visualisasi persebaran cluster 

fig, ax = plt.subplots(figsize=(10,6))

sns.scatterplot(
    x='PC 1', y='PC 2',
    hue='clusters',
    linestyle='--',
    data=df_pca,
    marker = '+',
    palette=['blue','red','green','yellow'],
    s=50,
    ax=ax
)


# **Menempelkan Label Cluster ke Dataset**

# In[60]:


# Assign cluster ke dataset 
df_clean.loc[:,'clusters'] = kmeans.labels_
df_clean.sample(5)


# In[61]:


df_clean['clusters'].value_counts().to_frame().reset_index().rename(columns={"index": "clusters", "clusters": "total_members"})


# In[62]:


# Menampilkan statistik tiap cluster
df_select['clusters'] = clusters
display(df_select.groupby('clusters').agg(['min', 'max','mean','median']))


# ## Tentang Clusters

# Penjelasan masing-masing cluster adalah sbb :
# 
# #### Cluster 0 : 
# Pelanggan dalam cluster ini lebih cenderung melakukan jumlah penerbangan yang stabil dengan rata - rata 5–6 penerbangan dengan jarak yang relatif pendek dan rata-rata 122 poin. Cluster ini memiliki masa keanggotaan yang tidak terlalu panjang atau bisa dikatakan baru bergabung diantara pelanggan cluster lainnya.
# 
# #### Cluster 1 :
# Pelanggan dalam cluster ini memiliki ciri-ciri seperti cluster 0, namun rata-rata poin yang didapatkan lebih tinggi dari cluster 0 yaitu 146 poin. Pelanggan yang tergabung dalam cluster ini juga bukan anggota lama atau dapat dikatakan baru bergabung. Mungkin karena data yang tercatat baru sedikit (data penerbangan sejak program diinput) yang menyebabkan cluster 0 dan 1 masih belum memiliki jumlah penerbangan yang tinggi. 
# Kedua cluster tersebut berpotensi untuk bisa diupgrade lagi dikarenakan jumlah penerbangan yang mereka lakukan cukup baik meskipun baru bergabung.
# 
# #### Cluster 2 :
# Pelanggan yang tergolong pada cluster 2 adalah mereka yang melakukan perjalanan lebih sedikit dengan jarak yang relatif pendek pula, namun poin yang dimiliki tinggi. Selain itu, mereka sudah bergabung dengan program lebih lama dari cluster 0 dan 1. Artinya mereka memiliki loyalitas yang bagus karena tetap bergabung menjadi keanggotaan namun jarang melakukan perjalanan. 
# 
# #### Cluster 3 :
# Pelanggan terbaik adalah pelanggan yang berada di cluster 3. CLuster ini memiliki jumlah penerbangan yang lebih tinggi dari cluster lainnya dengan rata-rata 15–16 kali penerbangan dengan jarak yang jauh pula. Besar kemungkinan pelanggan cluster ini sering melakukan perjalanan internasional. Selain itu jumlah poin yang mereka dapatkan juga tinggi karena mereka sudah lama bergabung menjadi keanggotaan.

# ## Rekomendasi Bisnis

# #### Cluster 0 dan 1 (Potential Customers)  
# Dikarenakan cluster 0 dan 1 merupakan potential customer dimana mereka sering melakukan perjalanan walaupun baru bergabung menjadi anggota, maka fokus peningkatan revenue lebih kearah mempertahankan mereka agar terus menjadi anggota dan memberikan reward yang menarik agar mereka tetap sering melakukan perjalanan.  Maka rekomendasi bisnis nya yaitu :   
# **1. Birthday Coupon**  
# Memberikan diskon penerbangan di bulan ulang tahun pelanggan hingga 15% sesuai dengan jumlah poin yang mereka dapatkan. Keuntungan lainnya adalah jika melakukan perjalanan tepat di hari ulang tahun, maka mereka akan mendapatkan double points.  
# **2. Penukaran Poin**  
# Setiap pelanggan yang telah mencapai jumlah poin tertentu, berkesempatan untuk menukar poin nya menjadi kupon belanja atau kupon penginapan di mitra perusahaan.          
# **3. Afiliasi Paket Wisata** 
# Menawarkan program afiliasi dimana pelanggan yang berhasil membawa minimal 2 orang menjadi anggota akan mendapatkan diskon harga paket wisata bersama orang yang mereka ajak.    
# 
# #### Cluster 2 (Loyal Customers)  
# Dikarenakan cluster 2 merupakan cluster dimana pelanggan sudah cukup lama menjadi anggota namun sedkit melakukan perjalanan, maka fokus kita adalah bagaimana cara mereka agar sering melakukan perjalanan. Beberapa rekomendasi bisnis nya yaitu :  
# **1.  Inactive Treatment**  
# Pelanggan yang sudah tidak melakukan perjalanan hingga 6 bulan akan diberikan penawaran khusus dimana jika mereka melakukan perjalanan di antara batas waktu yang ditetapkan, maka mereka akan mendapatkan diskon sebesar 10% dan double points. Hal ini bertujuan agar meminimalisir pelanggan yang inactive.  
# **2. Couple Package**  
# Buat paket perjalanan khusus untuk 2 orang, baik bersama pasangan, sahabat, atau dengan yang lain. Masing-masing dari mereka akan mendapatkan diskon 5% dan double points. Hal ini bertujuan agar setiap hari nya banyak penumpang yang melakukan perjalanan.  
# **3. Tour Package**  
# Penawaran spesial untuk mereka yang melakukan perjalanan dan ingin berwisata. Mereka akan mendapatkan diskon khusus dan pelayanan yang baik dari mitra perusahaan.  
# 
# #### Cluster 3 (Exclusive Customers)  
# Tentu saja pelanggan di cluster 3 ini adalah pelanggan eksklusif yang harus dijaga dengan baik. Mereka membelanjakan uang menggunakan layanan perusahaan sehingga fokus peningkatan bisnis nya adalah menjaga agar mereka terus menggunakan penerbangan perusahaan. Beberapa rekomendasi bisnisnya yaitu :  
# **1. First Priority**  
# Menjadikan pelanggan cluster ini sebagai prioritas utama, seperti misalnya prioritas kursi, makanan dan minuman gratis, dan diskon yang lebih besar dibanding cluster lainnya.  
# **2. Luxury Service**  
# Mempromosikan perjalanan international mewah. Tawarkan paket perjalanan mewah dengan fasilitas premium seperti akomodasi bintang lima, penerbangan kelas satu, dan layanan pribadi yang disesuaikan.  
# **3. Half Price Refund**  
# Keuntungan istimewa yang dimiliki cluster ini selain prioritas dan luxury service adalah berkesempatan untuk bisa refund 50% di hari yang sama dengan minimum jumlah poin tertentu.  
# 
# #### Untuk semua cluster** 
# **1. Mengembangkan aplikasi seluler**  
# Mengembangkan aplikasi seluler untuk mempermudah pelanggan dalam mengakses informasi penerbangan, poin, dan penawaran eksklusif yang hanya bisa optimal digunakan melalui aplikasi.  
# **2. Gamification**  
# Berikan peningkatan kelas atau fasilitas khusus kepada pelanggan yang telah mencapai poin tertentu untuk dapat menikmati promo atau diskon kecil.  
# **3. Seasons Promotion**  
# Rencanakan promosi musiman yang sesuai dengan liburan dan peristiwa khusus, seperti diskon hari raya keagamaan, penawaran khusus tahun baru, atau hari besar lainnya.

# In[ ]:




