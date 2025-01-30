# app.py
from controller.browser_controller import BrowserController
from data.privacy_manager import PrivacyManager
from ui.ui import UI
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk

def main():
    # Initialisation des composants
    privacy_manager = PrivacyManager()  # Gestion de la confidentialité
    ui = UI()  # Interface utilisateur
    controller = BrowserController(ui, privacy_manager)  # Contrôleur de la logique métier

    # Initialisation de l'UI avec le contrôleur
    ui.set_controller(controller)

    # Lancement de la boucle principale de Gtk
    Gtk.main()

if __name__ == "__main__":
    main()
