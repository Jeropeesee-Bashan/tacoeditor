import sys
import gi
import os

from pathlib import Path

resources_dir = Path(__file__).parent / "resources"
os.environ["GI_TYPELIB_PATH"] = str(resources_dir)

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("TacoEditor", "1.0")

from gi.repository import (
    Gtk,
    Gio,
    Adw,
    TacoEditor,
)


@Gtk.Template(filename=str(resources_dir / "window.xml"))
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__ = "TacoEditorWindow"

    file_button = Gtk.Template.Child()
    theme_button = Gtk.Template.Child()
    welcome_picture = Gtk.Template.Child()
    main_box = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        picture_path = str(resources_dir / "welcome.svg")
        self.welcome_picture.set_filename(picture_path)

        file_menu = Gio.Menu()
        file_menu.append("New", "win.new")
        file_menu.append("Open", "win.open")
        file_menu.append("Exit", "win.exit")
        self.file_button.set_menu_model(file_menu)

        new_action = Gio.SimpleAction.new("new", None)
        new_action.connect("activate", self.on_new_clicked)
        self.add_action(new_action)

        open_action = Gio.SimpleAction.new("open", None)
        open_action.connect("activate", self.on_open_clicked)
        self.add_action(open_action)

        exit_action = Gio.SimpleAction.new("exit", None)
        exit_action.connect("activate", self.on_exit_clicked)
        self.add_action(exit_action)

        self.theme_button.connect("clicked", self.on_theme_toggle)
        gl_preview = TacoEditor.GLPreview()
        gl_preview.set_size_request(-1, 150)
        self.main_box.append(gl_preview)

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


class TacoEditorApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="su.kulenko.tacoeditor")

    def do_activate(self):
        window = MainWindow(application=self)
        window.present()


def main():
    os.chdir(Path(__file__).parent)
    app = TacoEditorApp()
    return app.run(sys.argv)
