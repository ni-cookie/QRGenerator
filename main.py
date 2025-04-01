import customtkinter as ctk 
from tkinter import filedialog, messagebox
import qrcode
import qrcode.image.svg
import os
from PIL import Image
import webbrowser 

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

class RadioButtonFrame(ctk.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master, fg_color="transparent", width=200)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.radiobuttons = []
        self.variable = ctk.StringVar(value="")

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="transparent", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        for i, value in enumerate(self.values):
            radiobutton = ctk.CTkRadioButton(self, text=value, value=value, variable=self.variable)
            radiobutton.grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="w")
            self.radiobuttons.append(radiobutton)

    def get(self):
        return self.variable.get()
    
    def set(self, value):
        self.variable.set(value)
        
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("QRGen") # Window title
        self.geometry("700x450")  # Window size

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(__file__), "images")
        icon_path = os.path.join(image_path, "QRGenLOGO_512x512.png")  # Use PNG instead of ICNS
        self.logo_image = ctk.CTkImage(Image.open(icon_path), size=(36, 36))
        self.home_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(3, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  QRGen", image=self.logo_image,
                                                             compound="left", font=ctk.CTkFont(size=25, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.about_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="About",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_about_button_event)
        self.about_button.grid(row=2, column=0, sticky="ew")

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["System", "Dark", "Light"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.textbox_label = ctk.CTkLabel(self.home_frame, text="Enter text or URL:")
        self.textbox_label.grid(row=0, column=0, padx=20, pady=(0, 0), sticky="s")
        self.textbox = ctk.CTkTextbox(self.home_frame, width=200, height=100, corner_radius=6)
        self.textbox.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="nsew")
        self.radiobuttons = RadioButtonFrame(self.home_frame, "Choose a format:", values=["PNG", "SVG"])
        self.radiobuttons.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")

        self.button = ctk.CTkButton(self.home_frame, text="Generate QR Code", command=self.on_click)
        self.button.grid(row=4, column=0, padx=10, pady=(20, 0), sticky="ns")
        
        # create about frame
        self.about_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        info_textarea = ctk.CTkTextbox(self.about_frame, width=480, height=320, corner_radius=6, cursor="arrow", fg_color="transparent")
        info_textarea.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="nsew")
        info_textarea.insert("0.0", "About app:\n\n"
                            "This application is designed to create QR codes from text information. 📱\n\n"
                            "With its help you can easily convert a text or a link into a QR code that can\n"
                            "be saved in PNG or SVG format. 🔗💾\n\n"
                            "Project Purpose:\n\n"
                            "This project was created solely to demonstrate my skills and knowledge in\n"
                            "development using Python, Tkinter, and other relevant\n"
                            "libraries and modules. 🛠️💻🚀\n\n"
                            "This application is not commercial and serves as an example of my mental\n"
                            "and practical achievements in programming. 🎓💡🌱\n\n"
                            "The application is open source and you can find the code on my \n"
                            "GitHub profile. 🌐👨‍💻")
        # make the text field read-only
        info_textarea.configure(state="disabled")

        def open_link():
            webbrowser.open("https://github.com/ni-cookie") # open my GitHub profile in the default browser

        # create a text label with a link
        link_label = ctk.CTkLabel(self.about_frame, text="Click here to visit my GitHub profile", fg_color="transparent", cursor="hand2", text_color="#2C8B62", font=("Roboto", 12))
        link_label.grid(row=1, column=0, padx=20, pady=20)

        # bind the left mouse button click handler to the label
        link_label.bind("<Button-1>", lambda e: open_link()) 

        self.label = ctk.CTkLabel(self.about_frame, text="Created by nicookie ❤️", font=("Roboto", 12), text_color="gray")
        self.label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="e")


        # select default frame
        self.select_frame_by_name("home")

    def on_click(self):
        link = self.textbox.get("1.0", "end").strip()
        if not link:
            messagebox.showerror("Error", "Please enter text or URL.")
            return

        qr = qrcode.QRCode(
            version = None, box_size = 10, border = 5, 
            error_correction = qrcode.constants.ERROR_CORRECT_H
            )
        qr.add_data(link)
        qr.make(fit=True)
        file_type = self.radiobuttons.get()
        if file_type == "PNG":
            img = qr.make_image(fill_color = 'black', back_color = 'white')
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                    filetypes=[("PNG files", "*.png")])
            if file_path:
                img.save(file_path)
                messagebox.showinfo("Success", f"QR Code saved as {file_path}")
        elif file_type == "SVG":
            factory = qrcode.image.svg.SvgPathImage
            img = qr.make_image(image_factory=factory)
            file_path = filedialog.asksaveasfilename(defaultextension=".svg",
                                                    filetypes=[("SVG files", "*.svg")])
            if file_path:
                img.save(file_path)
                messagebox.showinfo("Success", f"QR Code saved as {file_path}")
        qr.clear()    

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.about_button.configure(fg_color=("gray75", "gray25") if name == "about" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "about":
            self.about_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.about_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_about_button_event(self):
        self.select_frame_by_name("about")
    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)  

if __name__ == "__main__":
    app = App()
    app.mainloop()