# controller/browser_controller.py
class BrowserController:
    def __init__(self, ui, privacy_manager):
        self.ui = ui
        self.privacy_manager = privacy_manager

    def load_url(self, url):
        """Traite l'URL et l'envoie à l'UI pour l'affichage."""
        url = self.privacy_manager.enforce_https(url)  # Forcer HTTPS
        url = self.privacy_manager.apply_tracking_protection(url)  # Appliquer la protection contre les traqueurs
        self.ui.update_webview(url)  # Mettre à jour le WebView avec l'URL traitée
