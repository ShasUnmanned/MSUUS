import qrtools
qr = qrtools.QR()
qr.decode("test.jpg")
print qr.data