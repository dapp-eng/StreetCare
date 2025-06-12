from kivy_garden.mapview import MapMarker
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.popup import Popup
from kivymd.uix.label import MDLabel

class MyCustomMarker(MapMarker):
    def __init__(self, lat, lon, cluster_id, jumlah, nama_jalan, status, jumlah_kecelakaan, source, **kwargs):
        super().__init__(lat=lat, lon=lon, source=source, **kwargs)
        self.cluster_id = cluster_id
        self.nama_jalan = nama_jalan
        self.jumlah = jumlah
        self.jumlah_kecelakaan = jumlah_kecelakaan
        self.status = status.capitalize()
        self.popup = None
    
    def on_release(self):
        status_color = self.get_status_color(self.status.lower())
        r, g, b, a = status_color
        hex_color = f"{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
        
        if self.popup:
            self.popup.dismiss()
        content = MDLabel(
                markup=True,
                text=(
                    f"Jumlah laporan: {self.jumlah}\n"
                    f"[color={hex_color}]Status: {self.status.replace('_', ' ')}[/color]\n"
                    f"Intensitas Kecelakaan: {self.jumlah_kecelakaan}"
                ),
                theme_font_size="Custom",
                font_size="11.5sp",
                theme_font_name="Custom",
                font_name="Poppins-Medium",
                theme_text_color="Custom",
                text_color=(0.1, 0.2, 0.4, 1),
                halign="center",
            )
        self.popup = Popup(
            title=f"{self.nama_jalan}",
            content=content,
            size_hint=(0.45, 0.285),
            title_font="Poppins-Bold",
            title_align="center",
            title_color=(0.1, 0.2, 0.4, 1),
            background="",
            background_color=(1, 1, 1, 1),
            separator_color=(0.1, 0.2, 0.4, 1),
            padding="10dp",
        )
        self.popup.open()
    
    def get_status_color(self, status):
        status_colors = {
            "pending": (1, 0.6, 0, 1),
            "approved": (0.2, 0.6, 1, 1),
            "dalam_perbaikan": (1, 0.4, 0, 1),
            "selesai": (0, 0.6, 0, 1),
        }
        return status_colors.get(status.lower(), (0.4, 0.4, 0.4, 1))
    