import requests
headers = {
   
  #  'Content-Type': 'multipart/form-data',
}

files = {
    "img_file": open('08092003_PHUONG_NGUYEN HOANG LE_20120101_20200908_(6444)_OS.jpg', 'rb'),
    "description": (None, '{"MaBN": "08092003","TenBN": "NGUYEN HOANG LE PHUONG","Ngaysinh": "20120101","Ngaychup":"20200908","MaHinhAnh": "6444"}'),
}

response = requests.post('http://eyedr.bvmat.com/api/v1/capture', headers=headers, files=files)
print(response.text)
'''
curl -X POST -H "Content-Type: multipart/form-data" -F "img_file=@PotatoHealthy1.JPG"
-F description="{\"MaBN\": \"08092003\",\"TenBN\": \"NGUYEN HOANG LE PHUONG\",\"Ngaysinh\": \"20120101\",\"Ngaychup\": \"20200908\",
\"MaHinhAnh\": \"6444\"}" http://eyedr.bvmat.com/api/v1/capture
'''
