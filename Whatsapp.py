import speech_recognition as sr
import subprocess
import time
import pyttsx3
from pywinauto import keyboard
import pyautogui
import keyboard as kb

# --- Inicializa TTS ---
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def falar(texto):
    engine.say(texto)
    engine.runAndWait()

# --- Abre o WhatsApp Desktop ---
subprocess.Popen(['start', 'whatsapp://'], shell=True)
print("⌛ Abrindo WhatsApp Desktop...")
falar("Abrindo WhatsApp Desktop")
time.sleep(1)  # Aguarda abrir

# --- Função para enviar mensagem ---
def enviar_mensagem(contato, mensagem):
    try:
        # Busca contato
        keyboard.SendKeys('^f')
        time.sleep(1)
        keyboard.SendKeys(contato)
        time.sleep(1)
        keyboard.SendKeys('{TAB}')
        time.sleep(1)
        keyboard.SendKeys('{ENTER}')
        time.sleep(1)

        kb.write(mensagem)
        keyboard.SendKeys('{ENTER}')
        print(f"✅ Mensagem enviada para {contato}: {mensagem}")
        falar(f"Mensagem enviada para {contato}")
    except Exception as e:
        print("❌ Erro ao enviar mensagem:", e)
        falar("Erro ao enviar mensagem")

# --- Captura de voz ---
reconhecedor = sr.Recognizer()
microfone = sr.Microphone()

while True:
    with microfone as source:
        print("🎧 Aguardando comando de voz...")
        falar("Aguardando comando")
        reconhecedor.adjust_for_ambient_noise(source)
        audio = reconhecedor.listen(source)

    try:
        comando = reconhecedor.recognize_google(audio, language="pt-BR")
        print(f"🎤 Captado: {comando}")

        # --- Comando para enviar mensagem ---
        if "enviar mensagem para" in comando.lower() and "dizendo" in comando.lower():
            partes = comando.lower().split("enviar mensagem para")[1].split("dizendo")
            contato_nome = partes[0].strip().title()
            texto_mensagem = partes[1].strip()
            enviar_mensagem(contato_nome, texto_mensagem)

        elif comando.lower() == "sair":
            print("👋 Encerrando...")
            falar("Encerrando programa")
            break
        else:
            print("❌ Comando não reconhecido.")
            falar("Comando não reconhecido")
    except sr.UnknownValueError:
        print("❌ Não entendi o que você falou.")
        falar("Não entendi o que você falou")
    except sr.RequestError as e:
        print(f"❌ Erro no serviço de reconhecimento: {e}")
        falar("Erro no serviço de reconhecimento")
