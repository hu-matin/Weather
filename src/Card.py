import threading
import customtkinter as ctk
from io import BytesIO
from PIL import Image
import requests


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class WeatherCardApp(ctk.CTk):
    def __init__(self, weather_obj):
        super().__init__()

        self.weather_obj = weather_obj
        self.weather_data = None

        self.title("Weather App")
        self.iconbitmap('assets/icon.ico')
        self.minsize(380, 600)
        self.maxsize(380, 600)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        top_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=25)
        top_frame.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="ew")
        top_frame.grid_columnconfigure(0, weight=1)
        top_frame.grid_columnconfigure(1, weight=0)

        self.city_entry = ctk.CTkEntry(
            master=top_frame,
            placeholder_text="Enter city name: ",
            border_width=1,
            placeholder_text_color='gray',
            border_color= 'white',
            fg_color='black',
        )
        self.city_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.submit_button = ctk.CTkButton(
            master=top_frame,
            text="Submit",
            fg_color= 'black',
            text_color='white',
            border_color='white',
            border_width= 1,
            hover_color= 'gray',
            command=self.on_submit_clicked,
        )
        self.submit_button.grid(row=0, column=1)

        if hasattr(self.weather_obj, "city"):
            self.city_entry.insert(0, str(self.weather_obj.city))

        status_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=25)
        status_frame.grid(row=1, column=0, padx=20, pady=(0, 5), sticky="ew")
        status_frame.grid_columnconfigure(0, weight=1)
        status_frame.grid_columnconfigure(1, weight=1)
        status_frame.grid_columnconfigure(2, weight=1)

        self.status_label = ctk.CTkLabel(
            master=status_frame,
            text="",
            text_color="#ff0000",
            font=ctk.CTkFont(size=12),
        )
        self.status_label.grid(row=0, column=0, sticky="w")

        self.loading_label = ctk.CTkLabel(
            master=status_frame,
            text="",
            text_color="#4dff00",
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=25,
        )
        self.loading_label.grid(row=0, column=1, sticky="nsew")

        self._loading = False
        self._loading_dots = 0

        self.card_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=25)
        self.card_frame.grid(row=2, column=0, padx=40, pady=10, sticky="nsew")

        self.card_frame.grid_rowconfigure(0, weight=1)
        self.card_frame.grid_columnconfigure(0, weight=1)

        self.card = ctk.CTkFrame(
            self.card_frame,
            corner_radius=25,
            fg_color="#000000",
        )
        self.card.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.card.grid_rowconfigure(0, weight=2)
        self.card.grid_rowconfigure(1, weight=1)
        self.card.grid_rowconfigure(2, weight=1)
        self.card.grid_rowconfigure(3, weight=1)
        self.card.grid_rowconfigure(4, weight=1)
        self.card.grid_columnconfigure(0, weight=1)

        self.image_frame = ctk.CTkFrame(
            master=self.card,
            fg_color="transparent",
            corner_radius=0,
        )
        self.image_frame.grid(row=0, column=0, sticky="nsew", pady=(25, 10))
        self.image_frame.grid_columnconfigure(0, weight=1)
        self.image_frame.grid_rowconfigure(0, weight=1)

        self.image_label = ctk.CTkLabel(
            self.image_frame,
            text="",
            fg_color="transparent",
        )
        self.image_label.grid(column=0, row=0, sticky="nsew")

        self.temperature_label = ctk.CTkLabel(
            master=self.card,
            text="--",
            font=ctk.CTkFont(size=52, weight="bold"),
            text_color="#FFFFFF",
        )
        self.temperature_label.grid(row=1, column=0, sticky="n")

        self.feels_like_label = ctk.CTkLabel(
            master=self.card,
            text="Feels like: --",
            font=ctk.CTkFont(size=16),
            text_color="#ffffff",
        )
        self.feels_like_label.grid(row=2, column=0, sticky="n")

        self.desc_label = ctk.CTkLabel(
            master=self.card,
            text="--",
            font=ctk.CTkFont(size=20),
            text_color="#ffffff",
        )
        self.desc_label.grid(row=3, column=0, sticky="n", pady=(0, 10))



        self.location_label = ctk.CTkLabel(
            master=self.card,
            text="City, Country",
            font=ctk.CTkFont(size=16),
            text_color="#ffffff",
        )
        self.location_label.grid(row=4, column=0, sticky="n", pady=(0, 20))

        self.start_loading()
        t = threading.Thread(target=self.fetch_weather_thread_initial, daemon=True)
        t.start()

    def start_loading(self):
        self._loading = True
        self._loading_dots = 0
        self.animate_loading()

    def stop_loading(self):
        self._loading = False
        self.loading_label.configure(text="")

    def animate_loading(self):
        if not self._loading:
            return
        dots = "." * (self._loading_dots % 4)
        self.loading_label.configure(text=f"Loading{dots}")
        self._loading_dots += 1
        self.after(300, self.animate_loading)

    def _get_icon_image(self, icon_code: str | None):
        if not icon_code:
            return None
        try:
            url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            img_data = resp.content
            img = Image.open(BytesIO(img_data))
            return ctk.CTkImage(img, size=(150, 150))
        except Exception:
            return None

    def update_card(self, weather: dict):
        city = weather.get("city", "")
        country = weather.get("country", "")
        temp = weather.get("temp", 0.0)
        feels_like = weather.get("feels_like", 0.0)
        icon = weather.get("icon", None)
        description = weather.get("main", "")

        icon_img = self._get_icon_image(icon)
        if icon_img:
            self.image_label.configure(image=icon_img)
            self.image_label.image = icon_img

        self.temperature_label.configure(text=f"{temp:.1f}°")
        self.feels_like_label.configure(text=f"Feels like: {feels_like:.1f}°")
        self.desc_label.configure(
            text=description,
            text_color={
                "Clouds": "#ebebe2",
                "Clear": "#69e6ff",
                "Rain": "#4492c2",
                "Sunny": '#fff200',
            }.get(description, "gray"),
        )
        self.location_label.configure(text=f"{city}, {country}")

    def fetch_weather_thread_initial(self):
        data = self.weather_obj.get()
        self.after(0, self.on_weather_result, data)

    def on_submit_clicked(self):
        city = self.city_entry.get().strip()

        if not city:
            self.status_label.configure(text="City name cannot be empty.")
            return
        if len(city) < 2:
            self.status_label.configure(text="City name is too short.")
            return
        if city.isdigit():
            self.status_label.configure(text="City name cannot be only numbers.")
            return

        self.status_label.configure(text="")
        self.start_loading()

        def worker():
            self.weather_obj.city = city
            data = self.weather_obj.get()
            self.after(0, self.on_weather_result, data)

        t = threading.Thread(target=worker, daemon=True)
        t.start()

    def on_weather_result(self, data: dict | None):
        self.stop_loading()
        if data is None:
            self.status_label.configure(
                text="Could not fetch weather data. Check city or network."
            )
            return

        self.status_label.configure(text="")
        self.weather_data = data
        self.update_card(data)

