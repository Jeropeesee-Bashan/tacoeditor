import sys
import gi
import os

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import (
    Gtk,
    Gio,
    Adw
)

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_title("Taco Editor")
        self.set_default_size(800, 600)

        toolbar = Adw.ToolbarView()
        header_bar = Adw.HeaderBar()
        toolbar.add_top_bar(header_bar)
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.append(toolbar)
        self.set_content(main_box)

        theme_button = Gtk.Button()
        theme_button.set_icon_name("weather-clear-night-symbolic")
        theme_button.connect("clicked", self.on_theme_toggle)
        header_bar.pack_end(theme_button)

        file_button = Gtk.MenuButton(label="File")
        header_bar.pack_start(file_button)
        new_action = Gio.SimpleAction.new("new", None)
        new_action.connect("activate", self.on_new_clicked)
        self.add_action(new_action)

        open_action = Gio.SimpleAction.new("open", None)
        open_action.connect("activate", self.on_open_clicked)
        self.add_action(open_action)

        exit_action = Gio.SimpleAction.new("exit", None)
        exit_action.connect("activate", self.on_exit_clicked)
        self.add_action(exit_action)

        file_menu = Gio.Menu()
        file_menu.append("New", "win.new")
        file_menu.append("Open", "win.open")
        file_menu.append("Exit", "win.exit")
        file_button.set_menu_model(file_menu)

        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        content_box.set_valign(Gtk.Align.CENTER)
        content_box.set_halign(Gtk.Align.CENTER)
        content_box.set_vexpand(True)
        main_box.append(content_box)

        resource_path = os.path.join(os.path.dirname(__file__), "resources", "welcome.svg")

        picture = Gtk.Picture.new_for_filename(resource_path)
        content_box.append(picture)

        label = Gtk.Label()
        label.set_markup('Welcome to Taco Editor!\nYou can open an existing project or create a new one...')
        label.set_justify(Gtk.Justification.CENTER)
        label.set_wrap(True)
        content_box.append(label)

    def on_new_clicked(self, action, param):
        print("New project functionality will be implemented here")

    def on_open_clicked(self, action, param):
        print("Open project functionality will be implemented here")

    def on_exit_clicked(self, action, param):
        self.close()

    def on_theme_toggle(self, button):
        style_manager = Adw.StyleManager.get_default()
        is_dark = style_manager.get_dark()
        style_manager.set_color_scheme(
            Adw.ColorScheme.FORCE_LIGHT if is_dark else Adw.ColorScheme.FORCE_DARK
        )
        button.set_icon_name(
            "weather-clear-symbolic" if is_dark else "weather-clear-night-symbolic"
        )

class MyGtkApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id='su.kulenko.tacoeditor')
        
    def do_activate(self):
        window = MainWindow(application=self)
        window.present()

def main():
    app = MyGtkApp()
    return app.run(sys.argv)

if __name__ == '__main__':
    main()
