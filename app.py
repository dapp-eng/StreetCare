import sys, os
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.screenmanager import SlideTransition, FadeTransition, WipeTransition, RiseInTransition
from kivymd.uix.transition.transition import MDSharedAxisTransition
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.config import Config
from kivy.properties import StringProperty, NumericProperty
from kivy_garden.mapview import MapView, MapMarker
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogContentContainer,
)
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.label import MDLabel
from kivy.animation import Animation
from kivy.uix.image import Image
from kivymd.uix.bottomsheet import MDBottomSheet
from kivy.core.image import Image as CoreImage
from io import BytesIO
from kivy.graphics import PushMatrix, PopMatrix, Scale, Translate
from plyer import gps
from kivy.utils import platform
from kivy.metrics import dp, sp
from plyer import camera
from kivy.uix.image import Image
from kivymd.uix.fitimage import FitImage
from kivy.graphics.texture import Texture
from kivy.uix.video import Video
from moviepy import VideoFileClip
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDIcon
from kivymd.uix.pickers import MDDockedDatePicker, MDModalInputDatePicker
import random, smtplib, re, hashlib, bcrypt, json, time, pymysql, requests, geocoder, cv2, shutil, threading, datetime, fitz, uuid
from datetime import datetime
from urllib.parse import unquote
from threading import Thread
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarSupportingText, MDSnackbarButtonContainer, MDSnackbarCloseButton
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from custom_marker import MyCustomMarker
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivymd.uix.card import MDCard
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.textfield import MDTextField
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivymd.uix.divider import MDDivider
from kivymd.uix.menu import MDDropdownMenu
from kivy.graphics import Color, RoundedRectangle
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.clock import mainthread
from plyer import filechooser
from num2words import num2words

API_URL = "https://StreetCare.pythonanywhere.com"
Config.set('kivy', 'video', 'ffpyplayer')
Config.set('graphics', 'width', '720')
Config.set('graphics', 'height', '1280')
Window.size = (360, 640)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

LabelBase.register(name="Poppins-Regular", fn_regular=resource_path("assets/fonts/Poppins-Regular.ttf"))
LabelBase.register(name="Poppins-SemiBold", fn_regular=resource_path("assets/fonts/Poppins-SemiBold.ttf"))
LabelBase.register(name="Poppins-Medium", fn_regular=resource_path("assets/fonts/Poppins-Medium.ttf"))
LabelBase.register(name="Poppins-Bold", fn_regular=resource_path("assets/fonts/Poppins-Bold.ttf"))

# if platform == 'android':
#     from jnius import autoclass, cast
#     from android import activity
#     from android.permissions import request_permissions, Permission
#     request_permissions([
#         Permission.CAMERA,
#         Permission.RECORD_AUDIO,
#         Permission.READ_EXTERNAL_STORAGE,
#         Permission.WRITE_EXTERNAL_STORAGE
#     ])
    
def open_video_capture():
    # if platform == 'android':
    #     open_video_camera_android()
    # else:
    open_video_file_desktop()
        
def open_video_file_desktop():
    file_path = filechooser.open_file(
        title="Pilih Video", filters=[("Video files", "*.mp4;*.avi;*.mov")]
    )
    if file_path:
        print("Video selected:", file_path[0])
        show_video_in_container(file_path[0])
        
# def open_video_camera_android():
#     PythonActivity = autoclass('org.kivy.android.PythonActivity')
#     Intent = autoclass('android.content.Intent')
#     MediaStore = autoclass('android.provider.MediaStore')
#     currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
#     intent = Intent(MediaStore.ACTION_VIDEO_CAPTURE)
#     currentActivity.startActivityForResult(intent, 1001)
#     if not hasattr(activity, "_video_result_bound"):
#         activity.bind(on_activity_result=on_video_result)
#         activity._video_result_bound = True
        
def on_video_result(request_code, result_code, intent):
    if request_code == 1001 and result_code == -1:
        uri = intent.getData()
        path = uri.toString()
        print("Video recorded:", path)
        app = MDApp.get_running_app()
        app.recorded_video_path = path
        show_video_in_container(path)
        
def show_video_in_container(video_path):
    app = MDApp.get_running_app()
    screen = app.root.get_screen("camera")
    screen.show_video(video_path)
    app.change_screen("camera", "rise")

def show_message(text):
    MDSnackbar(
        MDSnackbarSupportingText(
            text=text,
            theme_font_name="Custom",
            font_name="Poppins-Regular",
            theme_font_size="Custom",
            font_size=sp(11.5),
        ),
        MDSnackbarButtonContainer(
            MDSnackbarCloseButton(
                icon="close",
            ),
            pos_hint={"center_y": 0.5}
        ),
        y=dp(24),
        orientation="horizontal",
        pos_hint={"center_x": 0.5},
        size_hint_x=0.75,
        background_color= (0.1, 0.2, 0.4, 0.7),
    ).open()

def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def hide_edit_icon(widget):
    for child in widget.children:
        if isinstance(child, MDIconButton) and child.icon == "pencil":
            child.opacity = 0
            child.disabled = True
        hide_edit_icon(child)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_user_to_database(user_data):
    try:
        response = requests.post(f"{API_URL}/register", json=user_data)
        if response.status_code == 201:
            print("User berhasil disimpan ke database melalui API.")
            return True
        else:
            print("Gagal menyimpan user:", response.json())
            return False
    except Exception as e:
        print("Error saat menyimpan user:", e)
        return False
  
def is_email_registered(email):
    try:
        response = requests.post(f"{API_URL}/check/email", json={"email": email})
        if response.status_code == 200:
            return response.json().get("registered", False)
        return False
    except Exception as e:
        print("Error saat cek email:", e)
        return False

def is_username_registered(username):
    try:
        response = requests.post(f"{API_URL}/check/username", json={"username": username})
        if response.status_code == 200:
            return response.json().get("registered", False)
        return False
    except Exception as e:
        print("Error saat cek username:", e)
        return False

def verify_login(login_id, password_plain):
    try:
        response = requests.post(f"{API_URL}/login", json={
            "login_id": login_id,
            "password": password_plain
        })
        if response.status_code == 200:
            return True, "Login berhasil!"
        elif response.status_code == 401:
            return False, "Kata sandi salah."
        elif response.status_code == 404:
            return False, "Username atau email tidak ditemukan."
        else:
            return False, response.json().get("error", "Gagal login.")
    except Exception as e:
        print("Error saat verifikasi login:", e)
        return False, "Terjadi kesalahan, silahkan coba lagi nanti."

