# ui/ui.py
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk, WebKit2

class UI(Gtk.Window):
    def __init__(self):
        super().__init__(title="Navigateur GTK + WebKitGTK")
        self.set_default_size(1000, 600)
        self.controller = None

        # Barre d'adresse
        self.url_bar = Gtk.Entry()
        self.url_bar.set_placeholder_text("Entrez une URL...")
        self.url_bar.connect("activate", self.load_url)

        # Bouton Aller
        self.go_button = Gtk.Button(label="Aller")
        self.go_button.connect("clicked", self.load_url)

        # WebView pour afficher les pages
        self.webview = WebKit2.WebView()

        # Barre en haut pour l'URL et bouton Aller
        self.top_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.top_bar.pack_start(self.url_bar, expand=True, fill=True, padding=5)
        self.top_bar.pack_start(self.go_button, expand=False, fill=True, padding=5)

        # Mise en page principale
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.box.pack_start(self.top_bar, expand=False, fill=True, padding=5)
        self.box.pack_start(self.webview, expand=True, fill=True, padding=5)

        self.add(self.box)
        self.show_all()

    def set_controller(self, controller):
        """Associe le contrôleur à l'interface."""
        self.controller = controller

    def load_url(self, widget):
        """Charge l'URL entrée dans la barre d'adresse."""
        url = self.url_bar.get_text()
        self.controller.load_url(url)

    def update_webview(self, url):
        """Met à jour la vue Web avec l'URL donnée."""
        self.webview.load_uri(url)
