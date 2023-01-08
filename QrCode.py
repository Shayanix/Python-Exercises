import qrcode


class QrCode:
    
    def __init__(self,size,padding):
        self.qr = qrcode.QRCode(box_size=size,border=padding)
        
    def generate_qr(self,file_name,fg,bg):
        
        user_input = input('Enter the Text or URL to generate QR code:')
        
        try:
            self.qr.add_data(user_input)
            qr_image = self.qr.make_image(fill_color = fg , back_color = bg)
            qr_image.save(file_name)
            print (f'QR code saved as {file_name} successfully...')
            
        except Exception as e:
            print (f'Error : {e}')
            
def main():
    qr = QrCode(size=30,padding=5)
    qr.generate_qr(file_name='myQrCode.png',fg = 'black', bg = 'white')
    
    
if __name__ == '__main__':
    main()
    