def get_user_data(login_id):
    url = f"{API_URL}/user"
    data = {
        "login_id": login_id
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return True, response.json().get("user")
        else:
            error_msg = response.json().get("error", "Gagal ambil data user")
            return False, error_msg
    except Exception as e:
        return False, f"Koneksi error. Harap coba lagi nanti."

class ReportItem(MDBoxLayout):
    def __init__(self, nama_jalan, jumlah_laporan, status, jumlah_kecelakaan, **kwargs):
        super().__init__(orientation="vertical", size_hint_y=None, height=dp(70), padding=dp(10), spacing=dp(5), **kwargs)
        self.nama_jalan = nama_jalan
        self.jumlah_laporan = jumlah_laporan
        self.status = status
        self.jumlah_kecelakaan = jumlah_kecelakaan
        
        content_box = MDBoxLayout(orientation="horizontal", spacing=dp(10))

        left_box = MDBoxLayout(orientation="vertical", spacing=dp(4), size_hint_x=0.675)
        left_box.add_widget(MDLabel(
            text=nama_jalan,
            theme_font_name="Custom", font_name="Poppins-Bold",
            theme_font_size="Custom", font_size="14sp",
            theme_text_color="Custom", text_color=(0.063, 0.169, 0.325, 1),
            size_hint_y=None, height=dp(30)))
        left_box.add_widget(MDLabel(
            text=f"Laporan: {jumlah_laporan} | Kecelakaan: {jumlah_kecelakaan}",
            theme_font_name="Custom", font_name="Poppins-Medium",
            theme_font_size="Custom", font_size="12sp",
            theme_text_color="Custom", text_color=(0.1, 0.1, 0.1, 1),
            size_hint_y=None, height=dp(20)))

        status_box = MDBoxLayout(orientation="vertical", size_hint_x=0.325, spacing=dp(2), padding=(0, dp(6)), size_hint_y=None, height=dp(50))
        status_title = MDLabel(
            text="Status:",
            halign="center",
            theme_font_name="Custom", font_name="Poppins-SemiBold",
            theme_font_size="Custom", font_size="12sp",
            theme_text_color="Custom",
            text_color=(0.3, 0.3, 0.3, 1),
            size_hint_y=None,
            height=dp(18),
        )
        status_content = MDBoxLayout(orientation="horizontal", spacing=dp(5), size_hint_y=None, height=dp(24))
        status_icon = MDIcon(
            icon=self.get_status_icon(status),
            theme_icon_color="Custom",
            icon_color=self.get_status_color(status),
            size_hint=(None, None),
            size=(dp(20), dp(20)),
            theme_font_size="Custom", font_size="16.5sp",
            pos_hint={"center_y": 0.5}
        )
        status_label = MDLabel(
            text=status.replace("_", " ").title(),
            halign="left",
            theme_font_name="Custom", font_name="Poppins-SemiBold",
            theme_font_size="Custom", font_size="11.5sp",
            theme_text_color="Custom",
            text_color=self.get_status_color(status),
            valign="center",
            pos_hint={"center_y": 0.455}
        )
        status_content.add_widget(status_icon)
        status_content.add_widget(status_label)
        status_box.add_widget(status_title)
        status_box.add_widget(status_content)
        content_box.add_widget(left_box)
        content_box.add_widget(status_box)
        self.add_widget(content_box)
        self.add_widget(MDDivider(height=dp(2)))

    def get_status_color(self, status):
        status_colors = {
            "pending": (1, 0.6, 0, 1),
            "approved": (0.2, 0.6, 1, 1),
            "dalam_perbaikan": (1, 0.4, 0, 1),
            "selesai": (0, 0.6, 0, 1),
        }
        return status_colors.get(status.lower(), (0.4, 0.4, 0.4, 1))

    def get_status_icon(self, status):
        status_icons = {
            "pending": "clock-outline",
            "approved": "check-circle-outline",
            "dalam_perbaikan": "tools",
            "selesai": "checkbox-marked-circle-outline",
        }
        return status_icons.get(status.lower(), "alert-circle-outline")

class EditableReportItem(ReportItem):
    def __init__(self, cluster_id, **kwargs):
        super().__init__(**kwargs)
        self.cluster_id = cluster_id
        self.bind(on_touch_down=self.on_item_touched)

    def on_item_touched(self, instance, touch):
        if self.collide_point(*touch.pos):
            app = MDApp.get_running_app()
            app.root.get_screen("adminstat").show_status_dialog(self)
    
class GresikMapView(MapView):
    def __init__(self, **kwargs):
        cache_dir = os.path.join(os.getcwd(), "cache")
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        self.cache_path = cache_dir 
        
        super().__init__(**kwargs)
        self.markers = []
        self.api_markers = []
        self.user_marker = None 
        self.lat = -7.1609
        self.lon = 112.6511
        self.zoom_default = 18
        self.zoom = self.zoom_default
        self.min_zoom = 16
        self.max_zoom = 22
        Clock.schedule_once(lambda dt: self.set_initial_zoom(), 0)
        self.bind(zoom=self.on_zoom_change)
        
        Clock.schedule_once(self.update_markers, 0.1)
        Clock.schedule_interval(self.update_markers, 60)
    
    def add_marker(self, marker):
        super().add_marker(marker)
        self.markers.append(marker)

    def remove_marker(self, marker):
        super().remove_marker(marker)
        if marker in self.markers:
            self.markers.remove(marker)

    def clear_api_markers(self):
        for marker in getattr(self, 'api_markers', []):
            self.remove_marker(marker)
        self.api_markers = []
    
    def update_markers(self, *args):
        try:
            response = requests.get(f"{API_URL}/map_markers")
            data = response.json()
            if data["success"]:
                self.clear_api_markers()
                for m in data["markers"]:
                    marker_icon = f"{m['marker_color']}_marker.png"
                    marker = MyCustomMarker(
                        lat=m['lat'],
                        lon=m['lon'],
                        source=f"assets/{marker_icon}",
                        cluster_id=m['cluster_id'],
                        jumlah=m['jumlah_laporan'],
                        nama_jalan=m['nama_jalan'],
                        status=m['status'],
                        jumlah_kecelakaan=m['jumlah_kecelakaan']
                    )
                    self.add_marker(marker)
                    self.api_markers.append(marker)
        except Exception as e:
            print(f"Error updating markers: {e}")

    def set_initial_zoom(self):
        self.zoom = self.zoom_default

    def on_zoom_change(self, instance, value):
        Clock.schedule_once(self.enforce_zoom, 0)

    def enforce_zoom(self, dt):
        if self.zoom < self.min_zoom:
            self.zoom = self.min_zoom
        elif self.zoom > self.max_zoom:
            self.zoom = self.max_zoom

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            super().on_touch_move(touch)
            Clock.schedule_once(lambda dt: self.limit_to_gresik(), 0)

    def limit_to_gresik(self):
        min_lat, max_lat = -7.236, -6.897
        min_lon, max_lon = 112.448, 112.753
        new_lat = self.lat
        new_lon = self.lon
        if self.lat < min_lat:
            new_lat = min_lat
        elif self.lat > max_lat:
            new_lat = max_lat
        if self.lon < min_lon:
            new_lon = min_lon
        elif self.lon > max_lon:
            new_lon = max_lon
        if new_lat != self.lat or new_lon != self.lon:
            self.center_on(new_lat, new_lon)

GRESIK_BOUNDS = {
    "min_lat": -7.236, 
    "max_lat": -6.897,
    "min_lon": 112.448, 
    "max_lon": 112.753
    }
class StreetReportMapView(GresikMapView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_marker = None
        self.ignore_next_touch_up = False

    def on_button_pressed(self):
        self.ignore_next_touch_up = True
    
    def on_touch_up(self, touch):
        if self.ignore_next_touch_up:
            self.ignore_next_touch_up = False
            return super().on_touch_up(touch)
        
        if not self.collide_point(*touch.pos):
            return super().on_touch_up(touch)
        lat, lon = self.get_latlon_at(*touch.pos)
        if (GRESIK_BOUNDS["min_lat"] <= lat <= GRESIK_BOUNDS["max_lat"] and
            GRESIK_BOUNDS["min_lon"] <= lon <= GRESIK_BOUNDS["max_lon"]):
            if self.current_marker:
                self.remove_marker(self.current_marker)
            self.current_marker = MapMarker(lat=lat, lon=lon, source="assets/user_marker.png")
            self.add_marker(self.current_marker)
            
            if hasattr(self, "on_marker_moved"):
                self.on_marker_moved(lat, lon)
        else:
            show_message("Lokasi di luar wilayah Gresik.")
        return super().on_touch_up(touch)

    def center_on(self, lat, lon):
        super().center_on(lat, lon)
    
    def limit_to_gresik(self):
        min_lat, max_lat = GRESIK_BOUNDS["min_lat"], GRESIK_BOUNDS["max_lat"]
        min_lon, max_lon = GRESIK_BOUNDS["min_lon"], GRESIK_BOUNDS["max_lon"]
        new_lat = self.lat
        new_lon = self.lon
        if self.lat < min_lat:
            new_lat = min_lat
        elif self.lat > max_lat:
            new_lat = max_lat
        if self.lon < min_lon:
            new_lon = min_lon
        elif self.lon > max_lon:
            new_lon = max_lon
        if new_lat != self.lat or new_lon != self.lon:
            self.center_on(new_lat, new_lon)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            super().on_touch_move(touch)
            Clock.schedule_once(lambda dt: self.limit_to_gresik(), 0)

class PDFView(Image):
    def __init__(self, pdf_path, target_widget, **kwargs):
        super().__init__(**kwargs)
        self.pdf_path = pdf_path
        self.target_widget = target_widget
        self.allow_stretch = True
        self.keep_ratio = True
        Clock.schedule_once(self.load_first_page, 0.1)

    def load_first_page(self, dt):
        doc = fitz.open(self.pdf_path)
        page = doc.load_page(0)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img_data = pix.tobytes("ppm")
        data = BytesIO(img_data)
        im = CoreImage(data, ext="ppm")
        self.texture = im.texture
        self.size = self.target_widget.size
        self.size_hint = (None, None)

class ProjectList(MDCard):
    text = ""
    period = ""
    active = False

    def __init__(self, text, period, fund_data=None, parent_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.period = period
        self.fund_data = fund_data
        self.parent_screen = parent_screen
        self.active = False
        self.orientation = "horizontal"
        self.size_hint = (1, None)
        self.height = "40dp"
        self.radius = [10]
        self.line_color = (0.1, 0.2, 0.4, 1)
        self.line_width = 1.7
        self.theme_bg_color = "Custom"
        self.ripple_color = (0, 0, 0, 0)
        self.style = "outlined"
        self.theme_line_color = "Custom"
        self.line_color = (0.1, 0.2, 0.4, 1)
        self.md_bg_color = (1, 1, 1, 1)
        self.build_content()

    def on_release(self):
        reports_screen = self.parent_screen
        if reports_screen and reports_screen.active_project:
            prev_active = reports_screen.active_project
            prev_active.active = False
            prev_active.md_bg_color = (1, 1, 1, 1)
            prev_active.update_text_colors()
        
        self.active = True
        self.md_bg_color = (0.1, 0.2, 0.4, 1)
        self.update_text_colors()
        if reports_screen:
            reports_screen.active_project = self

        if self.parent_screen and self.fund_data:
            self.parent_screen.show_loading("Sedang memuat...")
            def load_and_update():
                self.parent_screen.load_project_detail(self.fund_data)
                self.parent_screen.load_comments("rancangan")
                self.parent_screen.load_comments("akhir")
                Clock.schedule_once(lambda dt: self.update_screen_labels())
            Thread(target=load_and_update, daemon=True).start()
    
    def update_screen_labels(self):
        if hasattr(self.parent_screen, "ids"):
            self.parent_screen.ids.jalan_proyek1.text = self.text
            self.parent_screen.ids.jalan_proyek2.text = self.text
            start_date = self.fund_data.get("start_date")
            end_date = self.fund_data.get("end_date")
            formatted_period = self.format_period(start_date, end_date)
            self.parent_screen.ids.date1.text = f"({formatted_period})"
            self.parent_screen.ids.date2.text = f"({formatted_period})"
        
    def format_period(self, start_date: str, end_date: str) -> str:
        try:
            start_day, start_month, start_year = start_date.split("/")
            end_day, end_month, end_year = end_date.split("/")
            if start_month == end_month and start_year == end_year:
                return f"{start_day} - {end_day} {INDO_MONTHS[start_month]} {start_year}"
            elif start_year == end_year:
                return f"{start_day} {INDO_MONTHS[start_month]} - {end_day} {INDO_MONTHS[end_month]} {start_year}"
            else:
                return f"{start_day} {INDO_MONTHS[start_month]} {start_year} - {end_day} {INDO_MONTHS[end_month]} {end_year}"
        except Exception:
            return ""

    def build_content(self):
        self.clear_widgets()
        layout = MDBoxLayout(orientation="horizontal", spacing="5dp", padding="13dp")
        self.label_text = MDLabel(
            text=self.text,
            theme_font_size="Custom",
            font_size="12.5sp",
            theme_font_name="Custom",
            font_name="Poppins-SemiBold",
            theme_text_color="Custom",
            halign="left",
            shorten=True,
            size_hint_x=0.6
        )
        layout.add_widget(self.label_text)
        self.label_period = MDLabel(
            text=self.period,
            theme_text_color="Custom",
            theme_font_size="Custom",
            font_size="11sp",
            theme_font_name="Custom",
            font_name="Poppins-Medium",
            halign="right",
            size_hint_x=0.4
        )
        layout.add_widget(self.label_period)
        self.add_widget(layout)
        self.update_text_colors()

    def update_text_colors(self):
        color_active = (1, 1, 1, 1)
        color_inactive = (0.1, 0.2, 0.4, 1)
        color = color_active if self.active else color_inactive
        if hasattr(self, 'label_text'):
            self.label_text.text_color = color
        if hasattr(self, 'label_period'):
            self.label_period.text_color = color

class Splash(MDScreen):
    def on_enter(self):
        Clock.schedule_once(self.start_timer, 10)

    def start_timer(self, *args):
        Clock.schedule_once(self.next, 1)

    def next(self, *args):
        app = MDApp.get_running_app()
        admin_data = app.check_admin_json()
        if admin_data:
            print("Auto login admin")
            app.admin_data = admin_data
            app.change_screen("home", "fade")
            return
        user_json_path = resource_path("data/user_login.json")
        if os.path.exists(user_json_path):
            try:
                with open(user_json_path, "r", encoding="utf-8") as f:
                    user_data = json.load(f)
                if "id" in user_data and "username" in user_data:
                    print(f"Auto login user: {user_data['username']}")
                    app.user_data = user_data
                    app.change_screen("home", "fade")
                    return
            except Exception as e:
                print("Gagal auto-login user:", e)
        app.change_screen("welcome", "fade")
    pass

class Welcome(MDScreen):
    pass

class Login(MDScreen):
    def on_leave(self):
        Clock.schedule_once(lambda dt: self.reset_fields(), 0.1)
    
    def on_kv_post(self, base_widget):
        self.bind_error_style("account", "account_card", "account_icon")
        self.bind_error_style("passw", "passw_card", "passw_icon")

    def bind_error_style(self, textfield_id, card_id, icon_id):
        def on_error(instance, value):
            card = self.ids[card_id]
            icon = self.ids[icon_id]
            textfield = self.ids[textfield_id]
            if value:
                card.line_color = (1, 0, 0, 1)
                icon.icon_color = (1, 0, 0, 1)
                textfield.error_color = (0, 0, 0, 0)
            else:
                card.line_color = (0.1, 0.2, 0.4, 1)
                icon.icon_color = (0.1, 0.2, 0.4, 1)
                textfield.error_color = (0, 0, 0, 0)
        self.ids[textfield_id].bind(error=on_error)
    
    def show_password(self):
        passw = self.ids.passw
        show_icon = self.ids.show_pass
        passw.password = not passw.password
        show_icon.icon = "eye" if not passw.password else "eye-off"
    
    def password_input(self, textfield, is_focused, default_text, is_password=False):
        if is_focused:
            if textfield.text == default_text:
                textfield.text = ""
                if is_password:
                    textfield.password = True
        else:
            if textfield.text.strip() == "":
                textfield.text = default_text
                if is_password:
                    textfield.password = False
    
    def handle_password(self, textfield, default_text):
        if textfield.text != "" and textfield.text != default_text:
            textfield.password = True
        
    def update_text(self, textfield, is_focused, default_text):
        if is_focused:
            if textfield.text == default_text:
                textfield.text = ""
        else:
            if textfield.text.strip() == "":
                textfield.text = default_text
    
    def show_loading(self, message="Sedang memproses..."):
        if hasattr(self, "loading_dialog") and self.loading_dialog:
            return
        content = MDBoxLayout(orientation="vertical", spacing=10, padding=20)
        content.add_widget(MDCircularProgressIndicator(size_hint=(None, None), size=("33dp", "33dp")))
        content.add_widget(MDLabel(text=message, halign="center", theme_font_name="Custom", font_name="Poppins-SemiBold", theme_font_size="Custom", font_size="14dp"))
        self.loading_dialog = MDDialog(
            MDDialogHeadlineText(
                text="Mohon Tunggu",
                halign="center",
                theme_font_name="Custom", 
                font_name="Poppins-Bold",
                theme_font_size="Custom",
                font_size="12dp"
            ),
            MDDialogContentContainer(
                content
            ),
            auto_dismiss=False,
            size_hint_x=.925
        )
        self.loading_dialog.open()

    def hide_loading(self):
        if hasattr(self, "loading_dialog") and self.loading_dialog:
            self.loading_dialog.dismiss()
            self.loading_dialog = None
    
    def login(self):
        self.show_loading("Memproses login...")
        threading.Thread(target=self.login_thread, daemon=True).start()

    def login_thread(self):
        app = MDApp.get_running_app()
        acc = self.ids.account.text.strip()
        password = self.ids.passw.text.strip()
        def show_and_hide(msg):
            Clock.schedule_once(lambda dt: show_message(msg), 0)
            Clock.schedule_once(lambda dt: self.hide_loading(), 0)
        if not acc or acc == "Masukkan username/email":
            Clock.schedule_once(lambda dt: setattr(self.ids.account, 'error', True), 0)
            show_and_hide("Username atau email harus diisi.")
            return
        if not password or password == "Masukkan kata sandi":
            Clock.schedule_once(lambda dt: setattr(self.ids.passw, 'error', True), 0)
            show_and_hide("Kata sandi harus diisi.")
            return
        success, msg = verify_login(acc, password)
        if success:
            Clock.schedule_once(lambda dt: show_message(msg), 0)
            success_data, user_data = get_user_data(acc)
            if success_data and isinstance(user_data, dict):
                user_data.pop("password", None)
                if self.ids.login_check.active:
                    try:
                        app.user_data = user_data
                        json_path = resource_path("data/user_login.json")
                        with open(json_path, "w", encoding="utf-8") as f:
                            json.dump(user_data, f, ensure_ascii=False, indent=4)
                    except Exception as e:
                        print("Gagal menyimpan riwayat login:", e)
                else:
                    try:
                        app.user_data = user_data
                    except Exception as e:
                        print("Gagal menyimpan data login sementara:", e)
            else:
                Clock.schedule_once(lambda dt: show_message(user_data), 0)
            Clock.schedule_once(lambda dt: app.change_screen("home", "rise"), 0)
            Clock.schedule_once(lambda dt: self.hide_loading(), 0)
        else:
            Clock.schedule_once(lambda dt: show_message(msg), 0)
            if msg == "Username atau email tidak ditemukan.":
                Clock.schedule_once(lambda dt: setattr(self.ids.account, 'error', True), 0)
            elif msg == "Kata sandi salah.":
                Clock.schedule_once(lambda dt: setattr(self.ids.passw, 'error', True), 0)
            Clock.schedule_once(lambda dt: self.hide_loading(), 0)
    
    def reset_fields(self):
        self.ids.account.text = "Masukkan username/email"
        self.ids.passw.text = "Masukkan kata sandi"
        self.ids.account.error = False
        self.ids.passw.error = False
        self.ids.passw.password = False
    pass

class Adminlog(MDScreen):
    def on_leave(self):
        Clock.schedule_once(lambda dt: self.reset_fields(), 0.1)
        
    def on_kv_post(self, base_widget):
        self.bind_error_style("account", "account_card", "account_icon")
        self.bind_error_style("passw", "passw_card", "passw_icon")

    def bind_error_style(self, textfield_id, card_id, icon_id):
        def on_error(instance, value):
            card = self.ids[card_id]
            icon = self.ids[icon_id]
            textfield = self.ids[textfield_id]
            if value:
                card.line_color = (1, 0, 0, 1)
                icon.icon_color = (1, 0, 0, 1)
                textfield.error_color = (0, 0, 0, 0)
            else:
                card.line_color = (0.1, 0.2, 0.4, 1)
                icon.icon_color = (0.1, 0.2, 0.4, 1)
                textfield.error_color = (0, 0, 0, 0)
        self.ids[textfield_id].bind(error=on_error)
    
    def show_password(self):
        passw = self.ids.passw
        show_icon = self.ids.show_pass
        passw.password = not passw.password
        show_icon.icon = "eye" if not passw.password else "eye-off"
    
    def password_input(self, textfield, is_focused, default_text, is_password=False):
        if is_focused:
            if textfield.text == default_text:
                textfield.text = ""
                if is_password:
                    textfield.password = True
        else:
            if textfield.text.strip() == "":
                textfield.text = default_text
                if is_password:
                    textfield.password = False
    
    def handle_password(self, textfield, default_text):
        if textfield.text != "" and textfield.text != default_text:
            textfield.password = True
        
    def update_text(self, textfield, is_focused, default_text):
        if is_focused:
            if textfield.text == default_text:
                textfield.text = ""
        else:
            if textfield.text.strip() == "":
                textfield.text = default_text
    
    def show_loading(self, message="Sedang memproses..."):
        if hasattr(self, "loading_dialog") and self.loading_dialog:
            return
        content = MDBoxLayout(orientation="vertical", spacing=10, padding=20)
        content.add_widget(MDCircularProgressIndicator(size_hint=(None, None), size=("33dp", "33dp")))
        content.add_widget(MDLabel(text=message, halign="center", theme_font_name="Custom", font_name="Poppins-SemiBold", theme_font_size="Custom", font_size="14dp"))
        self.loading_dialog = MDDialog(
            MDDialogHeadlineText(
                text="Mohon Tunggu",
                halign="center",
                theme_font_name="Custom", 
                font_name="Poppins-Bold",
                theme_font_size="Custom",
                font_size="12dp"
            ),
            MDDialogContentContainer(
                content
            ),
            auto_dismiss=False,
            size_hint_x=.925
        )
        self.loading_dialog.open()

    def hide_loading(self):
        if hasattr(self, "loading_dialog") and self.loading_dialog:
            self.loading_dialog.dismiss()
            self.loading_dialog = None
    
    def adminlog(self):
        self.show_loading("Proses verifikasi...")
        threading.Thread(target=self.adminlog_thread, daemon=True).start()

    def adminlog_thread(self):
        app = MDApp.get_running_app()
        email = self.ids.account.text.strip()
        password_plain = self.ids.passw.text.strip()
        def show_and_hide(msg):
            Clock.schedule_once(lambda dt: show_message(msg), 0)
            Clock.schedule_once(lambda dt: self.hide_loading(), 0)
        if not email or email == "Masukkan alamat email":
            Clock.schedule_once(lambda dt: setattr(self.ids.account, 'error', True), 0)
            show_and_hide("Email harus diisi!")
            return
        if not password_plain or password_plain == "Masukkan kata sandi":
            Clock.schedule_once(lambda dt: setattr(self.ids.passw, 'error', True), 0)
            show_and_hide("Kata sandi harus diisi!")
            return
        try:
            response = requests.post(
                f"{API_URL}/admin/login",
                json={"email": email, "password": password_plain},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                admin = data.get("admin")
                if admin:
                    Clock.schedule_once(lambda dt: show_message("Login sebagai admin berhasil!"), 0)
                    admin['login_timestamp'] = time.time()
                    try:
                        json_path = resource_path("data/admin_login.json")
                        with open(json_path, "w", encoding="utf-8") as f:
                            json.dump(admin, f, ensure_ascii=False, indent=4)
                        app.admin_data = admin
                    except Exception as e:
                        print("Gagal menyimpan data admin:", e)
                    Clock.schedule_once(lambda dt: app.change_screen("home", "rise"), 0)
            else:
                msg = response.json().get("message", "Login gagal.")
                Clock.schedule_once(lambda dt: show_message(msg), 0)
                if "email" in msg.lower():
                    Clock.schedule_once(lambda dt: setattr(self.ids.account, 'error', True), 0)
                elif "sandi" in msg.lower():
                    Clock.schedule_once(lambda dt: setattr(self.ids.passw, 'error', True), 0)
        except requests.exceptions.RequestException as e:
            print("Gagal terhubung ke server adminlogin:", e)
            Clock.schedule_once(lambda dt: show_message("Tidak dapat terhubung ke server. Coba lagi nanti."), 0)
        finally:
            Clock.schedule_once(lambda dt: self.hide_loading(), 0)
    
    def reset_fields(self):
        self.ids.account.text = "Masukkan alamat email"
        self.ids.passw.text = "Masukkan kata sandi"
        self.ids.account.error = False
        self.ids.passw.error = False
        self.ids.passw.password = False
    pass

class Forgot(MDScreen):
    otp_storage = {}
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.countdown_event = None
        self.countdown_time = 0
    
    def on_leave(self):
        Clock.schedule_once(lambda dt: self.reset_fields(), 0.1)
    
    def on_kv_post(self, base_widget):
        self.bind_error_style("account", "account_card", "account_icon")
        self.bind_error_style("otp", "otp_card", "otp_icon")
        
    def bind_error_style(self, textfield_id, card_id, icon_id):
        def on_error(instance, value):
            card = self.ids[card_id]
            icon = self.ids[icon_id]
            textfield = self.ids[textfield_id]
            if value:
                card.line_color = (1, 0, 0, 1)
                icon.icon_color = (1, 0, 0, 1)
                textfield.error_color = (0, 0, 0, 0)
            else:
                card.line_color = (0.1, 0.2, 0.4, 1)
                icon.icon_color = (0.1, 0.2, 0.4, 1)
                textfield.error_color = (0, 0, 0, 0)
        self.ids[textfield_id].bind(error=on_error)
        
    def update_text(self, textfield, is_focused, default_text):
        if is_focused:
            if textfield.text == default_text:
                textfield.text = ""
        else:
            if textfield.text.strip() == "":
                textfield.text = default_text
    
    def generate_otp(self, length=6):
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])

    def send_email_otp(self):
        if self.countdown_time > 0:
            return
        email = self.ids.account.text.strip()
        otp = self.generate_otp()
        Forgot.otp_storage[email] = otp
        if not email or email == "Masukkan alamat email":
            show_message("Email tidak boleh kosong")
        elif self._send_email(email, otp):
            show_message("OTP berhasil dikirim")
            self.start_countdown(60)
        else:
            show_message("Gagal mengirim OTP, coba lagi beberapa saat!")

    def _send_email(self, email, otp):
        sender_email = 'streetcareapps@gmail.com'
        sender_password = 'pett dofw ntse xxvi'
        subject = 'StreetCare: Kode OTP Verifikasi Akun'

        plain_body = f"""
            Halo Sobat StreetCare! 🛣️

            Kode OTP kamu adalah:
            
                    {otp}
            
            NOTE:
            Jangan bagikan kode ini ke siapapun, ya!
            
            Masukkan kode ini untuk memverifikasi akun dan mulai melaporkan jalan rusak di sekitarmu.
            Terima kasih sudah peduli dengan jalan kita!

            Salam,
            Tim StreetCare
            """
        html_body = f"""
            <html>
            <head>
            <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #ffffff;
                color: #000000;
            }}
            .otp {{
                display: block;
                font-size: 24px;
                font-weight: bold;
                margin: 10px 0;
                color: #000000;
            }}
            @media (prefers-color-scheme: dark) {{
                body {{
                background-color: #000000;
                color: #ffffff;
                }}
                .otp {{
                color: #ffffff;
                }}
            }}
            </style>
            </head>
            <body>
            <p>Halo Sobat <strong>StreetCare</strong>! 🛣️</p>
            <p>Kode OTP kamu adalah:</p>
            <span class="otp">{otp}</span>
            <p><strong>NOTE:</strong><br>Jangan bagikan kode ini ke siapapun, ya!</p>
            <p>Masukkan kode ini untuk memverifikasi akun dan mulai melaporkan jalan rusak di sekitarmu.</p>
            <p>Terima kasih sudah peduli dengan jalan kita!</p>
            <p>Salam,<br>Tim StreetCare</p>
            </body>
            </html>
            """
        msg = MIMEMultipart("alternative")
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(plain_body, "plain"))
        msg.attach(MIMEText(html_body, "html"))
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, email, msg.as_string())
            return True
        except Exception as e:
            print("Gagal kirim email:", e)
            return False

    def start_countdown(self, seconds):
        self.countdown_time = seconds
        self.update_label_countdown()
        self.countdown_event = Clock.schedule_interval(self._update_countdown, 1)

    def _update_countdown(self, dt):
        self.countdown_time -= 1
        self.update_label_countdown()
        if self.countdown_time <= 0:
            self.countdown_event.cancel()
            self.countdown_event = None

    def update_label_countdown(self):
        if self.countdown_time > 0:
            self.ids.otp_label.text = f"[u]Kirimkan kode ({self.countdown_time})[/u]"
        else:
            self.ids.otp_label.text = "[u]Kirimkan kode[/u]"
    
    def show_loading(self, message="Sedang memproses..."):
        if hasattr(self, "loading_dialog") and self.loading_dialog:
            return
        content = MDBoxLayout(orientation="vertical", spacing=10, padding=20)
        content.add_widget(MDCircularProgressIndicator(size_hint=(None, None), size=("33dp", "33dp")))
        content.add_widget(MDLabel(text=message, halign="center", theme_font_name="Custom", font_name="Poppins-SemiBold", theme_font_size="Custom", font_size="14dp"))
        self.loading_dialog = MDDialog(
            MDDialogHeadlineText(
                text="Mohon Tunggu",
                halign="center",
                theme_font_name="Custom", 
                font_name="Poppins-Bold",
                theme_font_size="Custom",
                font_size="12dp"
            ),
            MDDialogContentContainer(
                content
            ),
            auto_dismiss=False,
            size_hint_x=.925
        )
        self.loading_dialog.open()

    def hide_loading(self):
        if hasattr(self, "loading_dialog") and self.loading_dialog:
            self.loading_dialog.dismiss()
            self.loading_dialog = None
    
    def verify_account(self):
        self.show_loading("Memverifikasi akun...")
        threading.Thread(target=self._verify_account_thread, daemon=True).start()

    def _verify_account_thread(self):
        app = MDApp.get_running_app()
        email = self.ids.account.text.strip()
        otp = self.ids.otp.text.strip()
        saved_otp = Forgot.otp_storage.get(email)

        def set_error(field, status=True):
            Clock.schedule_once(lambda dt: setattr(self.ids[field], "error", status), 0)

        def show_and_stop(msg, field=None):
            Clock.schedule_once(lambda dt: show_message(msg), 0)
            Clock.schedule_once(lambda dt: self.hide_loading(), 0)
            if field:
                set_error(field)
                
        if not email or email == "Masukkan alamat email":
            return show_and_stop("Email harus diisi!", "account")
        elif not is_valid_email(email):
            return show_and_stop("Email tidak valid.", "account")
        elif not is_email_registered(email):
            return show_and_stop("Email belum terdaftar!", "account")
        if not otp:
            return show_and_stop("Kode OTP harus diisi!", "otp")
        if not saved_otp:
            return show_and_stop("Kode OTP belum dikirim atau sudah kadaluarsa.", "otp")
        elif otp != saved_otp:
            return show_and_stop("Kode OTP tidak sesuai.", "otp")
        Clock.schedule_once(lambda dt: setattr(app, "verif_email", email), 0)
        Clock.schedule_once(lambda dt: show_message("Verifikasi berhasil!"), 0)
        Clock.schedule_once(lambda dt: app.change_screen("forgot2", "rise"), 0)
        Clock.schedule_once(lambda dt: self.hide_loading(), 0)
    
    def reset_fields(self):
        self.ids.account.text = "Masukkan alamat email"
        self.ids.otp.text = ""
        self.ids.account.error = False
        self.ids.otp.error = False
    pass

