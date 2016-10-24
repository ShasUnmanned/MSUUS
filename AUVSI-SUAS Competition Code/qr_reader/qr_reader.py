import qrtools
qr = qrtools.QR()
qr.decode("test3.jpg")
print(qr.data)
