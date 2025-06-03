import cv2
import mediapipe as mp
import numpy as np
import pygame
import time
import os
import sys

# Inicializa MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Inicializa Pygame e mixer
pygame.init()
pygame.mixer.init()

# Arquivos de som
EMERGENCIA_SOUND = 'emergencia.wav'
ASSISTENCIA_SOUND = 'assistencia.wav'
RISCO_SOUND = 'risco.wav'

# Verifica se os arquivos existem
for sound_file in [EMERGENCIA_SOUND, ASSISTENCIA_SOUND, RISCO_SOUND]:
    if not os.path.exists(sound_file):
        print(f"[ERRO] Arquivo de som não encontrado: {sound_file}")
        sys.exit(1)

# Carrega os sons
try:
    emergencia_sound = pygame.mixer.Sound(EMERGENCIA_SOUND)
    assistencia_sound = pygame.mixer.Sound(ASSISTENCIA_SOUND)
    risco_sound = pygame.mixer.Sound(RISCO_SOUND)
except pygame.error as e:
    print(f"[ERRO] Falha ao carregar som: {e}")
    sys.exit(1)

# Função para tocar som
def play_sound(sound):
    pygame.mixer.Sound.play(sound)

# Função para reconhecer gestos
def recognize_gesture(hand_landmarks):
    tip_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Polegar
    if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Outros dedos
    for i in range(1, 5):
        if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    # Gesto: apenas o dedo indicador levantado
    if fingers == [0, 1, 0, 0, 0]:
        return "RISCO"

    # Gesto: todos os dedos levantados
    if fingers.count(1) == 5:
        return "EMERGENCIA"

    # Gesto: indicador e médio levantados
    if fingers == [0, 1, 1, 0, 0]:
        return "ASSISTENCIA"

    return "NENHUM"

# Inicia captura de vídeo
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("[ERRO] Não foi possível abrir o vídeo.")
    sys.exit(1)

prev_gesture = ""
gesture_cooldown = 3  # segundos
last_action_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            gesture = recognize_gesture(hand_landmarks)

            if gesture != "NENHUM" and gesture != prev_gesture and (time.time() - last_action_time) > gesture_cooldown:
                print(f"[ALERTA] {gesture} detectada!")

                if gesture == "EMERGENCIA":
                    play_sound(emergencia_sound)
                elif gesture == "ASSISTENCIA":
                    play_sound(assistencia_sound)
                elif gesture == "RISCO":
                    play_sound(risco_sound)

                prev_gesture = gesture
                last_action_time = time.time()

            # Mostra o nome do gesto na tela
            cv2.putText(frame, f"Gesto: {gesture}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2, cv2.LINE_AA)
    else:
        prev_gesture = "NENHUM"

    cv2.imshow('WattsUp Gesture Monitor', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera recursos
cap.release()
cv2.destroyAllWindows()
hands.close()
pygame.quit()