class Forgot2(MDScreen):
    def on_leave(self):
        Clock.schedule_once(lambda dt: self.reset_fields(), 0.1)
    
    def on_kv_post(self, base_widget):
        self.bind_error_style("passw1", "passw1_card", "passw1_icon")
        self.bind_error_style("passw2", "passw2_card", "passw2_icon")
        
    def bind_error_style(self, textfield_id, card_id, icon_id):
        def on_error(instance, value):
            card = self.ids[card_id]
            icon = self.ids[icon_id]
            textfield = self.ids[textfield_id]
            if value:
                card.line_color = (1, 0, 0, 1)
                icon.icon_color = (1, 0, 0, 1)
                textfield.error_color = (0, 0, 0, 0)
            else:
                card.line_color = (0.1, 0.2, 0.4, 1)
                icon.icon_color = (0.1, 0.2, 0.4, 1)
                textfield.error_color = (0, 0, 0, 0)
        self.ids[textfield_id].bind(error=on_error)
    
    def show_password(self, id):
        passw = self.ids[id]
        show_icon = self.ids[f"show_{id}"]
        passw.password = not passw.password
        show_icon.icon = "eye" if not passw.password else "eye-off"
    
    def password_input(self, textfield, is_focused, default_text, is_password=False):
        if is_focused:
            if textfield.text == default_text:
                textfield.text = ""
                if is_password:
                    textfield.password = True
        else:
            if textfield.text.strip() == "":
                textfield.text = default_text
                if is_password:
                    textfield.password = False
    
    def handle_password(self, textfield, default_text):
        if textfield.text != "" and textfield.text != default_text:
            textfield.password = True
    
    def show_loading(self, message="Sedang memproses..."):
        if hasattr(self, "loading_dialog") and self.loading_dialog:
            return
        content = MDBoxLayout(orientation="vertical", spacing=10, padding=20)
        content.add_widget(MDCircularProgressIndicator(size_hint=(None, None), size=("33dp", "33dp")))
        content.add_widget(MDLabel(text=message, halign="center", theme_font_name="Custom", font_name="Poppins-SemiBold", theme_font_size="Custom", font_size="14dp"))
        self.loading_dialog = MDDialog(
            MDDialogHeadlineText(
                text="Mohon Tunggu",
                halign="center",
                theme_font_name="Custom", 
                font_name="Poppins-Bold",
                theme_font_size="Custom",
                font_size="12dp"
            ),
            MDDialogContentContainer(
                content
            ),
            auto_dismiss=False,
            size_hint_x=.925
        )
        self.loading_dialog.open()

    def hide_loading(self):
        if hasattr(self, "loading_dialog") and self.loading_dialog:
            self.loading_dialog.dismiss()
            self.loading_dialog = None
    
    def validate_passw(self):
        self.show_loading("Mengubah kata sandi...")
        threading.Thread(target=self._validate_passw_thread, daemon=True).start()

    def _validate_passw_thread(self):
        app = MDApp.get_running_app()
        password = self.ids.passw1.text.strip()
        ulangi_password = self.ids.passw2.text.strip()
        email = app.verif_email

        def end_with_message(msg, error_field=None):
            Clock.schedule_once(lambda dt: show_message(msg), 0)
            Clock.schedule_once(lambda dt: self.hide_loading(), 0)
            if error_field:
                Clock.schedule_once(lambda dt: setattr(self.ids[error_field], 'error', True), 0)

        if not password or password == "Masukkan kata sandi baru":
            return end_with_message("Kata sandi baru harus diisi!", "passw1")
        if password != ulangi_password:
            return end_with_message("Kata sandi harus sama!", "passw2")
        try:
            response = requests.post(
                f"{API_URL}/update_password",
                json={"email": email, "new_password": password},
                timeout=10
            )
            if response.status_code == 200:
                Clock.schedule_once(lambda dt: show_message("Password berhasil diubah"), 0)
                Clock.schedule_once(lambda dt: app.change_screen("login", "rise"), 0)
            else:
                data = response.json()
                msg = data.get("message", "Gagal mengganti password")
                end_with_message(msg)
        except Exception as e:
            end_with_message(f"Error: {e}")
        Clock.schedule_once(lambda dt: self.hide_loading(), 0)
        
    def reset_fields(self):
        self.ids.passw1.text = "Masukkan kata sandi baru"
        self.ids.passw2.text = "Masukkan ulang kata sandi"
        self.ids.passw1.error = False
        self.ids.passw1.password = False
        self.ids.passw2.error = False
        self.ids.passw2.password = False
    pass

class Signup(MDScreen):
    def on_kv_post(self, base_widget):
        self.bind_error_style("nama", "nama_card", "nama_icon")
        self.bind_error_style("tanggal_lahir", "tgl_card", "tgl_icon")
        self.bind_error_style("asal", "asal_card", "asal_icon")
        self.bind_error_style("alamat", "alamat_card", "alamat_icon")

    def bind_error_style(self, textfield_id, card_id, icon_id):
        def on_error(instance, value):
            card = self.ids[card_id]
            icon = self.ids[icon_id]
            textfield = self.ids[textfield_id]
            if value:
                card.line_color = (1, 0, 0, 1)
                icon.icon_color = (1, 0, 0, 1)
                textfield.error_color = (0, 0, 0, 0)
            else:
                card.line_color = (0.1, 0.2, 0.4, 1)
                icon.icon_color = (0.1, 0.2, 0.4, 1)
                textfield.error_color = (0, 0, 0, 0)
        self.ids[textfield_id].bind(error=on_error)
    
    def update_text(self, textfield, is_focused, default_text):
        if is_focused:
            if textfield.text == default_text:
                textfield.text = ""
        else:
            if textfield.text.strip() == "":
                textfield.text = default_text
    
    def show_date_picker(self, instance, is_focused):
        if is_focused:
            self.date_picker = MDDockedDatePicker(
                text_button_ok = "Simpan",
                text_button_cancel = "Batal",
                scrim_color = (0.1, 0.2, 0.4, 1),
            )  
            self.date_picker.pos_hint = {"center_x": 0.5, "center_y": 0.5}
            self.date_picker.bind(on_ok=self.date_save,
                                  on_cancel=lambda *args: self.date_picker.dismiss())
            self.date_picker.open()

    def date_save(self, picker):
        selected_date = picker.get_date()
        self.formatted_date(selected_date)
        picker.dismiss()

    def formatted_date(self, date):
        selected_date = date[0]
        formatted = selected_date.strftime('%Y-%m-%d')
        self.ids.tanggal_lahir.text = formatted
                
    def next_signup(self):
        app = MDApp.get_running_app()
        nama = self.ids.nama.text.strip()
        tgl_lahir = self.ids.tanggal_lahir.text.strip()
        asal = self.ids.asal.text.strip()
        alamat = self.ids.alamat.text.strip()
        if not nama or nama == "Masukkan nama lengkap":
            show_message("Nama lengkap harus diisi!")
            self.ids.nama.error = True
            return
        if not tgl_lahir or tgl_lahir == "Masukkan tanggal lahir":
            show_message("Tanggal lahir harus diisi!")
            self.ids.tanggal_lahir.error = True
            return
        if not asal or asal == "Masukkan daerah asal":
            show_message("Daerah asal harus diisi!")
            self.ids.asal.error = True
            return
        if not alamat or alamat == "Masukkan alamat lengkap":
            show_message("Alamat lengkap harus diisi!")
            self.ids.alamat.error = True
            return
        app.user_data = {
            "nama": nama,
            "tgl_lahir": tgl_lahir,
            "asal": asal,
            "alamat": alamat
        }
        app.change_screen("signup2", "fade")
    
    def reset_fields(self):
        self.ids.nama.text = "Masukkan nama lengkap"
        self.ids.tanggal_lahir.text = "Masukkan tanggal lahir"
        self.ids.asal.text = "Masukkan daerah asal"
        self.ids.alamat.text = "Masukkan alamat lengkap"
        self.ids.nama.error = False
        self.ids.tanggal_lahir.error = False
        self.ids.asal.error = False
        self.ids.alamat.error = False
    pass

