# OSIsoft-Time-Series-Forecasting

PI System Demo Tagleri'nden biri olan "BA:TEMP.1" verileriyle bir makine öğrenmesi algoritması geliştirilmesi hedeflenmiştir.
Algoritma geliştirilirken Python Pandas kütüphanesi kullanılmıştır. Veriler Autoregressive Model ile regresyona sokulmuştur.

Algoritma 3 aşamadan gerçekleştirilmiştir;
* Bir PI System'den AFSDK üzerinden Python'a veri çekmek.
* Python Pandas kütüphanesiyle birlikte verilerin önişlemesini yapmak, regresyona sokulabilecek hale getirmek ve verileri regresyona
sokarak gelecek için veri tahminlerinde bulunmak.
* Bütün verileri grafik üzerinde göstererek ve tahmin verilerini kullanarak anomali tespit etmek.

# Gereksinimler

## PI System tarafındaki Gereksinimler
* PI Data Archive 2015.
* AFSDK , PI Data Archive'e okuma/yazma erişimi.

## Algoritma Geliştirme IDE'si ve Python Sürümü
* Spyder IDE için Anaconda kurulumu.
* Python Pandas ve statsmodels kütüphanelerinin kurulumu.(Anaconda kurulumu ile sağlanabilir)
