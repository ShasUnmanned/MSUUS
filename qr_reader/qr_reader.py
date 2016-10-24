import qrtools
qr = qrtools.QR()
qr.decode("test2.jpg")
print(qr.data)
