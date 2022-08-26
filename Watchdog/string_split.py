import json
def stringsplit(text, res ,s, n, t, i, xC, yC, wC, hC, xD, yD, wD, hD):
    name = text.split(".")
    x = name[0].split("_")
    js = {
        "MaBN" : x[0],
        "TenBN" : x[2] +" "+ x[1],
        "Ngaysinh" : x[3],
        "Ngaychup" : x[4],
        "IDmay" : x[5],
        "S" : s,
        "N" : n,
        "T" : t,
        "I" : i,
        "xC" : xC,
        "yC" : yC,
        "hC" : hC,
        "wC" : wC,
        "xD" : xD,
        "yD" : yD,
        "hD" : hD,
        "wD" : wD,
        "Resolution" : res
        }
    print(js)
    return name[0], js
def exportJS(name, data):
    with open(name +'.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
def getEye(name):
    x = name.split(".")
    x = x[0].split("_")
    if x[6] == 'OD': return "R"
    if x[6] == 'OS': return "L"
    return "R"
#print(getEye("08092003_PHUONG_NGUYEN HOANG LE_20120101_20200908_(6444)_OS.jpg"))
