import cv2 as cv
import mediapipe as mp
from hand_module import HandModule

hand_module = HandModule()

# Webcam'den görüntü almak için VideoCapture nesnesi oluştur
cap = cv.VideoCapture(0)

while True:
    # Webcam'den bir görüntü oku
    success, image = cap.read()
    
    # Eğer görüntü başarıyla alınamadıysa döngüden çık
    if not success:
        break

    image = cv.flip(image, 1)
    
    positions = hand_module.nokta_koordinatlarini_bul(image)

    if positions:
        parmak_sayisi = hand_module.parmak_sayisini_bul()
        hand_module.metin_goster(image, f'Parmaklar: {parmak_sayisi}', (50, 50))
        hand_module.el_izlerini_ciz(image)

    # Görüntüyü ekranda göster
    cv.imshow("El Takibi", image)
    
    # Kullanıcı 'q' tuşuna basarsa döngüyü kır
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# VideoCapture ve OpenCV pencerelerini kapat
cap.release()
cv.destroyAllWindows()
