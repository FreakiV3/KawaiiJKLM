from pynput.keyboard import Listener, Key
import pyautogui
import pyperclip
import random
import time
from colorama import init, Fore
from pythonosc import udp_client

# Configuration VRChat
IP_VRCHAT = "127.0.0.1"  # Adresse IP de votre instance VRChat
PORT_VRCHAT_SEND = 9000  # Port d'envoi OSC de VRChat

def send_osc_message(address, *args):
    client = udp_client.SimpleUDPClient(IP_VRCHAT, PORT_VRCHAT_SEND)
    client.send_message(address, args)

# Liste des langues disponibles
LANGUAGES = {
    1: 'wordlisten',
    2: 'wordlistes',
    3: 'wordlistfr'
}

# Fonction pour afficher une animation de texte
def animate_text(lines, delay=0.1):
    for line in lines:
        print("\r" + " " * 40, end="", flush=True)
        for char in line:
            print(char, end="", flush=True)
            time.sleep(delay)
        print()

# Affichage de l'animation d'introduction
init(autoreset=True)
intro_animation = [
    "Bienvenue dans le script de saisie de mots!",
    "Appuyez sur F8 pour définir la position, F4 pour saisir un mot.",
]

animate_text(intro_animation, delay=0.05)

# Sélection de la langue
def select_language():
    print("\nChoisissez la langue:")
    for key, value in LANGUAGES.items():
        print(f"{key}. {Fore.MAGENTA}{value}{Fore.RESET}")

    while True:
        try:
            choice = int(input("Entrez le numéro de la langue choisie: "))
            if choice in LANGUAGES:
                return LANGUAGES[choice]
            else:
                print(f"{Fore.RED}Choix invalide. Veuillez choisir un numéro valide.{Fore.RESET}")
        except ValueError:
            print(f"{Fore.RED}Veuillez entrer un numéro valide.{Fore.RESET}")

# Chargement du fichier de mots en fonction de la langue sélectionnée
selected_language = select_language()
word_list_file = f"{selected_language}.txt"

with open(word_list_file) as word_file:
    valid_words = word_file.read().split()

# Paramètres du script
bomb_x = ""
bomb_y = ""
delays = [0.03, 0.04, 0.05, 0.06, 0.4]
long_words = True
instant_typing = False
pyautogui.PAUSE = 0
used_words = set()

# Fonction de libération de la touche
def release(key):
    global bomb_x, bomb_y, used_words
    if key == Key.f8:
        try:
            bomb_x, bomb_y = pyautogui.position()
            print(f"{Fore.GREEN}Position définie avec succès!{Fore.RESET}")
        except Exception as err:
            print(f"{Fore.RED}Erreur lors de la récupération de la position de la souris: {err}{Fore.RESET}")
    if key == Key.f4:
        try:
            pyautogui.click(x=bomb_x, y=bomb_y, clicks=2)
            with pyautogui.hold('ctrl'):
                pyautogui.press('c')
            pyautogui.click(x=bomb_x - 100, y=bomb_y)
            time.sleep(0.1)
            syllable = pyperclip.paste().lower().strip()
            pyperclip.copy('')
            found_words = [word for word in valid_words if syllable in word]
            
            if not found_words:
                print(f"{Fore.YELLOW}Aucun mot trouvé.{Fore.RESET}")
                return

            if long_words:
                found_words.sort(key=len, reverse=True)
            
            final_word = random.choice(found_words)
            while final_word in used_words:
                if len(used_words) == len(found_words):
                    print(f"{Fore.YELLOW}Tous les mots ont été utilisés.{Fore.RESET}")
                    return
                final_word = random.choice(found_words)
            
            used_words.add(final_word)
            
            if instant_typing:
                pyperclip.copy(final_word)
                with pyautogui.hold('ctrl'):
                    pyautogui.press('v')
            else:
                for char in final_word:
                    delay = random.choice(delays)
                    pyautogui.write(char, delay)
            
            # Envoi du mot à la chatbox de VRChat
            send_osc_message("/chatbox/input", final_word)
            
            time.sleep(0.1)
            pyautogui.press('enter')
            print(f"{Fore.GREEN}Mot saisi avec succès: {final_word}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Erreur: {e}{Fore.RESET}")

with Listener(on_release=release) as listener:
    print(f"{Fore.CYAN}Script de saisie de mots chargé. Appuyez sur F8 pour définir la position, F4 pour saisir un mot.{Fore.RESET}")
    print(f"{Fore.CYAN}Crédits: FreakiV3 KawaiiSquad.{Fore.RESET}")
    listener.join()
