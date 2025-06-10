"""
Projekt: Neo Tamagotchi
Prosty program typu Tamagotchi napisany w Pythonie.
Użytkownik wybiera zwierzaka, nadaje mu imię i dba o jego energię i nastrój.
"""

import customtkinter as ctk
from PIL import Image, ImageTk
import os


class PixelPetGame:
    """
    Klasa główna gry Neo Tamagotchi.
    Odpowiada za interfejs, logikę gry i obsługę cyklu życia zwierzaka.
    """

    PET_IMAGE_SIZE = (160, 160)  # stały rozmiar obrazków zwierzaków

    def __init__(self):
        """Inicjalizacja okna gry i podstawowych elementów."""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.root = ctk.CTk()
        self.root.title("Neo Tamagotchi")
        self.root.geometry("1100x800")
        self.root.minsize(1100, 800)

        self.pixel_font = ("Courier", 14)
        self.title_font = ("Courier", 20, "bold")
        self.sidebar_title_font = ("Courier", 18, "bold")
        self.button_font = ("Courier", 16)

        self.colors = {
            "bg_dark": "#0a0a0a",
            "bg_medium": "#1a1a1a",
            "accent": "#b434eb",
            "accent_dark": "#7a1ca7",
            "text": "#ffffff",
            "text_dim": "#a0a0a0",
            "neon_glow": "#d896ff",
            "danger": "#ff2e6d"
        }

        self.root.configure(fg_color=self.colors["bg_dark"])

        self.load_pet_images()
        self.reset_game_state()
        self.create_pet_selection_screen()

    def load_pet_images(self):
        """Ładuje obrazki zwierzaków z folderu assets."""
        self.pet_images = {}
        folder = "assets"
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Utworzono folder: {folder}")

        for pet in ["Dog", "Cat", "Rabbit", "Turtle"]:
            path = os.path.join(folder, f"{pet.lower()}.png")
            if os.path.exists(path):
                try:
                    img = Image.open(path)
                    img = img.resize(self.PET_IMAGE_SIZE, Image.Resampling.LANCZOS)
                    self.pet_images[pet] = ImageTk.PhotoImage(img)
                    print(f"Wczytano obrazek dla: {pet}")
                except Exception as e:
                    print(f"Błąd przy ładowaniu {pet}: {e}")
                    self.pet_images[pet] = None
            else:
                print(f"Brak obrazka: {path}")
                self.pet_images[pet] = None

    def reset_game_state(self):
        """Resetuje stan gry (nowa gra / po śmierci zwierzaka)."""
        self.selected_pet = None
        self.pet_type = ""
        self.running = False

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_frame()

    def create_sidebar(self):
        """Tworzy boczny panel z tytułem i paskami statusu."""
        self.sidebar = ctk.CTkFrame(
            self.root,
            width=250,
            corner_radius=0,
            fg_color=self.colors["bg_medium"],
            border_width=1,
            border_color=self.colors["accent"]
        )
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)
        self.sidebar.grid_propagate(False)

        title_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(30, 20))
        title_frame.grid_columnconfigure(0, weight=1)

        neo_label = ctk.CTkLabel(
            title_frame,
            text="NEO",
            font=self.sidebar_title_font,
            text_color=self.colors["accent"]
        )
        neo_label.grid(row=0, column=0, pady=(0, 5))

        tamagotchi_label = ctk.CTkLabel(
            title_frame,
            text="TAMAGOTCHI",
            font=self.sidebar_title_font,
            text_color=self.colors["accent"]
        )
        tamagotchi_label.grid(row=1, column=0)

        self.stats_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.stats_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        self.stats_frame.grid_columnconfigure(0, weight=1)

    def create_main_frame(self):
        """Tworzy główną ramkę na ekranie."""
        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.colors["bg_dark"])
        self.main_frame.grid(row=0, column=1, rowspan=4, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

    def create_pet_selection_screen(self):
        """Tworzy ekran wyboru zwierzaka i wpisania imienia."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        selection_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        selection_container.place(relx=0.5, rely=0.5, anchor="center")

        title = ctk.CTkLabel(
            selection_container,
            text="SELECT YOUR PET",
            font=self.title_font,
            text_color=self.colors["accent"]
        )
        title.pack(pady=(0, 40))

        button_frame = ctk.CTkFrame(selection_container, fg_color="transparent")
        button_frame.pack(pady=30)

        pets = ["Dog", "Cat", "Rabbit", "Turtle"]
        for i, pet in enumerate(pets):
            row = i // 2
            col = i % 2

            button_frame_outer = ctk.CTkFrame(button_frame, fg_color=self.colors["accent"])
            button_frame_outer.grid(row=row, column=col, padx=15, pady=15)

            image_frame = ctk.CTkFrame(
                button_frame_outer,
                width=self.PET_IMAGE_SIZE[0],
                height=self.PET_IMAGE_SIZE[1],
                fg_color=self.colors["bg_medium"]
            )
            image_frame.pack(padx=3, pady=3)
            image_frame.pack_propagate(False)

            if self.pet_images.get(pet):
                image_label = ctk.CTkLabel(image_frame, image=self.pet_images[pet], text="")
                image_label.place(relx=0.5, rely=0.5, anchor="center")
            else:
                placeholder = ctk.CTkLabel(
                    image_frame,
                    text=f"{pet}\nImage",
                    font=self.pixel_font,
                    text_color=self.colors["text_dim"]
                )
                placeholder.place(relx=0.5, rely=0.5, anchor="center")

            pet_button = ctk.CTkButton(
                button_frame_outer,
                text=pet.upper(),
                width=160,
                height=40,
                corner_radius=0,
                font=self.button_font,
                fg_color=self.colors["bg_medium"],
                hover_color=self.colors["accent_dark"],
                text_color=self.colors["text"],
                command=lambda p=pet: self.select_pet(p)
            )
            pet_button.pack(padx=3, pady=3)

        name_frame = ctk.CTkFrame(selection_container, fg_color="transparent")
        name_frame.pack(pady=40)

        name_label = ctk.CTkLabel(
            name_frame,
            text="PET NAME:",
            font=self.pixel_font,
            text_color=self.colors["text_dim"]
        )
        name_label.pack(side="left", padx=15)

        self.name_entry = ctk.CTkEntry(
            name_frame,
            width=220,
            font=self.pixel_font,
            fg_color=self.colors["bg_medium"],
            border_color=self.colors["accent"],
            text_color=self.colors["text"]
        )
        self.name_entry.pack(side="left", padx=15)

        start_frame = ctk.CTkFrame(selection_container, fg_color="transparent")
        start_frame.pack(pady=30)

        self.start_button = ctk.CTkButton(
            start_frame,
            text="START GAME",
            font=self.button_font,
            width=220,
            height=45,
            corner_radius=0,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_dark"],
            text_color=self.colors["text"],
            command=self.start_game
        )
        self.start_button.pack()

    def create_game_screen(self):
        """Tworzy główny ekran gry po wyborze zwierzaka."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        game_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        game_container.place(relx=0.5, rely=0.5, anchor="center")

        self.pet_display = ctk.CTkFrame(
            game_container,
            width=self.PET_IMAGE_SIZE[0] + 40,
            height=self.PET_IMAGE_SIZE[1] + 80,
            fg_color=self.colors["bg_medium"],
            border_width=2,
            border_color=self.colors["accent"]
        )
        self.pet_display.pack(pady=20)
        self.pet_display.pack_propagate(False)

        self.name_label = ctk.CTkLabel(
            self.pet_display,
            text=self.selected_pet.name,
            font=self.title_font,
            text_color=self.colors["accent"]
        )
        self.name_label.pack(pady=10)

        image_frame = ctk.CTkFrame(
            self.pet_display,
            width=self.PET_IMAGE_SIZE[0],
            height=self.PET_IMAGE_SIZE[1],
            fg_color=self.colors["bg_dark"]
        )
        image_frame.pack(pady=5)
        image_frame.pack_propagate(False)

        if self.pet_images.get(self.pet_type):
            image_label = ctk.CTkLabel(image_frame, image=self.pet_images[self.pet_type], text="")
            image_label.place(relx=0.5, rely=0.5, anchor="center")
        else:
            placeholder = ctk.CTkLabel(
                image_frame,
                text=f"{self.pet_type}\nImage",
                font=self.pixel_font,
                text_color=self.colors["text_dim"]
            )
            placeholder.place(relx=0.5, rely=0.5, anchor="center")

        controls_frame = ctk.CTkFrame(game_container, fg_color="transparent")
        controls_frame.pack(pady=20, fill="x")

        food_frame = self.create_control_frame(controls_frame, "FOOD AMOUNT", "FEED", self.feed_pet)
        food_frame.pack(side="left", expand=True, padx=10)

        play_frame = self.create_control_frame(controls_frame, "PLAY TIME", "PLAY", self.play_with_pet)
        play_frame.pack(side="right", expand=True, padx=10)

        self.update_status_display()

    def create_control_frame(self, parent, label_text, button_text, command):
        """Tworzy ramkę kontrolną (dla karmienia i zabawy)."""
        frame = ctk.CTkFrame(parent, fg_color=self.colors["bg_medium"], border_width=1,
                             border_color=self.colors["accent"])

        ctk.CTkLabel(frame, text=label_text, font=self.pixel_font, text_color=self.colors["text_dim"]).pack(pady=5)

        entry = ctk.CTkEntry(
            frame,
            width=100,
            font=self.pixel_font,
            fg_color=self.colors["bg_dark"],
            border_color=self.colors["accent"],
            text_color=self.colors["text"]
        )
        entry.insert(0, "5")
        entry.pack(pady=5)

        ctk.CTkButton(
            frame,
            text=button_text,
            command=command,
            width=100,
            corner_radius=0,
            font=self.pixel_font,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_dark"],
            text_color=self.colors["text"]
        ).pack(pady=5)

        if button_text == "FEED":
            self.food_entry = entry
        else:
            self.play_entry = entry

        return frame

    def update_status_display(self):
        """Aktualizuje paski statusu (energia i nastrój)."""
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        title_frame = ctk.CTkFrame(self.stats_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 10))
        title_frame.grid_columnconfigure(0, weight=1)

        status_title = ctk.CTkLabel(title_frame, text="STATUS", font=self.button_font, text_color=self.colors["accent"])
        status_title.grid(row=0, column=0)

        self.create_status_bar("ENERGY", self.selected_pet.hunger)
        self.create_status_bar("MOOD", self.selected_pet.boredom)

    def create_status_bar(self, label, value):
        """Tworzy pojedynczy pasek statusu."""
        ctk.CTkLabel(
            self.stats_frame,
            text=f"{label}: {max(0, value):.0f}%",
            font=self.pixel_font,
            text_color=self.colors["text_dim"]
        ).pack(pady=2)

        progress = ctk.CTkProgressBar(
            self.stats_frame,
            width=160,
            height=15,
            corner_radius=0,
            fg_color=self.colors["bg_dark"],
            progress_color=self.colors["accent"]
        )
        progress.pack(pady=(0, 10))
        progress.set(max(0, min(value, 100)) / 100)

    def show_death_screen(self, pet_name):
        """Pokazuje ekran śmierci zwierzaka."""
        self.reset_game_state()

        message_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        message_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            message_frame,
            text=f"Your pet {pet_name}\nis no longer with us",
            font=self.title_font,
            text_color=self.colors["danger"]
        ).pack(pady=20)

        ctk.CTkButton(
            message_frame,
            text="RETURN TO MAIN MENU",
            command=self.create_pet_selection_screen,
            font=self.button_font,
            width=200,
            height=40,
            corner_radius=0,
            fg_color=self.colors["danger"],
            hover_color=self.colors["accent_dark"],
            text_color=self.colors["text"]
        ).pack(pady=20)

    def select_pet(self, pet_type):
        """Obsługuje wybór zwierzaka przez użytkownika."""
        self.pet_type = pet_type
        print(f"Selected pet: {pet_type}")

    def start_game(self):
        """Rozpoczyna grę z wybranym zwierzakiem."""
        name = self.name_entry.get().strip() or "Unnamed"

        rates = {
            "Dog": (2, 2),
            "Cat": (3, 2),
            "Rabbit": (3, 3),
            "Turtle": (1, 4)
        }

        hunger_rate, boredom_rate = rates[self.pet_type]
        self.selected_pet = Pet(name, hunger_rate, boredom_rate)

        self.running = True
        self.create_game_screen()
        self.update_loop()

    def feed_pet(self):
        """Funkcja karmienia zwierzaka."""
        if self.selected_pet.alive:
            try:
                amount = int(self.food_entry.get())
                if 0 <= amount <= 10:
                    self.selected_pet.feed(amount)
                    self.update_status_display()
            except ValueError:
                pass

    def play_with_pet(self):
        """Funkcja zabawy ze zwierzakiem."""
        if self.selected_pet.alive:
            try:
                time_spent = int(self.play_entry.get())
                if 0 <= time_spent <= 10:
                    self.selected_pet.play(time_spent)
                    self.update_status_display()
            except ValueError:
                pass

    def update_loop(self):
        """Główna pętla gry — co sekundę zmniejsza parametry zwierzaka."""
        if not self.selected_pet.alive:
            self.show_death_screen(self.selected_pet.name)
            return

        self.selected_pet.update()
        self.update_status_display()

        if self.running:
            self.root.after(1000, self.update_loop)


class Pet:
    """
    Klasa reprezentująca zwierzaka w grze.
    Przechowuje jego stan (energia i nastrój).
    """

    def __init__(self, name, hunger_rate, boredom_rate):
        """Inicjalizuje zwierzaka z danymi parametrami."""
        self.name = name
        self.hunger = 100
        self.boredom = 100
        self.hunger_rate = hunger_rate
        self.boredom_rate = boredom_rate
        self.alive = True

    def feed(self, amount):
        """Zwiększa energię zwierzaka (hunger)."""
        self.hunger = min(100, self.hunger + amount)

    def play(self, time_spent):
        """Zwiększa nastrój zwierzaka (boredom)."""
        self.boredom = min(100, self.boredom + time_spent)

    def update(self):
        """Zmniejsza energię i nastrój o stały współczynnik. Sprawdza śmierć."""
        self.hunger = max(0, self.hunger - self.hunger_rate)
        self.boredom = max(0, self.boredom - self.boredom_rate)
        if self.hunger <= 0 or self.boredom <= 0:
            self.alive = False


if __name__ == "__main__":
    """Uruchamia aplikację Neo Tamagotchi."""
    app = PixelPetGame()
    app.root.mainloop()
