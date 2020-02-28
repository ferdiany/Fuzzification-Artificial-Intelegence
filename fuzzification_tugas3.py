import pandas as pd
import csv

influencers = pd.read_csv("influencers.csv",header=0,sep=",")

id_followers = influencers['id'].values.tolist()
followers = influencers['followerCount'].values.tolist()
rate = influencers['engagementRate'].values.tolist()

#Proses Fuzifikasi

#range rendah follower < 40000

#follower sedikit data < 40000
#follower sedang 30000 < data < 70000
#follower besar data > 60000

def FollowerSedikit(data):
    if(data <= 30000):
        return 1
    elif((data > 30000) and (data < 40000)):
        return (data - 30000)/(40000-30000)
    else:
        return 0

def FollowerSedang(data):
    if((data > 30000) and (data <= 40000)):
        return (40000-data)/(40000-30000)
    elif((data > 40000) and (data <= 60000)):
        return 1
    elif((data > 60000) and (data < 70000)):
        return (data-60000)/(70000-60000)
    else:
        return 0

def FollowerBanyak(data):
    if((data > 60000) and (data <= 70000)):
        return (70000-data)/(70000-60000)
    elif(data > 70000):
        return 1
    else:
        return 0

#rate kecil data < 3.0
#rate sedang 2,5 < data < 5,5
#rate tinggi data > 5,0
        
def RateKecil(data):
    if(data <= 2.5):
        return 1
    if((data > 2.5) and (data < 3.0)):
        return (data-2.5)/(3-2.5)
    else:
        return 0

def RateSedang(data):
    if((data > 2.5) and (data <= 3.0)):
        return (3.0-data)/(3.0-2.5)
    elif((data > 3.0) and (data <= 5.0)):
        return 1
    elif((data > 5.0) and (data < 5.5)):
        return (data-5.0)/(5.5-5.0)
    else:
        return 0

def RateTinggi(data):
    if((data > 5.0) and (data <= 5.5)):
        return (5.5-data)/(5.5-5.0)
    elif((data > 5.5)):
        return 1
    else:
        return 0

isifollower = []
isirate = []

for i in range(len(followers)):
    sedikit = FollowerSedikit(followers[i])
    sedang = FollowerSedang(followers[i])
    banyak = FollowerBanyak(followers[i])
    isifollower.append([sedikit,sedang,banyak])

for i in range(len(rate)):
    kecil = RateKecil(rate[i])
    sedang = RateSedang(rate[i])
    tinggi = RateTinggi(rate[i])
    isirate.append([kecil,sedang,tinggi])

#aturan Inferensi
inferensi = []

for i in range(len(id_followers)):
    layak = 0
    sangat_layak = 0
    #menentukan rules layak, tidak_layak, dan sangat_layak
    inf_rules1 = min(isifollower[i][0],isirate[i][0])
    inf_rules2 = min(isifollower[i][1],isirate[i][0])
    inf_rules3 = min(isifollower[i][2],isirate[i][0])
    #mengambil nilai max dari hasil nilai2 minimum
    if((inf_rules1 > inf_rules2) or (inf_rules1 > inf_rules3)):
        tidak_layak = inf_rules1
    elif((inf_rules2 > inf_rules1) or (inf_rules2 > inf_rules3)):
        tidak_layak = inf_rules2
    elif((inf_rules3 > inf_rules1) or (inf_rules3 > inf_rules2)):
        layak = inf_rules3
    #menentukan rules layak, tidak_layak, dan sangat_layak    
    inf_rules4 = min(isifollower[i][0],isirate[i][1])
    inf_rules5 = min(isifollower[i][1],isirate[i][1])
    inf_rules6 = min(isifollower[i][2],isirate[i][1])
    #mengambil nilai max dari hasil nilai2 minimum
    if((inf_rules4 > inf_rules5) or (inf_rules4 > inf_rules6)):
        tidak_layak = inf_rules4
    elif((inf_rules5 > inf_rules4) or (inf_rules5 > inf_rules6)):
        layak = inf_rules5
    elif((inf_rules6 > inf_rules4) or (inf_rules6 > inf_rules5)):
        layak = inf_rules6
    #menentukan rules layak, tidak_layak, dan sangat_layak    
    inf_rules7 = min(isifollower[i][0],isirate[i][2])
    inf_rules8 = min(isifollower[i][1],isirate[i][2])
    inf_rules9 = min(isifollower[i][2],isirate[i][2])
    #mengambil nilai max dari hasil nilai2 minimum
    if((inf_rules7 > inf_rules8) or (inf_rules7 > inf_rules9)):
        layak = inf_rules7
    elif((inf_rules8 > inf_rules7) or (inf_rules8 > inf_rules9)):
        sangat_layak = inf_rules8
    elif((inf_rules9 > inf_rules7) or (inf_rules9 > inf_rules8)):
        sangat_layak = inf_rules9

    inferensi.append([tidak_layak,layak,sangat_layak])

#Proses Defuzifikasi Menggunakan Model Sugeno
defuzifikasi = []
for i in range(len(inferensi)):
    nilai_tidaklayak = 55
    nilai_layak = 80
    nilai_sangatlayak = 90
    
    hasil = ((inferensi[i][0]*nilai_tidaklayak) + (inferensi[i][1]*nilai_layak) + (inferensi[i][2]*nilai_sangatlayak)) / (inferensi[i][0]+inferensi[i][1]+inferensi[i][2])
    defuzifikasi.append(hasil)
    
hasil = []
for i in range(len(id_followers)):
    hasil.append({
            'id' : id_followers[i],
            'nilai_kelayakan' : defuzifikasi[i]
        })

#mengurutkan nilai kelayakan dari yang terbesar ke terkecil
sorting = sorted(hasil, key=lambda d: d['nilai_kelayakan'], reverse=True)

#save file
i = 0
with open('chosen.csv','w') as f:
    writer1 = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    print("\n20 Influencers Terbaik")
    for d in sorting:
        tulis = d['id']
        writer1.writerow([tulis])
        print(tulis)
        i = i+1
        if(i==20):
            break