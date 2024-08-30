import cv2 as cv
import mediapipe as mp

class HandModule:
    # Gerekli sınıf değişkenleri
    def __init__(self):
        self.hands = mp.solutions.hands.Hands()
        self.drawing_utils = mp.solutions.drawing_utils
        self.hand_landmarks = None
        self.tipIds = [4, 8, 12, 16, 20]
        self.fingers = []

    def nokta_koordinatlarini_bul(self, image):
        # Elin görüntüyü işleme sürecini başlat
        results = self.hands.process(image)
        
        # Koordinatları saklamak için bir liste oluştur
        positions = []
        
        # Eğer el işaretleme noktaları bulunduysa
        if results.multi_hand_landmarks:
            # İlk elin işaretleme noktalarını al
            self.hand_landmarks = results.multi_hand_landmarks[0]
            
            # Görüntünün yüksekliği ve genişliğini al
            h, w, c = image.shape
            
            # Her bir işaretleme noktasını işleme
            for id, lm in enumerate(self.hand_landmarks.landmark):
                # İşaretleme noktasının ekran koordinatlarını hesapla
                cx, cy = int(lm.x * w), int(lm.y * h)
                # Koordinatları listeye ekle
                positions.append((id, cx, cy))
        
        # Koordinatların bulunduğu listeyi döndür
        return positions


    def parmak_sayisini_bul(self):
        if not self.hand_landmarks:
            return 0

        self.fingers = []  

        # Baş parmak kontrolü
        if self.hand_landmarks.landmark[self.tipIds[0]].x < self.hand_landmarks.landmark[self.tipIds[0] - 1].x:
            self.fingers.append(1)
        else:
            self.fingers.append(0)

        # Diğer parmaklar için kontrol
        for i in range(1, 5):
            if self.hand_landmarks.landmark[self.tipIds[i]].y < self.hand_landmarks.landmark[self.tipIds[i] - 2].y:
                self.fingers.append(1)
            else:
                self.fingers.append(0)

        # Açık olan parmakların toplam sayısını döndür
        return sum(self.fingers)

    def metin_goster(self, image, text, position, color=(98, 160, 3)):
        cv.putText(image, text, position, cv.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    def el_izlerini_ciz(self, image, landmark_color=(138, 58, 30), connection_color=(98, 160, 3)):
        if self.hand_landmarks:
            landmark_drawing_spec = self.drawing_utils.DrawingSpec(color=landmark_color, thickness=4)
            connection_drawing_spec = self.drawing_utils.DrawingSpec(color=connection_color, thickness=2)
            
            self.drawing_utils.draw_landmarks(
                image,
                self.hand_landmarks,
                mp.solutions.hands.HAND_CONNECTIONS,
                landmark_drawing_spec,
                connection_drawing_spec
            )
