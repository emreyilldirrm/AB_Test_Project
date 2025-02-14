#####################################################
# AB Testi ile BiddingYöntemlerinin Dönüşümünün Karşılaştırılması
#####################################################

#####################################################
# İş Problemi
#####################################################

# Facebook kısa süre önce mevcut "maximumbidding" adı verilen teklif verme türüne alternatif
# olarak yeni bir teklif türü olan "average bidding"’i tanıttı. Müşterilerimizden biri olan bombabomba.com,
# bu yeni özelliği test etmeye karar verdi veaveragebidding'in maximumbidding'den daha fazla dönüşüm
# getirip getirmediğini anlamak için bir A/B testi yapmak istiyor.A/B testi 1 aydır devam ediyor ve
# bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.Bombabomba.com için
# nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchasemetriğine odaklanılmalıdır.




#####################################################
# Veri Seti Hikayesi
#####################################################

# Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları
# reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır.Kontrol ve Test
# grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleriab_testing.xlsxexcel’ininayrı sayfalarında yer
# almaktadır. Kontrol grubuna Maximum Bidding, test grubuna AverageBiddinguygulanmıştır.

# impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç



#####################################################
# Proje Görevleri
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# 1. Hipotezleri Kur
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı (shapiro)
#   - 2. Varyans Homojenliği (levene)
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi
# 4. p-value değerine göre sonuçları yorumla
# Not:
# - Normallik sağlanmıyorsa direkt 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.


import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # veya 'QtAgg'
import matplotlib.pyplot as plt
from scipy.stats import shapiro, levene ,ttest_ind,mannwhitneyu
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)
pd.set_option('display.width', 1000)

#####################################################
# Görev 1:  Veriyi Hazırlama ve Analiz Etme
#####################################################

# Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz.
# Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.
df_C = pd.read_excel("datasets/ab_testing.xlsx",sheet_name="Control Group")
df_C.head()

df_T = pd.read_excel("datasets/ab_testing.xlsx",sheet_name="Test Group")
df_T.head()
# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.
df_C.describe().T
df_T.describe().T
# impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç

# c grubunda 550.89406 mean 531.20631  median birbirine yakın duruyor veri içerisinde çok aykırı durumlar söz konusu olmayabilir
# 582.10610 551.35573  T grubunda ortalama ve median birbirine yakın duruyor veri içerisinde çok aykırı durumlar söz konusu olmayabilir

# std her iki grupta aynı diyebileceğimiz bir derecede ve min ve max değereleri her iki grupta makul seviyelerde normal dağılıyor gibi
plt.hist(df_C["Purchase"],bins=25,alpha=0.6)
plt.show()

plt.hist(df_T["Purchase"],bins=25,alpha=0.6)
plt.show()

# Grafikte gördüğümüz gibi Normal dağılım var veri noktalarının yayılımı her bölgede benzer (homojenliğin) olmasının bir işareti olabilir
# ama Levene Testi veya Bartlett Testi ile homojenliğe bakılır

# Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.

df = pd.concat([df_C,df_T],ignore_index=True)
df.shape



#####################################################
# Görev 2:  A/B Testinin Hipotezinin Tanımlanması
#####################################################

# Adım 1: Hipotezi tanımlayınız.
# H0 : M1 == M2 Tıklanan reklamlar sonrası satın alınan ürün sayısı istatistiksel olarak anlamlı bir fark yoktur
# H0 : M1 != M2 Tıklanan reklamlar sonrası satın alınan ürün sayısı istatistiksel olarak anlamlı bir fark vardır

# Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz
df_C["Purchase"].mean()
df_T["Purchase"].mean()
#####################################################
# GÖREV 3: Hipotez Testinin Gerçekleştirilmesi
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################


# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.
# Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz
# Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz
# Adım 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma
# ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.



# H0 : Normal dağılım varsayımı sağlanmaktır.
# H1 : Normal dağılım varsayımı sağlanmamaktadır.
# p-value < ise 0.05'ten H0 RED edilir
# p-value > ise 0.05' H0 REDDEDİLEMEZ

test_stats ,pvalue = shapiro(df_C["Purchase"])
print('Test Stat = %.4f , p-value = %.4f'%(test_stats,pvalue))

test_stats ,pvalue = shapiro(df_T["Purchase"])
print('Test Stat = %.4f , p-value = %.4f'%(test_stats,pvalue))

# pvalue 0.05"ten büyüktür H0 REDDEDİLEMEZ Normal dağılım varsayımı sağlanmaktır.
# Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)

# VARYANS HOMOJENLİĞİ NORMAl DAĞILIM SAĞLANDIĞINDA YAPILIR
# p-value < ise 0.05'ten H0 RED edilir
# # p-value > ise 0.05' H0 REDDEDİLEMEZ

# H0 : varyans homojen olarak dağılım sağlamaktadır
# H1 : varyans homojen olarak dağılım sağlamamaktadır

test_stat,pvalue = levene(df_C["Purchase"],df_T["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# H0 REDDEDİLEMEZ varyans homojen olarak dağılım sağlamaktadır.

test_stats,pvalue = ttest_ind(df_C["Purchase"],df_T["Purchase"],
                              equal_var=True) #equal_var=False varsayanslar homojen değilse false yapılır
                                               #homojen ise true yapılır
print('Test Stat = %.4f , p-value = %.4f'%(test_stats,pvalue))


# p-value = 0.3493
# p-value < ise 0.05'ten H0 RED edilir
# # p-value > ise 0.05' H0 REDDEDİLEMEZ
# H0 : M1 == M2 Tıklanan reklamlar sonrası satın alınan ürün sayısı istatistiksel olarak anlamlı bir fark yoktur
# H0 : M1 != M2 Tıklanan reklamlar sonrası satın alınan ürün sayısı istatistiksel olarak anlamlı bir fark vardır

# H0 REDDEDİLEMEZ Tıklanan reklamlar sonrası satın alınan ürün sayısı istatistiksel olarak anlamlı bir fark yoktur

##############################################################
# GÖREV 4 : Sonuçların Analizi
##############################################################

# Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.
# Varsayımlar sağlandığı için bağımsız iki örneklem t testi (parametrik test)
# equal_var parametresini True ayarladım varsayanslar homojen olduğu için




# Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.
# H0 REDDEDİLEMEZ Tıklanan reklamlar sonrası satın alınan ürün sayısı istatistiksel olarak anlamlı bir fark yoktur.
# Yani "average bidding"’i kulanmak için ek bir maliyete gerek yoktur kurulu düzen ile devam edilebilir.
