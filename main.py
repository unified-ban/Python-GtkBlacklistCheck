import gi, requests, json
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

token="YOUR_API_KEY"

class UnifiedbanGUIWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="unified/ban GUI")
        self.set_size_request(350, 200)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Enter User_ID")
        self.entry.connect("activate", self.on_entry_activate)

        vbox.add(self.entry)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        
        vbox.add(scrolledwindow)

        textview = Gtk.TextView()
        self.textbuffer = textview.get_buffer()
        self.textbuffer.set_text("Wait for input ..")

        scrolledwindow.add(textview)

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