class Signup2(MDScreen):
    otp_storage = {}
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.countdown_event = None
        self.countdown_time = 0
    
    def on_leave(self):
        Clock.schedule_once(lambda dt: self.reset_fields(), 0.1)
    
    def on_kv_post(self, base_widget):
        self.bind_error_style("account", "account_card", "account_icon")
        self.bind_error_style("user", "user_card", "user_icon")
        self.bind_error_style("passw1", "passw1_card", "passw1_icon")
        self.bind_error_style("passw2", "passw2_card", "passw2_icon")
        self.bind_error_style("otp", "otp_card", "otp_icon")
        
    def bind_error_style(self, textfield_id, card_id, icon_id):
        def on_error(instance, value):
            card = self.ids[card_id]
            icon = self.ids[icon_id]
            textfield = self.ids[textfield_id]
            if value:
                card.line_color = (1, 0, 0, 1)
                icon.icon_color = (1, 0, 0, 1)
                textfield.error_color = (0, 0, 0, 0)
            else:
                card.line_color = (0.1, 0.2, 0.4, 1)
                icon.icon_color = (0.1, 0.2, 0.4, 1)
                textfield.error_color = (0, 0, 0, 0)
        self.ids[textfield_id].bind(error=on_error)
    
    def update_text(self, textfield, is_focused, default_text):
        if is_focused:
            if textfield.text == default_text:
                textfield.text = ""
        else:
            if textfield.text.strip() == "":
                textfield.text = default_text
    
    def show_password(self, id):
        passw = self.ids[id]
        show_icon = self.ids[f"show_{id}"]
        passw.password = not passw.password
        show_icon.icon = "eye" if not passw.password else "eye-off"
    
    def password_input(self, textfield, is_focused, default_text, is_password=False):
        if is_focused:
            if textfield.text == default_text:
                textfield.text = ""
                if is_password:
                    textfield.password = True
        else:
            if textfield.text.strip() == "":
                textfield.text = default_text
                if is_password:
                    textfield.password = False
    
    def handle_password(self, textfield, default_text):
        if textfield.text != "" and textfield.text != default_text:
            textfield.password = True

    def generate_otp(self, length=6):
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])

    def send_email_otp(self):
        if self.countdown_time > 0:
            return
        email = self.ids.account.text.strip()
        otp = self.generate_otp()
        Signup2.otp_storage[email] = otp
        if not email or email == "Masukkan alamat email":
            show_message("Email tidak boleh kosong")
        elif self._send_email(email, otp):
            show_message("OTP berhasil dikirim")
            self.start_countdown(60)
        else:
            show_message("Gagal mengirim OTP, coba lagi beberapa saat!")

    def _send_email(self, email, otp):
        sender_email = 'streetcareapps@gmail.com'
        sender_password = 'pett dofw ntse xxvi'
        subject = 'StreetCare: Kode OTP Verifikasi Akun'

        plain_body = f"""
            Halo Sobat StreetCare! 🛣️

            Kode OTP kamu adalah:
            
                    {otp}
            
            NOTE:
            Jangan bagikan kode ini ke siapapun, ya!
            
            Masukkan kode ini untuk memverifikasi akun dan mulai melaporkan jalan rusak di sekitarmu.
            Terima kasih sudah peduli dengan jalan kita!

            Salam,
            Tim StreetCare
            """
        html_body = f"""
            <html>
            <head>
            <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #ffffff;
                color: #000000;
            }}
            .otp {{
                display: block;
                font-size: 24px;
                font-weight: bold;
                margin: 10px 0;
                color: #000000;
            }}
            @media (prefers-color-scheme: dark) {{
                body {{
                background-color: #000000;
                color: #ffffff;
                }}
                .otp {{
                color: #ffffff;
                }}
            }}
            </style>
            </head>
            <body>
            <p>Halo Sobat <strong>StreetCare</strong>! 🛣️</p>
            <p>Kode OTP kamu adalah:</p>
            <span class="otp">{otp}</span>
            <p><strong>NOTE:</strong><br>Jangan bagikan kode ini ke siapapun, ya!</p>
            <p>Masukkan kode ini untuk memverifikasi akun dan mulai melaporkan jalan rusak di sekitarmu.</p>
            <p>Terima kasih sudah peduli dengan jalan kita!</p>
            <p>Salam,<br>Tim StreetCare</p>
            </body>
            </html>
            """
        msg = MIMEMultipart("alternative")
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(plain_body, "plain"))
        msg.attach(MIMEText(html_body, "html"))
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, email, msg.as_string())
            return True
        except Exception as e:
            print("Gagal kirim email:", e)
            return False

    def start_countdown(self, seconds):
        self.countdown_time = seconds
        self.update_label_countdown()
        self.countdown_event = Clock.schedule_interval(self._update_countdown, 1)

    def _update_countdown(self, dt):
        self.countdown_time -= 1
        self.update_label_countdown()
        if self.countdown_time <= 0:
            self.countdown_event.cancel()
            self.countdown_event = None

    def update_label_countdown(self):
        if self.countdown_time > 0:
            self.ids.otp_label.text = f"[u]Kirimkan kode ({self.countdown_time})[/u]"
        else:
            self.ids.otp_label.text = "[u]Kirimkan kode[/u]"
    
    def show_loading(self, message="Sedang memproses..."):
        if hasattr(self, "loading_dialog") and self.loading_dialog:
            return
        content = MDBoxLayout(orientation="vertical", spacing=10, padding=20)
        content.add_widget(MDCircularProgressIndicator(size_hint=(None, None), size=("33dp", "33dp")))
        content.add_widget(MDLabel(text=message, halign="center", theme_font_name="Custom", font_name="Poppins-SemiBold", theme_font_size="Custom", font_size="14dp"))
        self.loading_dialog = MDDialog(
            MDDialogHeadlineText(
                text="Mohon Tunggu",
                halign="center",
                theme_font_name="Custom", 
                font_name="Poppins-Bold",
                theme_font_size="Custom",
                font_size="12dp"
            ),
            MDDialogContentContainer(
                content
            ),
            auto_dismiss=False,
            size_hint_x=.925
        )
        self.loading_dialog.open()

    def hide_loading(self):
        if hasattr(self, "loading_dialog") and self.loading_dialog:
            self.loading_dialog.dismiss()
            self.loading_dialog = None
    
    def verify_signup(self):
        self.show_loading("Memproses signup...")
        threading.Thread(target=self.verify_signup_thread, daemon=True).start()
    
    def verify_signup_thread(self):
        app = MDApp.get_running_app()
        username = self.ids.user.text.strip()
        email = self.ids.account.text.strip()
        password = self.ids.passw1.text.strip()
        ulangi_password = self.ids.passw2.text
        otp = self.ids.otp.text
        saved_otp = Signup2.otp_storage.get(email)
        
        def show_and_hide(msg):
            Clock.schedule_once(lambda dt: show_message(msg), 0)
            Clock.schedule_once(lambda dt: self.hide_loading(), 0)
        
        if not email or email == "Masukkan alamat email":
            show_and_hide("Email harus diisi!")
            self.ids.account.error = True
            return
        elif not is_valid_email(email):
            show_and_hide("Email tidak valid.")
            self.ids.account.error = True
            return
        elif is_email_registered(email):
            show_and_hide("Email sudah terdaftar!")
            self.ids.account.error = True
            return
        if not username or username == "Masukkan username":
            show_and_hide("Username harus diisi!")
            self.ids.user.error = True
            return
        elif len(username) > 12:
            show_and_hide("Username maksimal 12 karakter!")
            self.ids.user.error = True
            return
        elif is_username_registered(username):
            show_and_hide("Username sudah terdaftar!")
            self.ids.user.error = True
            return
        if not password or password == "Masukkan kata sandi":
            show_and_hide("Kata sandi harus diisi!")
            self.ids.passw1.error = True
            return
        elif password != ulangi_password:
            show_and_hide("Kata sandi harus sama!")
            self.ids.passw2.error = True
            return
        if not otp:
            show_and_hide("Kode OTP harus diisi!")
            self.ids.otp.error = True
            return
        if not saved_otp:
            show_and_hide("Kode OTP belum dikirim atau sudah kadaluarsa.")
            self.ids.otp.error = True
            return
        elif otp != saved_otp:
            show_and_hide("Kode OTP tidak sesuai.")
            self.ids.otp.error = True
            return
        user_data = app.user_data
        user_data.update({
            "username": username,
            "email": email,
            "password": password
        })
        if save_user_to_database(user_data):
            Clock.schedule_once(lambda dt: show_message("Sign up berhasil. Silahkan login kembali!"), 0)
            signup = app.root.get_screen("signup")
            Clock.schedule_once(lambda dt: signup.reset_fields(), 0)
            Clock.schedule_once(lambda dt: self.reset_fields(), 0)
            Clock.schedule_once(lambda dt: app.change_screen("login", "rise"), 0)
        else:
            Clock.schedule_once(lambda dt: show_message("Sign up gagal, coba lagi setelah beberapa saat."), 0)
        Clock.schedule_once(lambda dt: self.hide_loading(), 0)
    
    def reset_fields(self):
        self.ids.user.text = "Masukkan username"
        self.ids.account.text = "Masukkan alamat email"
        self.ids.passw1.text = "Masukkan kata sandi"
        self.ids.passw2.text = "Ulangi kata sandi"
        self.ids.otp.text = ""
        self.ids.user.error = False
        self.ids.account.error = False
        self.ids.passw1.error = False
        self.ids.passw1.password = False
        self.ids.passw2.error = False
        self.ids.passw2.password = False
        self.ids.otp.error = False
    pass

class Home(MDScreen):
    def on_pre_enter(self):
        app = MDApp.get_running_app()
        username = ""
        if hasattr(app, "admin_data") and app.admin_data:
            username = app.admin_data.get("username", "")
        elif hasattr(app, "user_data") and app.user_data:
            username = app.user_data.get("username", "")
        if username:
            self.ids.user.text = username
        else:
            print("Tidak ada data user/admin yang ditemukan.")
        
    def on_enter(self):
        if not hasattr(self, 'mapview'):
            app = MDApp.get_running_app()
            container = self.ids.map_container
            container.clear_widgets()
            if app.mapview.parent:
                app.mapview.parent.remove_widget(app.mapview)
            app.mapview.size_hint = (0.965, 0.95)
            container.add_widget(app.mapview)
    
    def goto_camera(self):
        app = MDApp.get_running_app()
        Clock.schedule_once(lambda dt: app.change_screen("camera", ""), 0.3)
    pass

class Maps(MDScreen):
    def on_leave(self):
        Clock.schedule_once(lambda dt: self.reset_fields(), 0.1)
    
    def on_enter(self):
        if not hasattr(self, 'mapview'):
            app = MDApp.get_running_app()
            container = self.ids.map_container
            container.clear_widgets()
            if app.mapview.parent:
                app.mapview.parent.remove_widget(app.mapview)
            app.mapview.size_hint = (1, 1)
            container.add_widget(app.mapview)
    
    def goto_camera(self):
        app = MDApp.get_running_app()
        Clock.schedule_once(lambda dt: app.change_screen("camera", ""), 0.3)
                     
    def update_text(self, is_focused):
        default_text = "Cari laporan jalan..."
        textfield = self.ids.search_field
        if is_focused:
            if textfield.text == default_text:
                textfield.text = ""
        else:
            if textfield.text.strip() == "":
                textfield.text = default_text
    
    def search_by_street_name(self, street_name):
        app = MDApp.get_running_app()
        street_name = street_name.strip().lower()
        found_markers = []
        if street_name == "cari laporan jalan...":
            show_message("Nama jalan kosong")
            return
        
        marker_layer = None
        for child in app.mapview.children:
            if child.__class__.__name__ == 'MarkerMapLayer':
                marker_layer = child
                break
        if not marker_layer:
            print("Layer marker tidak ditemukan")
            return

        for marker in marker_layer.children:
            if isinstance(marker, MyCustomMarker):
                if street_name in marker.nama_jalan.strip().lower():
                    found_markers.append(marker)
        if found_markers:
            first_marker = found_markers[0]
            app.mapview.center_on(first_marker.lat, first_marker.lon)
            first_marker.on_release()
            if len(found_markers) > 1:
                show_message(f"{len(found_markers)} laporan ditemukan.")
        else:
            show_message("Tidak ada laporan di jalan ini.") 
            
    def reset_fields(self):
        self.ids.search_field.text = "Cari laporan jalan..."
    pass

