import requests

def api_send(name,js):
    headers = {
        # requests won't add a boundary if this header is set when you pass files=
        # 'Content-Type': 'multipart/form-data',
    }

    files = {
        'img_file': open(name, 'rb'),
    #   'description': (None, {"MaBN": js["MaBN"], "TenBN": js["TenBN"], "Ngaysinh": js["Ngaysinh"], "Ngaychup": js["Ngaychup"], "IDmay": js["IDmay"], "S": js["S"], "N": js["N"], "T": js["T"], "I": js["I"], "xC": js["xC"], "yC": js["yC"], "hC": js["hC"],"wC": js["wC"], "xD": js["xD"], "yD": js["yD"], "hD": js["hD"], "wD": js["wD"], "Resolution": js["Resolution"]}),
        'description': (None, js)
    }
    print("Files: ", files["description"])
    response = requests.post('http://116.118.51.144:8004/capture', headers=headers, files=files)
    print(response.text)

