import csv
const_dict = {}

# "曲名,譜面定数" 形式のcsvファイルを読みこむ
fname = "test.csv"  # csvファイル名を指定

with open(fname, "r", encoding="utf-8") as f:
    reader = csv.reader(f)

    for row in reader:
        const_dict[row[0]] = row[1]
        #print(row[0], row[1])
        # const_dict = {"曲名":"譜面定数", ... }

#print(const_dict)