import gi, requests, json
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

token="YOUR_TOKEN"

class UnifiedbanGUIWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="unified/ban GUI")
        self.set_size_request(400, 250)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-application-prefer-dark-theme", True)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.set_border_width(20)
        self.add(vbox)

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Enter User_ID and press Enter")
        self.entry.connect("activate", self.on_entry_activate)

        vbox.add(self.entry)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        
        vbox.add(scrolledwindow)

        textview = Gtk.TextView()
        textview.set_border_width(10)
        self.textbuffer = textview.get_buffer()
        self.textbuffer.set_text("Wait for input ..")

        scrolledwindow.add(textview)
        textview.grab_focus()

        self.add(vbox)
    
    def on_entry_activate(self, entry):
        api_url = "https://api.unifiedban.solutions/blacklist/check/%s" % self.entry.get_text()
        
        response = requests.get(
            api_url, headers = {
                'Authorization': token
            }
        )

        try:
            self.textbuffer.set_text(
                json.dumps(
                    json.loads(response.text),
                    sort_keys=True,
                    indent=4
                )
            )
        except:
            self.textbuffer.set_text(
                json.dumps(
                    '{"Error": "No data"}',
                    sort_keys=True,
                    indent=4
                )
            )


win = UnifiedbanGUIWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