INDO_MONTHS = {
    "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "Mei", "06": "Jun",
    "07": "Jul", "08": "Agu", "09": "Sep", "10": "Okt", "11": "Nov", "12": "Des"
}
class Reports(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_projects = []
        self.active_project = None
        self.current_page = 1
        self.items_per_page = 2
        self.report_url = ""
        self.final_url = ""
        self.selected_start_date = None
        self.selected_end_date = None
        self.rancangan_comments = []
        self.akhir_comments = []
    
    def on_enter(self, *args):
        if not MDApp.get_running_app().admin_data:
            self.ids.admin_report.opacity = 0
            self.ids.admin_report.disabled = True
        else:
            self.ids.admin_report.opacity = 1
            self.ids.admin_report.disabled = False
        
        self.show_loading("Sedang memuat...")
        Thread(target=self.load_projects_thread, daemon=True).start()
        
    def format_period_display(self, start_date: str, end_date: str) -> str:
        try:
            start_day, start_month, start_year = start_date.split("/")
            end_day, end_month, end_year = end_date.split("/")
            if start_month == end_month and start_year == end_year:
                return f"{INDO_MONTHS[start_month]} {start_year}"
            elif start_year == end_year:
                return f"{INDO_MONTHS[start_month]} - {INDO_MONTHS[end_month]} {start_year}"
            else:
                return f"{INDO_MONTHS[start_month]} {start_year} - {INDO_MONTHS[end_month]} {end_year}"
        except:
            return ""
    
    def load_projects_thread(self):
        try:
            response = requests.get(f"{API_URL}/get_all_project_fund")
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    projects = []
                    for fund in data["data"]:
                        start_date = fund.get("start_date")
                        end_date = fund.get("end_date")
                        if start_date and end_date and start_date != "0000-00-00" and end_date != "0000-00-00":
                            try:
                                period = self.format_period_display(start_date, end_date)
                            except:
                                period = ""
                            projects.append({
                                "text": fund['street_name'],
                                "period": period,
                                "fund_data": fund
                            })
                    Clock.schedule_once(lambda dt: self.finish_load_projects(projects))
            else:
                Clock.schedule_once(lambda dt: self.hide_loading())
        except Exception as e:
            print("Gagal mengambil data:", e)
            Clock.schedule_once(lambda dt: self.hide_loading())
    
    def finish_load_projects(self, projects_data):
        self.all_projects.clear()
        for item in projects_data:
            card = ProjectList(
                text=item["text"],
                period=item["period"],
                fund_data=item["fund_data"],
                parent_screen=self
            )
            self.all_projects.append(card)
        self.current_page = 1
        self.load_page()
        self.hide_loading() 
    
    def load_page(self):
        self.ids.project_list.clear_widgets()
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        for widget in self.all_projects[start:end]:
            self.ids.project_list.add_widget(widget)
        total_pages = max(1, (len(self.all_projects) + self.items_per_page - 1) // self.items_per_page)
        self.ids.page_label.text = f"Page {self.current_page} of {total_pages}"
        self.ids.prev_button.disabled = self.current_page <= 1
        self.ids.next_button.disabled = self.current_page >= total_pages

    def next_page(self):
        total_pages = max(1, (len(self.all_projects) + self.items_per_page - 1) // self.items_per_page)
        if self.current_page < total_pages:
            self.current_page += 1
            self.load_page()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_page()
    
    def format_rupiah(self, value):
        try:
            value = int(float(value)) if value is not None else 0
            return f"Rp {value:,}".replace(",", ".")
        except (ValueError, TypeError):
            return "Rp 0"

    def terbilang(self, value):
        try:
            value = int(float(value)) if value is not None else None
            if value is not None:
                return f"({num2words(value, lang='id').capitalize()} Rupiah)"
            else:
                return "(Belum ada data)"
        except (ValueError, TypeError):
            return "(Belum ada data)"
    
    def show_loading(self, message="Sedang memproses..."):
        if hasattr(self, "loading_dialog") and self.loading_dialog:
            return
        content = MDBoxLayout(orientation="vertical", spacing=10, padding=20)
        content.add_widget(MDCircularProgressIndicator(size_hint=(None, None), size=("33dp", "33dp")))
        content.add_widget(MDLabel(text=message, halign="center", theme_font_name="Custom", font_name="Poppins-SemiBold", theme_font_size="Custom", font_size="14dp"))
        self.loading_dialog = MDDialog(
            MDDialogHeadlineText(
                text="Mohon Tunggu",
                halign="center",
                theme_font_name="Custom", 
                font_name="Poppins-Bold",
                theme_font_size="Custom",
                font_size="12dp"
            ),
            MDDialogContentContainer(
                content
            ),
            auto_dismiss=False,
            size_hint_x=.925
        )
        self.loading_dialog.open()

    def hide_loading(self):
        if hasattr(self, "loading_dialog") and self.loading_dialog:
            self.loading_dialog.dismiss()
            self.loading_dialog = None
    
    def load_project_detail(self, fund):
        def fetch():
            try:
                total_plan = fund.get("total_estimated", 0)
                total_plan_formatted = self.format_rupiah(total_plan)
                total_plan_terbilang = self.terbilang(total_plan)
                total_final = fund.get("total_final", 0)
                total_final_formatted = self.format_rupiah(total_final)
                total_final_terbilang = self.terbilang(total_final)
                report_url = fund.get("estimated_pdf")
                final_url = fund.get("final_pdf")

                def update_ui(dt):
                    self.ids.dana1.text = total_plan_formatted
                    self.ids.terbilang1.text = total_plan_terbilang
                    self.ids.dana2.text = total_final_formatted
                    self.ids.terbilang2.text = total_final_terbilang

                    self.load_pdf_cover(report_url, final_url)
                    self.hide_loading()
                Clock.schedule_once(update_ui)
            except Exception as e:
                print("Gagal load detail:", e)
                Clock.schedule_once(lambda dt: self.hide_loading())
        Thread(target=fetch).start()
            
    def download_pdf_from_url(self, url):
        try:
            # if platform == "android":
            #     from android.storage import app_storage_path
            #     save_dir = os.path.join(app_storage_path(), "pdf_temp")
            # else:
            save_dir = os.path.join(os.getcwd(), "pdf_temp")

            os.makedirs(save_dir, exist_ok=True)
            filename = f"{uuid.uuid4()}.pdf"
            save_path = os.path.join(save_dir, filename)
            response = requests.get(url)
            if response.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(response.content)
                return save_path
            else:
                return None
        except Exception as e:
            print(f"Gagal mengunduh PDF: {e}")
            return None
    
    def load_pdf_cover(self, report_url, final_url, on_complete=None):
        self.report_url = report_url
        self.final_url = final_url

        def clear_widgets(dt):
            self.ids.pdf_card1.clear_widgets()
            self.ids.pdf_card2.clear_widgets()
            spinner1 = MDCircularProgressIndicator(size_hint=(None, None), size=("30dp", "30dp"), pos_hint={"center_x": 0.5, "center_y": 0.5})
            spinner2 = MDCircularProgressIndicator(size_hint=(None, None), size=("30dp", "30dp"), pos_hint={"center_x": 0.5, "center_y": 0.5})
            self.ids.pdf_card1.add_widget(spinner1)
            self.ids.pdf_card2.add_widget(spinner2)
        Clock.schedule_once(clear_widgets)

        def load_pdf1_thread():
            local_path = None
            if report_url:
                Clock.schedule_once(lambda dt: (
                    setattr(self.ids.btn_rancangan, "disabled", True),
                    setattr(self.ids.btn_rancangan, "opacity", 0.2)
                ))
                full_url = f"{API_URL}/{report_url}"
                local_path = self.download_pdf_from_url(full_url)

            def update_ui(dt):
                self.ids.pdf_card1.clear_widgets()
                if local_path:
                    viewer1 = PDFView(pdf_path=local_path, target_widget=self.ids.pdf_card1)
                    self.ids.pdf_card1.add_widget(viewer1)
                else:
                    self.ids.date1.text = "(Belum ada data)"
                self.ids.btn_rancangan.disabled = False
                self.ids.btn_rancangan.opacity = 1
            Clock.schedule_once(update_ui)

        def load_pdf2_thread():
            local_path = None
            if final_url:
                Clock.schedule_once(lambda dt: (
                    setattr(self.ids.btn_akhir, "disabled", True),
                    setattr(self.ids.btn_akhir, "opacity", 0.2)
                ))
                full_url = f"{API_URL}/{final_url}"
                local_path = self.download_pdf_from_url(full_url)

            def update_ui(dt):
                self.ids.pdf_card2.clear_widgets()
                if local_path:
                    viewer2 = PDFView(pdf_path=local_path, target_widget=self.ids.pdf_card2)
                    self.ids.pdf_card2.add_widget(viewer2)
                else:
                    self.ids.date2.text = "(Belum ada data)"
                self.ids.btn_akhir.disabled = False
                self.ids.btn_akhir.opacity = 1
                
                if on_complete:
                    on_complete()
            Clock.schedule_once(update_ui)
        Thread(target=load_pdf1_thread).start()
        Thread(target=load_pdf2_thread).start()

    def download_rancangan(self):
        if self.report_url:
            def download_thread():
                Clock.schedule_once(lambda dt: setattr(self.ids.btn_rancangan, "disabled", True))
                Clock.schedule_once(lambda dt: self.show_loading("Mengunduh laporan..."))

                full_url = f"{API_URL}/{self.report_url}"
                self._download_pdf(full_url, "laporan_rancangan.pdf")

                Clock.schedule_once(lambda dt: setattr(self.ids.btn_rancangan, "disabled", False))
                Clock.schedule_once(lambda dt: self.hide_loading())

            Thread(target=download_thread).start()
        else:
            show_message("Tidak ada laporan rancangan untuk diunduh.")

    def download_akhir(self):
        if self.final_url:
            def download_thread():
                Clock.schedule_once(lambda dt: setattr(self.ids.btn_akhir, "disabled", True))
                Clock.schedule_once(lambda dt: self.show_loading("Mengunduh laporan..."))

                full_url = f"{API_URL}/{self.final_url}"
                self._download_pdf(full_url, "laporan_akhir.pdf")

                Clock.schedule_once(lambda dt: setattr(self.ids.btn_akhir, "disabled", False))
                Clock.schedule_once(lambda dt: self.hide_loading())

            Thread(target=download_thread).start()
        else:
            show_message("Tidak ada laporan akhir untuk diunduh.")

    def _download_pdf(self, file_url, file_name):
        try:
            response = requests.get(file_url, stream=True, timeout=10)
            if response.status_code == 200:
                if platform == "win":
                    downloads_folder = os.path.join(os.environ["USERPROFILE"], "Downloads")
                # elif platform == "android":
                #     from android.storage import primary_external_storage_path
                #     downloads_folder = os.path.join(primary_external_storage_path(), "Download")
                else:
                    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

                save_path = os.path.join(downloads_folder, file_name)
                with open(save_path, "wb") as f:
                    f.write(response.content)
                    
                Clock.schedule_once(lambda dt: show_message(f"Berhasil mengunduh: {file_name}"))
            else:
                Clock.schedule_once(lambda dt: show_message("Gagal mengunduh PDF."))
        except Exception as e:
            Clock.schedule_once(lambda dt: show_message(f"Terjadi error: {str(e)}"))
    
    def show_date_picker(self, *args):
        picker = MDModalInputDatePicker(
            mode="range",
            text_button_ok="Selesai",
            text_button_cancel="Batal",
            scrim_color=(0.1, 0.2, 0.4, 1),
            date_format="dd/mm/yyyy"
        )
        picker.supporting_text = "Pilih Rentang Bulan & Tahun"
        picker.supporting_input_text = "(Abaikan tanggal)"
        picker.bind(
            on_ok=self.date_save,
            on_cancel=lambda *args: picker.dismiss()
        )
        picker.open()

    def date_save(self, picker):
        selected_range = picker.get_date()
        if selected_range and len(selected_range) == 2:
            self.selected_start_date, self.selected_end_date = selected_range
            self.format_date_range(selected_range)
            self.filter_projects()
        picker.dismiss()
    
    def filter_projects(self):
        if not self.selected_start_date or not self.selected_end_date:
            return
        start_month = self.selected_start_date.month
        start_year = self.selected_start_date.year
        end_month = self.selected_end_date.month
        end_year = self.selected_end_date.year
        filtered_projects = []
        for card in self.all_projects:
            fund = card.fund_data
            start_date_str = fund.get("start_date")
            if start_date_str and start_date_str != "0000-00-00":
                try:
                    project_date = datetime.strptime(start_date_str, "%d/%m/%Y")
                    project_month = project_date.month
                    project_year = project_date.year
                    project_val = project_year * 12 + project_month
                    start_val = start_year * 12 + start_month
                    end_val = end_year * 12 + end_month

                    if start_val <= project_val <= end_val:
                        filtered_projects.append(card)
                except Exception as e:
                    print("Format tanggal salah:", e)
        self.current_page = 1
        self.display_filtered_projects(filtered_projects)
        
    def display_filtered_projects(self, projects):
        self.filtered_projects = projects
        self.ids.project_list.clear_widgets()
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        for widget in self.filtered_projects[start:end]:
            self.ids.project_list.add_widget(widget)
        total_pages = max(1, (len(self.filtered_projects) + self.items_per_page - 1) // self.items_per_page)
        self.ids.page_label.text = f"Page {self.current_page} of {total_pages}"
        self.ids.prev_button.disabled = self.current_page <= 1
        self.ids.next_button.disabled = self.current_page >= total_pages
    
    def reset_filter(self):
        self.selected_start_date = None
        self.selected_end_date = None
        self.current_page = 1
        self.ids.rentang.text = "Pilih dahulu"
        self.load_page()

    def format_date_range(self, date_range):
        if date_range and len(date_range) == 2:
            start_date, end_date = date_range
            start_month = start_date.strftime("%b")
            end_month = end_date.strftime("%b")
            start_year = start_date.year
            end_year = end_date.year
            if start_year != end_year:
                formatted = f"{start_month} {start_year} - {end_month} {end_year}"
            else:
                formatted = f"{start_month} - {end_month} {start_year}"
            self.ids.rentang.text = formatted
    
    def update_text(self, textfield, is_focused, default_text):
        if is_focused:
            if textfield.text == default_text:
                textfield.text = ""
        else:
            if textfield.text.strip() == "":
                textfield.text = default_text
    
    def show_comments(self, tipe):
        if not self.active_project:
            show_message("Pilih proyek terlebih dahulu.")
            return
        self.current_comment_type = tipe
        bottom_sheet = self.ids.comment_sheet
        container = self.ids.comments
        container.clear_widgets()
        if tipe == "rancangan":
            if not self.active_project.fund_data.get("estimated_pdf"):
                show_message("Tidak ada data laporan rancangan.")
                return
            komentar_list = self.rancangan_comments
        elif tipe == "akhir":
            if not self.active_project.fund_data.get("final_pdf"):
                show_message("Tidak ada data laporan akhir.")
                return
            komentar_list = self.akhir_comments
        else:
            show_message("Terjadi kesalahan.")
            return
        for data in komentar_list:
            username = data["username"]
            teks = data["comment_text"]
            item_layout = BoxLayout(
                orientation="horizontal",
                spacing=dp(8),
                size_hint_y=None
            )
            item_layout.bind(minimum_height=item_layout.setter("height"))
            profile_icon = MDIcon(
                icon="account-circle",
                pos_hint={"center_y": 0.5},
                theme_font_size="Custom",
                font_size="35sp",
                size_hint=(None, None),
                size=(dp(32), dp(32)),
                theme_text_color="Custom",
                text_color=(0.2, 0.2, 0.2, 1),
            )
            text_container = BoxLayout(
                orientation="vertical",
                spacing=dp(1),
                size_hint_y=None,
            )
            text_container.bind(minimum_height=text_container.setter("height"))
            user_label = MDLabel(
                text=username,
                theme_text_color="Custom",
                text_color=(0.1, 0.2, 0.4, 1),
                theme_font_size="Custom",
                font_size="11sp",
                theme_font_name="Custom",
                font_name="Poppins-Bold",
                halign="left",
                adaptive_height=True,
            )
            comment_label = MDLabel(
                text=teks,
                theme_text_color="Custom",
                text_color=(0.1, 0.2, 0.4, 1),
                theme_font_size="Custom",
                font_size="13.5sp",
                theme_font_name="Custom",
                font_name="Poppins-Medium",
                halign="left",
                adaptive_height=True,
            )
            reply_label = MDLabel(
                text="[u]Balas[/u]",
                markup=True,
                theme_text_color="Custom",
                text_color=(0.1, 0.2, 0.4, 1),
                theme_font_size="Custom",
                font_size="10.5sp",
                theme_font_name="Custom",
                font_name="Poppins-SemiBold",
                halign="left",
                adaptive_height=True,
                # on_touch_down=lambda instance, touch: (
                #     self.balas_komentar(username, teks)
                #     if instance.collide_point(*touch.pos)
                #     else None
                # ),
            )
            
            text_container.add_widget(user_label)
            text_container.add_widget(comment_label)
            text_container.add_widget(reply_label)
            item_layout.add_widget(profile_icon)
            item_layout.add_widget(text_container)
            container.add_widget(item_layout)
        bottom_sheet.set_state("open")
        
    def load_comments(self, comment_type):
        if not self.active_project:
            Clock.schedule_once(lambda dt: show_message("Pilih proyek terlebih dahulu"))
            return
        try:
            project_id = self.active_project.fund_data["id"]
            url = f"{API_URL}/get_comments?project_id={project_id}&comment_type={comment_type}"
            response = requests.get(url)
            if response.status_code == 200:
                comments = response.json().get("data", [])
                if comment_type == "rancangan":
                    self.rancangan_comments = comments
                else:
                    self.akhir_comments = comments
            else:
                Clock.schedule_once(lambda dt: show_message("Gagal memuat komentar"))
        except Exception as e:
            Clock.schedule_once(lambda dt, err=e: show_message(f"Error: {err}"))
    
    def send_comment(self):
        text = self.ids.comment.text.strip()
        if not text or text == "Tambahkan komentar":
            Clock.schedule_once(lambda dt: show_message("Komentar tidak boleh kosong"))
            return
        
        app = MDApp.get_running_app()
        if app.admin_data:
            username = app.admin_data.get("username", "Admin")
            user_id = app.admin_data.get("id", 0)
        elif app.user_data:
            username = app.user_data.get("username", "Anonim")
            user_id = app.user_data.get("id", 0)
        else:
            Clock.schedule_once(lambda dt: show_message("Tidak ada user yang login"))
            return
        
        project_id = self.active_project.fund_data["id"]
        tipe = self.current_comment_type
        data = {
            "project_id": project_id,
            "user_id": user_id,
            "username": username,
            "comment_text": text,
            "comment_type": tipe
        }
        try:
            response = requests.post(f"{API_URL}/add_comment", json=data)
            if response.status_code in (200, 201):
                Clock.schedule_once(lambda dt: show_message("Komentar berhasil dikirim!"))
                comment_obj = {"username": username, "comment_text": text}
                if tipe == "rancangan":
                    self.rancangan_comments.append(comment_obj)
                else:
                    self.akhir_comments.append(comment_obj)
                self.ids.comment.text = "Tambahkan komentar"
                self.load_comments(tipe)
                Clock.schedule_once(lambda dt: self.show_comments(tipe), 0.2) 
            else:
                Clock.schedule_once(lambda dt: show_message(f"Gagal mengirim komentar: {response.text}"))
        except Exception as e:
            Clock.schedule_once(lambda dt, err=e: show_message(f"Error: {err}"))

    pass

class TransparentTouchCard(MDCard):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            return False
        return super().on_touch_down(touch)

class Adminreport(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pdf_paths = {}
        self.pdf_download_complete = {}
    
    def on_kv_post(self, base_widget):
        self.bind_error_style("jalan", "jalan_card", "jalan_icon")
        self.bind_error_style("periode", "periode_card", "periode_icon")
        self.bind_error_style("rd", "rd_card", "rd_icon")
        self.bind_error_style("ad", "ad_card", "ad_icon")

    def on_leave(self):
        Clock.schedule_once(lambda dt: self.reset_fields(), 0.1)
        Clock.schedule_once(lambda dt: self.reset_pdf_card('pdf_card1'), 0.1)
        Clock.schedule_once(lambda dt: self.reset_pdf_card('pdf_card2'), 0.1)
    
    def reset_fields(self):
        self.ids.jalan.text = "Masukkan nama jalan"
        self.ids.periode.text = "Masukkan periode proyek"
        self.ids.rd.text = "Masukkan total rancangan dana"
        self.ids.ad.text = "Masukkan total akhir dana"
        self.ids.jalan.error = False
        self.ids.periode.error = False
        self.ids.rd.error = False
        self.ids.ad.error = False
    
    def reset_pdf_card(self, card_id, *args):
        card = self.ids.get(card_id)
        if not card:
            return
        card.clear_widgets()
        layout = RelativeLayout()
        upload_icon = MDIcon(
            id=f"upload_icon_{card_id}",
            icon="upload",
            theme_icon_color="Custom",
            icon_color=(0.1, 0.2, 0.4, 1),
            theme_font_size="Custom",
            font_size="25sp",
            pos_hint={"center_x": 0.315, "center_y": 0.5}
        )
        label = MDLabel(
            text="Unggah PDF",
            pos_hint={"center_x": 0.545, "center_y": 0.47},
            theme_text_color="Custom",
            text_color=(0.1, 0.2, 0.4, 1),
            theme_font_size="Custom",
            font_size="12sp",
            halign="center",
            theme_font_name="Custom",
            font_name="Poppins-SemiBold"
        )
        layout.add_widget(upload_icon)
        layout.add_widget(label)
        card.add_widget(layout)

    def bind_error_style(self, textfield_id, card_id, icon_id):
        def on_error(instance, value):
            card = self.ids[card_id]
            icon = self.ids[icon_id]
            textfield = self.ids[textfield_id]
            if value:
                card.line_color = (1, 0, 0, 1)
                icon.icon_color = (1, 0, 0, 1)
                textfield.error_color = (0, 0, 0, 0)
            else:
                card.line_color = (0.1, 0.2, 0.4, 1)
                icon.icon_color = (0.1, 0.2, 0.4, 1)
                textfield.error_color = (0, 0, 0, 0)
        self.ids[textfield_id].bind(error=on_error)
    
    def update_text(self, textfield, is_focused, default_text):
        if is_focused:
            if textfield.text == default_text:
                textfield.text = ""
        else:
            if textfield.text.strip() == "":
                textfield.text = default_text
                
    def format_rupiah(self, nominal):
        angka = str(nominal).replace(".", "").replace(",", "")
        if angka.isdigit():
            return f"{int(angka):,}".replace(",", ".")
        else:
            return ""
    
    def show_loading(self, message="Sedang memproses..."):
        if hasattr(self, "loading_dialog") and self.loading_dialog:
            return
        content = MDBoxLayout(orientation="vertical", spacing=10, padding=20)
        content.add_widget(MDCircularProgressIndicator(size_hint=(None, None), size=("33dp", "33dp")))
        content.add_widget(MDLabel(text=message, halign="center", theme_font_name="Custom", font_name="Poppins-SemiBold", theme_font_size="Custom", font_size="14dp"))
        self.loading_dialog = MDDialog(
            MDDialogHeadlineText(
                text="Mohon Tunggu",
                halign="center",
                theme_font_name="Custom", 
                font_name="Poppins-Bold",
                theme_font_size="Custom",
                font_size="12dp"
            ),
            MDDialogContentContainer(
                content
            ),
            auto_dismiss=False,
            size_hint_x=.925
        )
        self.loading_dialog.open()

    def hide_loading(self):
        if hasattr(self, "loading_dialog") and self.loading_dialog:
            self.loading_dialog.dismiss()
            self.loading_dialog = None
    
    def cek_nama_jalan(self):
        nama_jalan = self.ids.jalan.text.strip()
        if not nama_jalan:
            self.ids.jalan.error = True
            show_message("Nama jalan tidak boleh kosong")
            return
        self.show_loading("Mengecek nama jalan...")
        threading.Thread(target=self._cek_nama_jalan_thread, args=(nama_jalan,), daemon=True).start()

    def _cek_nama_jalan_thread(self, nama_jalan):
        try:
            response = requests.post(f"{API_URL}/check_street_fund", data={'nama_jalan': nama_jalan})
            result = response.json()
            Clock.schedule_once(lambda dt: self.hide_loading())
            if response.status_code == 200 and result['status'] == 'exists':
                Clock.schedule_once(lambda dt: self._isi_field_dari_data(result['data']))
            elif result['status'] == 'pending':
                Clock.schedule_once(lambda dt: show_message("Terdapat laporan user dengan jalan serupa. Harap approve dahulu!"))
            elif result['status'] == 'not_found':
                Clock.schedule_once(lambda dt: show_message("Nama jalan tidak ditemukan."))
            else:
                Clock.schedule_once(lambda dt: show_message(result.get("message", "Gagal memuat data.")))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.hide_loading())
            Clock.schedule_once(lambda dt, err=e: show_message(f"Error: {err}"))

    def _isi_field_dari_data(self, data):
        def update_ui(dt):
            if not any([data.get('total_estimated'), data.get('estimated_pdf'), data.get('total_final'), data.get('final_pdf')]):
                Clock.schedule_once(lambda dt: show_message("Nama jalan telah diapprove. Lanjutkan pengisian!"))
                return
            self.ids.jalan.text = data['street_name']
            self.ids.periode.text = f"{data['start_date']} - {data['end_date']}"
            self.ids.rd.text = str(data.get('total_estimated') or 'Masukkan total rancangan dana')
            self.ids.ad.text = str(data.get('total_final') or 'Masukkan total akhir dana')
            if data.get('estimated_pdf'):
                self.set_pdf_filename('pdf_card1', data['estimated_pdf'], from_server=True)
            if data.get('final_pdf'):
                self.set_pdf_filename('pdf_card2', data['final_pdf'], from_server=True)
            Clock.schedule_once(lambda dt: show_message("Berhasil memuat data jalan."))
        Clock.schedule_once(update_ui)

    def kirim_laporan_dana(self):
        nama_jalan = self.ids.jalan.text.strip()
        periode = self.ids.periode.text.strip()
        total_r = self.ids.rd.text.strip()
        total_a = self.ids.ad.text.strip()

        valid = True
        if not nama_jalan or nama_jalan == "Masukkan nama jalan":
            self.ids.jalan.error = True
            valid = False
        if not periode or periode == "Masukkan periode proyek":
            self.ids.periode.error = True
            valid = False
        if not total_r or total_r == "Masukkan total rancangan dana":
            self.ids.rd.error = True
            valid = False
        if not total_a or total_a == "Masukkan total akhir dana":
            total_a = None
        if not self.pdf_paths.get('pdf_card1'):
            show_message("PDF rancangan wajib diunggah")
            valid = False
        if not valid:
            show_message("Isikan data dengan lengkap!")
            return

        self.show_loading("Memproses laporan...")
        def cek_ready_submit(dt):
            ready1 = self.pdf_download_complete.get('pdf_card1', False)
            ready2 = not self.pdf_paths.get('pdf_card2') or self.pdf_download_complete.get('pdf_card2', True)
            file1 = self.pdf_paths.get('pdf_card1')
            file2 = self.pdf_paths.get('pdf_card2')
            exists1 = file1 and os.path.exists(file1)
            exists2 = not file2 or os.path.exists(file2)

            if ready1 and ready2 and exists1 and exists2:
                Clock.unschedule(cek_ready_submit)
                threading.Thread(target=self._cek_jalan_dan_kirim,
                                args=(nama_jalan, periode, total_r, total_a, file1, file2),
                                daemon=True).start()
                return False
            return True

        Clock.schedule_interval(cek_ready_submit, 0.5)

    def _cek_jalan_dan_kirim(self, nama_jalan, periode, total_r, total_a, file1, file2):
        try:
            response = requests.post(f"{API_URL}/check_street_fund", data={'nama_jalan': nama_jalan})
            result = response.json()
            if result['status'] == 'pending':
                Clock.schedule_once(lambda dt: self.hide_loading())
                Clock.schedule_once(lambda dt: show_message("Terdapat laporan user dengan jalan serupa. Harap approve dahulu!"))
                return
            Clock.schedule_once(lambda dt: self._kirim_thread(nama_jalan, periode, total_r, total_a, file1, file2))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.hide_loading())
            Clock.schedule_once(lambda dt, err=e: show_message(f"Gagal validasi jalan: {err}"))

    def _kirim_thread(self, nama_jalan, periode, total_r, total_a, file1, file2):
        app = MDApp.get_running_app()
        try:
            data = {
                'nama_jalan': nama_jalan,
                'periode_proyek': periode,
                'total_rancangan': total_r,
                'total_akhir': total_a
            }
            with open(file1, 'rb') as f1:
                filename1 = os.path.basename(file1)
                if file2:
                    with open(file2, 'rb') as f2:
                        filename2 = os.path.basename(file2)
                        files = {
                            'laporan_rancangan': (filename1, f1, 'application/pdf'),
                            'laporan_akhir': (filename2, f2, 'application/pdf')
                        }
                        response = requests.post(f"{API_URL}/submit_fund_report", data=data, files=files)
                else:
                    files = {
                        'laporan_rancangan': (filename1, f1, 'application/pdf')
                    }
                    response = requests.post(f"{API_URL}/submit_fund_report", data=data, files=files)

            result = response.json()
            Clock.schedule_once(lambda dt: self.hide_loading())
            if response.status_code in (200, 201):
                Clock.schedule_once(lambda dt: show_message("Laporan dana berhasil dikirim"))
                Clock.schedule_once(lambda dt: app.change_screen("reports", "rise"))
            else:
                Clock.schedule_once(lambda dt: show_message(result.get("message", "Terjadi kesalahan saat mengirim.")))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.hide_loading())
            Clock.schedule_once(lambda dt, err=e: show_message(f"Gagal mengirim laporan: {err}"))
        
    def open_filechooser(self, pdf_card_id):
        def callback(selection):
            if selection:
                filepath = selection[0]
                self.show_loading("Memuat file PDF...")

                def process_pdf():
                    time.sleep(1)
                    Clock.schedule_once(lambda dt: self.set_pdf_filename(pdf_card_id, filepath))
                    Clock.schedule_once(lambda dt: self.hide_loading())

                threading.Thread(target=process_pdf).start()

        filechooser.open_file(on_selection=callback, filters=["*.pdf"])
    
    def set_pdf_filename(self, pdf_card_id, filepath, from_server=False):
        self.pdf_paths[pdf_card_id] = filepath
        self.pdf_download_complete[pdf_card_id] = not (from_server and filepath.startswith("http"))
        pdf_card = self.ids[pdf_card_id]
        pdf_card.clear_widgets()
        filename = os.path.basename(filepath)
        box = TransparentTouchCard(
            orientation='horizontal',
            padding=[12, 10],
            spacing=10,
            radius=[12],
            size_hint=(1, None),
            height="48dp",
            theme_bg_color="Custom",
            md_bg_color=(0, 0, 0, 0),
            focus_color=(0, 0, 0, 0),
        )
        icon = MDIcon(
            icon="file-pdf-box",
            size_hint=(None, None),
            size=("24dp", "24dp"),
            theme_text_color="Custom",
            text_color="#D32F2F",
            theme_font_size="Custom",
            font_size="26sp",
            pos_hint={'center_y': 0.5}
        )
        label = MDLabel(
            text=filename,
            halign="left",
            valign="middle",
            theme_text_color="Custom",
            text_color=(0.1, 0.2, 0.4, 1),
            theme_font_name="Custom",
            font_name="Poppins-SemiBold",
            theme_font_size="Custom",
            font_size="12sp",
            shorten=True,
            max_lines=1,
            size_hint_x=1,
        )
        box.add_widget(icon)
        box.add_widget(label)
        pdf_card.add_widget(box)
        
        if from_server:
            def download_pdf():
                try:
                    if filepath.startswith("http"):
                        url = filepath
                    else:
                        url = API_URL.rstrip('/') + '/' + filepath.lstrip('/')
                    r = requests.get(url, stream=True, timeout=10)
                    if r.status_code == 200:
                        local_path = os.path.join("temp_pdfs", filename)
                        os.makedirs("temp_pdfs", exist_ok=True)
                        with open(local_path, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                        self.pdf_paths[pdf_card_id] = local_path
                        self.pdf_download_complete[pdf_card_id] = True
                    else:
                        print(f"Download gagal, status code: {r.status_code}")
                        self.pdf_download_complete[pdf_card_id] = False
                except Exception as e:
                    print(f"Gagal memuat PDF: {e}")
                    self.pdf_download_complete[pdf_card_id] = False
                    
            self.pdf_download_complete[pdf_card_id] = False
            threading.Thread(target=download_pdf).start()
        else:
            self.pdf_download_complete[pdf_card_id] = True
        
    def show_date_picker(self, *args):
        picker = MDModalInputDatePicker(
            mode="range",
            text_button_ok="Selesai",
            text_button_cancel="Batal",
            scrim_color=(0.1, 0.2, 0.4, 1),
            date_format="dd/mm/yyyy"
        )
        picker.supporting_text = "Pilih Rentang Bulan & Tahun"
        picker.supporting_input_text = "Periode Proyek"
        picker.bind(
            on_ok=self.date_save,
            on_cancel=lambda *args: picker.dismiss()
        )
        picker.open()

    def date_save(self, picker):
        selected_range = picker.get_date()
        self.format_date_range(selected_range)
        picker.dismiss()

    def format_date_range(self, date_range):
        if date_range and len(date_range) == 2:
            start_date, end_date = date_range
            formatted_start = start_date.strftime("%d/%m/%Y")
            formatted_end = end_date.strftime("%d/%m/%Y")
            formatted = f"{formatted_start} - {formatted_end}"
            self.ids.periode.text = formatted
    pass

class Profil(MDScreen):
    def on_pre_enter(self):
        app = MDApp.get_running_app()
        username = ""
        alamat = ""
        if hasattr(app, "admin_data") and app.admin_data:
            username = app.admin_data.get("username", "")
            alamat = "Admin StreetCare"
        elif hasattr(app, "user_data") and app.user_data:
            username = app.user_data.get("username", "")
            alamat = app.user_data.get("alamat", "")
        if username:  
            self.ids.username.text = username
            threading.Thread(target=self.get_report_summary, args=(username,), daemon=True).start()
        if alamat:
            self.ids.address.text = alamat
        else:
            print("Tidak ada data user/admin yang ditemukan.")
    
    def get_report_summary(self, username):
        try:
            response = requests.post(f"{API_URL}/user/report_summary", json={"username": username}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.ids.pelaporan.text = str(data.get("total", 0))
                    self.ids.progress.text = str(data.get("in_progress", 0))
                    self.ids.done.text = str(data.get("completed", 0))
                else:
                    print("Gagal mengambil data laporan:", data.get("message"))
            else:
                print("Error server:", response.status_code)
        except Exception as e:
            print("Gagal mengambil data laporan:", e)
    
    @mainthread
    def update_labels(self, total, in_progress, completed):
        self.ids.pelaporan.text = str(total)
        self.ids.progress.text = str(in_progress)
        self.ids.done.text = str(completed)
        
    def show_dialog(self):
        layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        layout.add_widget(Label(
            text='Anda akan keluar dan\ndiarahkan ke halaman login.',
            font_size='12.5sp',
            font_name='Poppins-Medium',
            halign='center',
            color=(0.1, 0.2, 0.4, 1),
        ))
        button_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(20))
        button_layout.add_widget(Button(
            text="Batal",
            font_size='13sp',
            font_name='Poppins-Regular',
            background_normal='', 
            background_color=(0.1, 0.2, 0.4, 1),
            color=(1, 1, 1, 1),
            on_release=lambda x: popup.dismiss()
        ))
        button_layout.add_widget(Button(
            text="Konfirm",
            font_size='13sp',
            font_name='Poppins-Regular',
            background_normal='', 
            background_color=(0.1, 0.2, 0.4, 1),
            color=(1, 1, 1, 1),
            on_release=lambda x: (self.logout(), popup.dismiss())
        ))
        layout.add_widget(button_layout)
        popup = Popup(
            title="Konfirmasi Logout?",
            title_font="Poppins-Bold",
            title_align="center",
            title_color=(0.1, 0.2, 0.4, 1),
            title_size=sp(19),
            content=layout,
            size_hint=(None, None),
            size=(dp(300), dp(220)),
            auto_dismiss=False,
            background="",
            background_color=(1, 1, 1, 1),
            separator_color=(0.1, 0.2, 0.4, 1),
        )
        popup.open()
    
    def logout(self):
        app = MDApp.get_running_app()
        user_json = resource_path("data/user_login.json")
        admin_json = resource_path("data/admin_login.json")
        removed = False
        for file in [user_json, admin_json]:
            if os.path.exists(file):
                try:
                    os.remove(file)
                    removed = True
                    print(f"File login {file} berhasil dihapus.")
                except Exception as e:
                    print(f"Gagal menghapus {file}:", e)
        if hasattr(app, "user_data"):
            app.user_data = None
            removed = True
        if hasattr(app, "admin_data"):
            app.admin_data = None
            removed = True
        show_message("Berhasil log out." if removed else "Tidak ada data login tersimpan.")
        app.change_screen("login", "fade")
    pass

class Camera(MDScreen):
    def on_enter(self):
        app = MDApp.get_running_app()
        if app.recorded_video_path:
            self.show_video(app.recorded_video_path)
            app.recorded_video_path = None
            
    def show_video(self, path):
        container = self.ids.camera_container
        self.video = Video(source=path, state='pause')
        self.video.size_hint = (1, 1)
        self.video.radius =[dp(15),]
        self.video.allow_stretch = True
        self.video.keep_ratio = True
        self.video.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        container.add_widget(self.video, index=0)
        play_btn = self.ids.play_btn
        self.video.state = "play"
        play_btn.icon = "pause"
        Animation(opacity=0, d=3).start(play_btn)
        self.video_check_ev = Clock.schedule_interval(self.check_video_end, 0.5)
        
        thumbnail_path = os.path.join(os.getcwd(), "video_thumbnail.jpg")
        self.generate_thumbnail(path, thumbnail_path)
        app = MDApp.get_running_app()
        app.thumbnail_path = thumbnail_path
        self.video_duration_and_store(path)

    def toggle_play(self):
        play_btn = self.ids.play_btn
        if self.video.state == 'play':
            Animation.cancel_all(play_btn)
            self.video.state = 'pause'
            play_btn.icon = "play"
            play_btn.opacity = 1
        else:
            if self.video.position >= self.video.duration:
                self.video.position = 0
            self.video.state = 'play'
            play_btn.icon = "pause"
            anim = Animation(opacity=0, duration=3)
            anim.start(play_btn)
            
        if hasattr(self, "video_check_ev"):
            Clock.unschedule(self.video_check_ev)
        self.video_check_ev = Clock.schedule_interval(self.check_video_end, 0.5)
    
    def check_video_end(self, dt):
        if not self.video:
            return
        try:
            pos = self.video.position
            dur = self.video.duration
            if dur > 0 and pos >= dur-0.1:
                self.on_video_end()
                Clock.unschedule(self.video_check_ev)
        except:
            pass

    def on_video_end(self, *args):
        play_btn = self.ids.play_btn
        if hasattr(self, "video_check_ev"):
            Clock.unschedule(self.video_check_ev)
        if self.video:
            self.video.state = 'stop'
            self.video.position = 0
        if play_btn:
            print(f"Before: icon={play_btn.icon}, opacity={play_btn.opacity}, disabled={play_btn.disabled}")
            Animation.cancel_all(play_btn)
            play_btn.icon = "play"
            play_btn.disabled = False
            Animation(opacity=1, duration=0.1).start(play_btn)
    
    def generate_thumbnail(self, video_path, thumbnail_path):
        cap = cv2.VideoCapture(video_path)
        success, frame = cap.read()
        if success:
            cv2.imwrite(thumbnail_path, frame)
        cap.release()
    
    def video_duration_and_store(self, path):
        try:
            app = MDApp.get_running_app()
            streetreport = app.root.get_screen("streetreport")
            clip = VideoFileClip(path)
            duration_sec = int(clip.duration)
            minutes = duration_sec // 60
            seconds = duration_sec % 60
            duration_label = streetreport.ids.duration
            duration_label.text = f"Durasi: {minutes:02d}:{seconds:02d}"
            app.temp_video_path = path
        except Exception as e:
            print("Gagal membaca durasi video:", e)
    pass

class Streetreport(MDScreen):
    def on_leave(self):
        Clock.schedule_once(lambda dt: self.reset_fields(), 0.1)
    
    def on_enter(self):
        app = MDApp.get_running_app()
        if hasattr(app, "thumbnail_path"):
            thumb_path = app.thumbnail_path
            layout = self.ids.thumbnail
            layout.clear_widgets()
            layout.add_widget(
                FitImage(
                    source=thumb_path,
                    radius=[dp(12)],
                    size_hint=(1, 1),
                    pos_hint={"center_x": 0.5, "center_y": 0.5}
                )
            )
            layout.add_widget(
                MDIcon(
                    icon= "play",
                    theme_icon_color= "Custom",
                    icon_color= (0.1, 0.2, 0.4, 0.65),
                    theme_font_size= "Custom",
                    font_size= "50sp",
                    pos_hint= {"center_x": 0.5, "center_y": 0.5},
                )
            )
        if not hasattr(self, "mapview") or self.mapview is None:
            self.mapview = StreetReportMapView()
        container = self.ids.map_container
        container.clear_widgets()
        if self.mapview.parent:
            self.mapview.parent.remove_widget(self.mapview)
        container.add_widget(self.mapview)
        lat = app.gps_location.get('lat', -7.1609)
        lon = app.gps_location.get('lon', 112.6511)
        self.marker_lat = lat
        self.marker_lon = lon
        if (GRESIK_BOUNDS["min_lat"] <= lat <= GRESIK_BOUNDS["max_lat"] and
            GRESIK_BOUNDS["min_lon"] <= lon <= GRESIK_BOUNDS["max_lon"]):
            if self.mapview.current_marker:
                self.mapview.remove_marker(self.mapview.current_marker)
            self.mapview.current_marker = MapMarker(
                lat=lat, lon=lon, source="assets/user_marker.png"
            )
            self.mapview.add_marker(self.mapview.current_marker)
            self.mapview.center_on(lat, lon)
        self.mapview.on_marker_moved = self.on_marker_moved

    def on_marker_moved(self, lat, lon):
        print(f"Marker dipindahkan ke: {lat}, {lon}")
        self.marker_lat = lat
        self.marker_lon = lon
    
    def recenter_map(self):
        app = MDApp.get_running_app()
        lat = app.gps_location.get('lat', -7.1609)
        lon = app.gps_location.get('lon', 112.6511)
        if (GRESIK_BOUNDS["min_lat"] <= lat <= GRESIK_BOUNDS["max_lat"] and
            GRESIK_BOUNDS["min_lon"] <= lon <= GRESIK_BOUNDS["max_lon"]):
            if self.mapview.current_marker:
                self.mapview.remove_marker(self.mapview.current_marker)
            self.mapview.current_marker = MapMarker(
                lat=lat, lon=lon, source="assets/user_marker.png"
            )
            self.mapview.add_marker(self.mapview.current_marker)
            self.mapview.center_on(lat, lon)
        else:
            show_message("Lokasi Anda di luar wilayah Gresik.")
            
    def update_text(self, textfield, is_focused, default_text):
        if is_focused:  
            if textfield.text == default_text:
                textfield.text = ""
        else:
            if textfield.text.strip() == "":
                textfield.text = default_text
    
    def message(self):
        yes = self.ids.yes_check
        no = self.ids.no_check
        if not yes.active and not no.active:
            show_message("Pilih terlebih dahulu.")
            return False
        elif not yes.active:
            show_message("Anda memilih 'belum pernah'")
            return False
        return True

    def no_check(self, checkbox, value):
        if value:
            self.ids.yes_check.active = False
            self.ids.intensity.text = "--"

    def compress_video(self, input_path, output_path):
        try:
            original_size_mb = os.path.getsize(input_path) / (1024 * 1024)
            print(f"Ukuran video asli: {original_size_mb:.2f} MB")
            if original_size_mb <= 5:
                shutil.copyfile(input_path, output_path)
                print("Video tidak perlu dikompresi.")
                return True
            clip = VideoFileClip(input_path)
            clip.write_videofile(output_path, bitrate="500k", audio_codec='aac')
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"Ukuran video terkompresi: {size_mb:.2f} MB")
            return size_mb <= 5
        except Exception as e:
            print("Gagal mengompres video:", e)
            return False
    
    def show_loading(self, message="Sedang memproses..."):
        if hasattr(self, "loading_dialog") and self.loading_dialog:
            return
        content = MDBoxLayout(orientation="vertical", spacing=10, padding=20)
        content.add_widget(MDCircularProgressIndicator(size_hint=(None, None), size=("33dp", "33dp")))
        content.add_widget(MDLabel(text=message, halign="center", theme_font_name="Custom", font_name="Poppins-SemiBold", theme_font_size="Custom", font_size="14dp"))
        self.loading_dialog = MDDialog(
            MDDialogHeadlineText(
                text="Mohon Tunggu",
                halign="center",
                theme_font_name="Custom", 
                font_name="Poppins-Bold",
                theme_font_size="Custom",
                font_size="12dp"
            ),
            MDDialogContentContainer(
                content
            ),
            auto_dismiss=False,
            size_hint_x=.925
        )
        self.loading_dialog.open()

    def hide_loading(self):
        if hasattr(self, "loading_dialog") and self.loading_dialog:
            self.loading_dialog.dismiss()
            self.loading_dialog = None
    
    def submit(self):
        self.show_loading("Sedang memproses...")
        threading.Thread(target=self.submit_thread, daemon=True).start()
    
    def submit_thread(self):
        app = MDApp.get_running_app()
        username = app.user_data.get("username") if hasattr(app, "user_data") else None
        jalan = self.ids.location.text.strip()
        lat = self.marker_lat
        lon = self.marker_lon
        pernah = self.ids.yes_check.active
        tidak_pernah = self.ids.no_check.active
        intensitas = self.ids.intensity.text.strip()
        komentar = self.ids.comment.text.strip()
        video_path = getattr(app, "temp_video_path", None)
        
        def show_and_hide(msg):
            Clock.schedule_once(lambda dt: show_message(msg), 0)
            Clock.schedule_once(lambda dt: self.hide_loading(), 0)
            
        if not username:
            show_and_hide("Error: Data login tidak ditemukan.")
            return
        if not jalan or jalan =="Ketikkan di sini...":
            show_and_hide("Isikan alamat jalan terlebih dulu!")
            return
        if lat is None or lon is None:
            show_and_hide("Pilih lokasi di map!")
            return
        if not pernah and not tidak_pernah:
            show_and_hide("Pilih keterangan kecelakaan!")
            return
        if pernah:
            if intensitas == "--":
                show_and_hide("Isikan intensitas!")
                return
            try:
                intensitas_val = int(intensitas)
            except ValueError:
                show_and_hide("Intensitas hanya menerima angka!")
                return
        else:
            intensitas_val = ""

        video_file = None
        if video_path and os.path.exists(video_path):
            compressed_path = os.path.join("compressed", "compressed_video.mp4")
            os.makedirs("compressed", exist_ok=True)
            success = self.compress_video(video_path, compressed_path)
            if not success:
                show_and_hide("Ukuran video terlalu besar.")
                return
            video_file = open(compressed_path, 'rb')
        form_data = {
            "username": username,
            "jalan": jalan,
            "lat": str(lat),
            "lon": str(lon),
            "pernah": str(pernah).lower(),
            "intensitas": str(intensitas_val),
            "komentar": komentar,
        }
        files = {"video": video_file} if video_file else None
        try:
            response = requests.post(f"{API_URL}/submit_report", data=form_data, files=files)
            if video_file:
                video_file.close()
            if response.status_code == 201:
                Clock.schedule_once(lambda dt: show_message("Laporan berhasil dikirim!"), 0)
                Clock.schedule_once(lambda dt: MDApp.get_running_app().go_back(), 0)
            else:
                data = response.json()
                Clock.schedule_once(lambda dt: show_message(f"Gagal mengirim: {data.get('message', 'Error')}"), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: show_message(f"Error koneksi: {str(e)}"), 0)
        finally:
            Clock.schedule_once(lambda dt: self.hide_loading(), 0)
    
    def reset_fields(self):
        self.ids.location.text = "Ketikkan di sini..."
        self.ids.yes_check.active = False
        self.ids.no_check.active = False
        self.ids.intensity.text = "--"
        self.ids.comment.text = "Ketikkan di sini..."
        self.marker_lat = None
        self.marker_lon = None
    pass

class Recap(MDScreen):
    def on_enter(self, *args):
        self.all_reports = []
        self.load_report()
        if not MDApp.get_running_app().admin_data:
            self.ids.admin_status.opacity = 0
            self.ids.admin_status.disabled = True
        else:
            self.ids.admin_status.opacity = 1
            self.ids.admin_status.disabled = False

    def on_leave(self):
        Clock.schedule_once(lambda dt: self.reset_fields(), 0.1)
        app = MDApp.get_running_app()
        app.recap_sort = ""
    
    def show_loading(self, message="Sedang memproses..."):
        if hasattr(self, "loading_dialog") and self.loading_dialog:
            return
        content = MDBoxLayout(orientation="vertical", spacing=10, padding=20)
        content.add_widget(MDCircularProgressIndicator(size_hint=(None, None), size=("33dp", "33dp")))
        content.add_widget(MDLabel(text=message, halign="center", theme_font_name="Custom", font_name="Poppins-SemiBold", theme_font_size="Custom", font_size="14dp"))
        self.loading_dialog = MDDialog(
            MDDialogHeadlineText(
                text="Mohon Tunggu",
                halign="center",
                theme_font_name="Custom", 
                font_name="Poppins-Bold",
                theme_font_size="Custom",
                font_size="12dp"
            ),
            MDDialogContentContainer(
                content
            ),
            auto_dismiss=False,
            size_hint_x=.925
        )
        self.loading_dialog.open()

    def hide_loading(self):
        if hasattr(self, "loading_dialog") and self.loading_dialog:
            self.loading_dialog.dismiss()
            self.loading_dialog = None

    def load_report(self):
        self.ids.report_list.clear_widgets()
        self.show_loading("Sedang memuat...")
        threading.Thread(target=self.load_report_thread, daemon=True).start()

    def load_report_thread(self):
        try:
            response = requests.get(f"{API_URL}/all_clusters")
            data = response.json()
            if data.get("success"):
                markers = data["clusters"]
                self.all_reports = markers

                def add_widgets(dt):
                    self.display_reports(self.all_reports)

                Clock.schedule_once(add_widgets, 0)
                Clock.schedule_once(lambda dt: self.hide_loading(), 0)
            else:
                Clock.schedule_once(lambda dt: show_message("Gagal mengambil data dari server!"), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt, err=e: show_message(f"Error koneksi: {str(err)}"), 0)
    
    def display_reports(self, data):
        self.ids.report_list.clear_widgets()
        for m in data:
            item = ReportItem(
                nama_jalan=m["nama_jalan"],
                jumlah_laporan=m["jumlah_laporan"],
                status=m["status"],
                jumlah_kecelakaan=m["jumlah_kecelakaan"]
            )
            self.ids.report_list.add_widget(item)
        if not hasattr(self, 'original_children') or not self.original_children:
            self.original_children = list(self.ids.report_list.children)
            
    def sort_report_list(self):             
        app = MDApp.get_running_app()
        children = list(self.ids.report_list.children)
        self.ids.report_list.clear_widgets()
        status_order = {
            "pending": 0,
            "approved": 1,
            "dalam_perbaikan": 2,
            "selesai": 3
        }
        mode = app.recap_sort
        if not mode:
            sorted_children = getattr(self, 'original_children', children)
        else:
            def sort_key(item):
                keys = []
                if mode in ("status_asc", "status_desc"):
                    keys.append(status_order.get(item.status.lower(), 4))
                elif mode == "kecelakaan":
                    try:
                        keys.append(int(item.jumlah_kecelakaan))
                    except:
                        keys.append(0)
                elif mode == "pelaporan":
                    try:
                        keys.append(int(item.jumlah_laporan))
                    except:
                        keys.append(0)
                return tuple(keys)
            reverse_sort = mode in ("status_desc", "kecelakaan", "pelaporan")
            children.sort(key=sort_key, reverse=reverse_sort)
            sorted_children = children
        for child in sorted_children:
            self.ids.report_list.add_widget(child)
        
    def search_reports(self, keyword):
        keyword = keyword.strip().lower()
        if not keyword:
            self.display_reports(self.all_reports)
            return
        filtered = [m for m in self.all_reports if keyword in m["nama_jalan"].lower()]
        if not filtered:
            self.ids.report_list.clear_widgets()
            self.ids.report_list.add_widget(MDLabel(
                text="Tidak ada data jalan yang cocok.",
                halign="center",
                theme_font_name="Custom",
                font_name="Poppins-SemiBold",
                theme_font_size="Custom",
                font_size="13sp",
                theme_text_color="Custom",
                text_color=(0.3, 0.3, 0.3, 1),
                size_hint_y=None,
                height=dp(40)
            ))
        else:
            self.display_reports(filtered)
        
    def update_text(self, is_focused):
        default_text = "Cari laporan jalan..."
        textfield = self.ids.search_field
        if is_focused:
            if textfield.text == default_text:
                textfield.text = ""
        else:
            if textfield.text.strip() == "":
                textfield.text = default_text
                self.display_reports(self.all_reports)   
    
    def reset_fields(self):
        self.ids.search_field.text = "Cari laporan jalan..."  
    pass

class Adminstat(MDScreen):
    def on_enter(self, *args):
        self.all_reports = []
        self.load_report()

    def on_leave(self):
        Clock.schedule_once(lambda dt: self.reset_fields(), 0.1)
        app = MDApp.get_running_app()
        app.admin_sort = ""

    def show_loading(self, message="Sedang memproses..."):
        if hasattr(self, "loading_dialog") and self.loading_dialog:
            return
        content = MDBoxLayout(orientation="vertical", spacing=10, padding=20)
        content.add_widget(MDCircularProgressIndicator(size_hint=(None, None), size=("33dp", "33dp")))
        content.add_widget(MDLabel(text=message, halign="center", theme_font_name="Custom", font_name="Poppins-SemiBold", theme_font_size="Custom", font_size="14dp"))
        self.loading_dialog = MDDialog(
            MDDialogHeadlineText(
                text="Mohon Tunggu",
                halign="center",
                theme_font_name="Custom", 
                font_name="Poppins-Bold",
                theme_font_size="Custom",
                font_size="12dp"
            ),
            MDDialogContentContainer(
                content
            ),
            auto_dismiss=False,
            size_hint_x=.925
        )
        self.loading_dialog.open()

    def hide_loading(self):
        if hasattr(self, "loading_dialog") and self.loading_dialog:
            self.loading_dialog.dismiss()
            self.loading_dialog = None

    def load_report(self):
        self.ids.report_list.clear_widgets()
        self.show_loading("Sedang memuat...")
        threading.Thread(target=self.load_report_thread, daemon=True).start()

    def load_report_thread(self):
        try:
            response = requests.get(f"{API_URL}/all_clusters")
            data = response.json()
            if data.get("success"):
                self.all_reports = data["clusters"]
                Clock.schedule_once(lambda dt: self.display_reports(self.all_reports))
                Clock.schedule_once(lambda dt: self.hide_loading(), 0)
            else:
                Clock.schedule_once(lambda dt: show_message("Gagal mengambil data dari server!"), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt, err=e: show_message(f"Error koneksi: {str(err)}"), 0)

    def display_reports(self, data):
        self.ids.report_list.clear_widgets()
        for m in data:
            item = EditableReportItem(
                cluster_id=m["cluster_id"],
                nama_jalan=m["nama_jalan"],
                jumlah_laporan=m["jumlah_laporan"],
                status=m["status"],
                jumlah_kecelakaan=m["jumlah_kecelakaan"]
            )
            self.ids.report_list.add_widget(item)
        self.original_children = list(self.ids.report_list.children)

    def sort_report_list(self):
        app = MDApp.get_running_app()
        children = list(self.ids.report_list.children)
        self.ids.report_list.clear_widgets()
        status_order = {
            "pending": 0,
            "approved": 1,
            "dalam_perbaikan": 2,
            "selesai": 3
        }
        mode = app.admin_sort
        if not mode:
            sorted_children = getattr(self, 'original_children', children)
        else:
            def sort_key(item):
                keys = []
                if mode in ("status_asc", "status_desc"):
                    keys.append(status_order.get(item.status.lower(), 4))
                elif mode == "kecelakaan":
                    try:
                        keys.append(int(item.jumlah_kecelakaan))
                    except:
                        keys.append(0)
                elif mode == "pelaporan":
                    try:
                        keys.append(int(item.jumlah_laporan))
                    except:
                        keys.append(0)
                return tuple(keys)
            reverse_sort = mode in ("status_desc", "kecelakaan", "pelaporan")
            children.sort(key=sort_key, reverse=reverse_sort)
            sorted_children = children
        for child in sorted_children:
            self.ids.report_list.add_widget(child)

    def search_reports(self, keyword):
        keyword = keyword.strip().lower()
        if not keyword:
            self.display_reports(self.all_reports)
            return
        filtered = [m for m in self.all_reports if keyword in m["nama_jalan"].lower()]
        if not filtered:
            self.ids.report_list.clear_widgets()
            self.ids.report_list.add_widget(MDLabel(
                text="Tidak ada data jalan yang cocok.",
                halign="center",
                size_hint_y=None,
                height=dp(40)
            ))
        else:
            self.display_reports(filtered)

    def update_text(self, is_focused):
        default_text = "Cari laporan jalan..."
        textfield = self.ids.search_field
        if is_focused:
            if textfield.text == default_text:
                textfield.text = ""
        else:
            if textfield.text.strip() == "":
                textfield.text = default_text
                self.display_reports(self.all_reports)

    def reset_fields(self):
        self.ids.search_field.text = "Cari laporan jalan..."
    
    def show_status_dialog(self, item):
        def set_status(status):
            self.update_status_to_api(item.cluster_id, status)
            menu.dismiss()
    
        status_options = [
            ("Pending", "pending"),
            ("Approved", "approved"),
            ("Dalam Perbaikan", "dalam_perbaikan"),
            ("Selesai", "selesai"),
        ]
        menu_items = []
        for i, (label, status_value) in enumerate(status_options):
            menu_items.append({
                "viewclass": "MDLabel",
                "markup": True,
                "text": f"[ref={status_value}]{label}[/ref]",
                "on_ref_press": lambda x, ref=status_value: set_status(ref),
                "theme_text_color": "Custom",
                "text_color": (0.1, 0.2, 0.4, 1),
                "font_name": "Poppins-SemiBold",
                "halign": "left",
                "padding": dp(16.5),
                "theme_font_size": "Custom",
                "font_size": sp(14),
                "size_hint_x": None,
                "adaptive_size": True,
                "shorten": True,
                "size_hint_y": None,
                "height": dp(52),
            })
            if i < len(status_options) - 1:
                menu_items.append({
                    "viewclass": "MDDivider",
                    "height": dp(1),
                })
        menu = MDDropdownMenu(
            caller=item,
            items=menu_items,
            width_mult=1,
            position="center",
        )
        menu.open()

    def update_status_to_api(self, cluster_id, new_status):
        self.show_loading("Memperbarui status...")
        def task():
            try:
                res = requests.post(f"{API_URL}/update_status", json={
                    "cluster_id": cluster_id,
                    "status": new_status
                })
                if res.status_code == 200:
                    Clock.schedule_once(lambda dt: show_message("Status berhasil diperbarui."))
                    Clock.schedule_once(lambda dt: self.load_report())
                else:
                    Clock.schedule_once(lambda dt: show_message("Gagal memperbarui status."))
            except Exception as e:
                Clock.schedule_once(lambda dt, err=e: show_message(f"Error update: {err}"))
            Clock.schedule_once(lambda dt: self.hide_loading())
        threading.Thread(target=task, daemon=True).start() 
    pass

KV_FILES = [
    "splash.kv", "welcome.kv", "login.kv", "adminlog.kv", "forgot.kv", "forgot2.kv", "signup.kv",
    "signup2.kv", "home.kv", "maps.kv", "reports.kv", "profil.kv", "camera.kv", "streetreport.kv",
    "recap.kv", "adminstat.kv", "adminreport.kv"
]
class StreetCare(MDApp):
    current_screen = StringProperty()
    screen_stack = []
    excluded_screens = ["splash", "camera", "signup2", "recap", "adminstat", "adminreport"]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.recorded_video_path = None
        self.admin_data = None
        self.user_data = None
        self.recap_sort = ""
        self.admin_sort = ""
        
    def build(self):
        self.title = "StreetCare"
        self.icon = resource_path("assets/icon.png")
        self.mapview = GresikMapView()
        self.mapview.size_hint = (1, 1)
        self.mapview.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.user_marker = None
        self.gps_location = None
        self.start_gps()
        self.mapview.bind(lat=self.on_map_moved, lon=self.on_map_moved)
        self.open_video_capture = open_video_capture
        self.resource_path = resource_path
        
        screen_manager = MDScreenManager()
        for kv in KV_FILES:
            Builder.load_file(resource_path(kv))
            screen_name = kv.split(".")[0].capitalize()
            screen_class = globals()[screen_name]
            screen_manager.add_widget(screen_class(name=screen_name.lower()))
        return screen_manager
    
    def change_screen(self, screen_name, transition):
        if self.root.current not in self.excluded_screens and self.root.current != screen_name:
            self.screen_stack.append(self.root.current)
        if transition == "wipe":
            self.root.transition = WipeTransition()
        elif transition == "fade":
            self.root.transition = FadeTransition()
        elif transition == "fast":
            self.root.transition = FadeTransition(duration=0.01)
        elif transition == "slide":
            self.root.transition = SlideTransition(direction="right")
        elif transition == "rise":
            self.root.transition = RiseInTransition(duration=0.15)
        else:
            self.root.transition = MDSharedAxisTransition(transition_axis="z", duration=0.5)
        self.root.current = screen_name
        self.current_screen = screen_name
    
    def go_back(self):
        if self.screen_stack:
            previous_screen = self.screen_stack.pop()
            self.change_screen(previous_screen, "fade")
    
    def check_admin_json(self):
        admin_json_path = resource_path("data/admin_login.json")
        if os.path.exists(admin_json_path):
            try:
                with open(admin_json_path, "r", encoding="utf-8") as f:
                    admin_data = json.load(f)
                timestamp = admin_data.get("login_timestamp")
                if timestamp and time.time() - timestamp < 86400:
                    return admin_data
                else:
                    os.remove(admin_json_path)
            except Exception as e:
                print("Gagal membaca admin_login.json:", e)
        return None
    
    def transition_to_map(self):
        sm = self.root
        home = sm.get_screen("home")
        self.map_container = home.ids.map_container
        self.original_parent = self.map_container.parent
        self.original_index = self.original_parent.children.index(self.map_container)

        start_pos = self.map_container.to_window(*self.map_container.pos)
        start_size = self.map_container.to_window(self.map_container.right, self.map_container.top)
        start_size = (start_size[0] - start_pos[0], start_size[1] - start_pos[1])
        
        snapshot = self.map_container.export_as_image()
        texture = snapshot.texture
        texture.flip_vertical()
        self.anim_widget = Image(
            texture=texture,
            size=start_size,
            size_hint=(None, None),
            pos=start_pos,
            allow_stretch=True,
            keep_ratio=True,
        )
        Window.add_widget(self.anim_widget)
        anim = Animation(pos=(0, 0), size=Window.size, duration=0.3, t='out_quad')
        anim.bind(on_complete=self.fade_out)
        anim.start(self.anim_widget)
        self.map_container.opacity = 0

    def fade_out(self, *args):
        anim = Animation(opacity=0, duration=0.5)
        self.change_screen("maps", "fade")
        anim.bind(on_complete=self.on_complete)
        anim.start(self.anim_widget)

    def on_complete(self, *args):
        if self.anim_widget.parent:
            self.anim_widget.parent.remove_widget(self.anim_widget)
        self.restore_map_container()

    def restore_map_container(self):
        if not self.map_container.parent:
            self.original_parent.add_widget(self.map_container, index=self.original_index)
        self.map_container.size_hint = (1, 1)
        self.map_container.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.map_container.opacity = 1
    
    def start_gps(self):
        if platform == "android":
            try:
                gps.configure(on_location=self.update_gps_location, on_status=self.on_gps_status)
                gps.start(minTime=1000, minDistance=1)
            except NotImplementedError:
                print("GPS is not implemented on this platform")
        else:
            self.gps_location = {"lat": -7.1609, "lon": 112.6511}

            self.set_user_marker()

    def update_gps_location(self, **kwargs):
        self.gps_location = {"lat": kwargs['lat'], "lon": kwargs['lon']}
        self.set_user_marker()

    def on_gps_status(self, status_type, status_msg):
        print("GPS Status:", status_type, status_msg)

    def set_user_marker(self):
        if not self.gps_location:
            return
        lat = self.gps_location['lat']
        lon = self.gps_location['lon']
        if self.user_marker:
            self.mapview.remove_marker(self.user_marker)
        self.user_marker = MapMarker(
            lat=lat,
            lon=lon,
            source=resource_path("assets/user_marker.png")
        )
        self.mapview.add_marker(self.user_marker)
        self.mapview.center_on(lat, lon)
        self.mapview.user_marker = self.user_marker

    def on_map_moved(self, *args):
        self.update_gps_icon()

    def update_gps_icon(self):
        map_center_lat = self.mapview.lat
        map_center_lon = self.mapview.lon
        user_lat = self.user_marker.lat
        user_lon = self.user_marker.lon
        threshold = 0.00005
        if self.root.current == "home":
            home_screen = self.root.get_screen("home")
            gps_btn = home_screen.ids.gps_btn
            if (abs(map_center_lat - user_lat) < threshold and abs(map_center_lon - user_lon) < threshold):
                gps_btn.icon = "crosshairs-gps"
            else:
                gps_btn.icon = "crosshairs"
        elif self.root.current == "maps":
            maps_screen = self.root.get_screen("maps")
            gps_btn = maps_screen.ids.gps_btn
            if (abs(map_center_lat - user_lat) < threshold and abs(map_center_lon - user_lon) < threshold):
                gps_btn.icon = "crosshairs-gps"
            else:
                gps_btn.icon = "crosshairs"

    def recenter_map(self, *args):
        if hasattr(self, 'gps_location') and self.gps_location:
            lat = self.gps_location.get("lat")
            lon = self.gps_location.get("lon")
            if lat is not None and lon is not None:
                self.mapview.center_on(lat, lon)
                self.mapview.zoom = self.mapview.zoom_default
            self.update_gps_icon()
    
    def toggle_filter(self, key, active):
        current_screen = self.root.current
        if active:
            if current_screen == "recap":
                self.recap_sort = key
            elif current_screen == "adminstat":
                self.admin_sort = key

    def apply_drawer_sort(self):
        current_screen = self.root.current
        if current_screen == "recap":
            screen = self.root.get_screen("recap")
            screen.sort_report_list()
        elif current_screen == "adminstat":
            screen = self.root.get_screen("adminstat")
            screen.sort_report_list()
    
if __name__ == "__main__":
    StreetCare().run()