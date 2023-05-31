# import generales
import sys
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gio, GObject, Gtk

#Clase muestra opciones
class Widget(GObject.Object):
    __gtype_name__ = 'Widget'
    def __init__(self, name):
        super().__init__()
        self._name = name
    @GObject.Property
    def name(self):
        return self._name

#Clase principal que ejecutara la ventana
class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        #Condiciones iniciales
        super().__init__(*args, **kwargs)
        self.app_ = self.get_application()
        self.main_vertical_box = Gtk.Box.new(Gtk.Orientation.VERTICAL,15)
        self.set_default_size(600, 150)
        self.set_title("VENTANA")
        self.set_child(self.main_vertical_box)
        self.buscador = ""
        #Variables del dropdown
        self.text_select = ["Hombre","Mujer","Barbie", "Ken"]
        #Dropdown 1
        self.dropdown_1 = Gtk.DropDown.new_from_strings(self.text_select)
        self.main_vertical_box.append(self.dropdown_1)
        #Boton del dropdown 1
        self.print_button1 = Gtk.Button.new()
        self.print_button1.props.label = "Print del texto en Dropdown1"
        self.print_button1.connect("clicked", self.print_select_dropdown, self.dropdown_1)
        self.main_vertical_box.append(self.print_button1)
        #Box horizontal 1
        self.secundary_horizontal_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 1)
        self.secundary_horizontal_box.set_homogeneous(True)
        self.main_vertical_box.append(self.secundary_horizontal_box)
        #Entry text pt.1
        self.texto = Gtk.Entry()
        self.secundary_horizontal_box.append(self.texto)
        #Model
        self.model_widget = Gio.ListStore(item_type=Widget)
        self.filtro_lista = Gtk.FilterListModel(model=self.model_widget)
        self.filtro_lista_custum = Gtk.CustomFilter.new(self.filtrar, self.filtro_lista)
        self.filtro_lista.set_filter(self.filtro_lista_custum)
        for i in self.text_select:
            self.model_widget.append(Widget(i))
        #factory
        self.factory = Gtk.SignalListItemFactory()
        self.factory.connect("setup", self._on_factory_widget_setup)
        self.factory.connect("bind", self._on_factory_widget_bind)
        #Dropdown 2
        self.dropdown_2 = Gtk.DropDown(model=self.filtro_lista, factory=self.factory)
        self.dropdown_2.set_enable_search(True)
        self.dropdown_2.connect("notify::selected-item", self.refresh)
        self.secundary_horizontal_box.append(self.dropdown_2)
        #Search Bar
        search_entry = self._get_search_entry_widget(self.dropdown_2)
        search_entry.connect('search-changed', self._on_search_widget_changed)
        #Boton 1 del dropdown 2
        self.print_button2 = Gtk.Button.new()
        self.print_button2.props.label = "Print del texto en Entry"
        self.print_button2.connect("clicked", self.print_select_entry, self.texto)
        self.main_vertical_box.append(self.print_button2)
        #Boton Salir
        self.quit_button = Gtk.Button.new_with_label("Salir")
        self.quit_button.connect("clicked",self.salir_boton)
        self.main_vertical_box.append(self.quit_button)

    #print dropdown con la accion "Click"
    def print_select_dropdown(self,p_button,texto):
        print(self.text_select[texto.get_selected()])

    #print del entry
    def print_select_entry(self,p_button,texto):
        print(texto.get_text())

    #Mueve automaticamente la seleccion al entry
    def refresh(self, dropdown, data):
        self.texto.set_text(self.text_select[dropdown.get_selected()])

    #Conecta la eleccion del Boton Salir con la accion "Click"
    def salir_boton(self,p_button):
        self.close()

    #Set up del dropdown
    def _on_factory_widget_setup(self, factory, list_item):
        box = Gtk.Box()
        label = Gtk.Label()
        box.append(label)
        list_item.set_child(box)

    #Une la lista con el dropdown
    def _on_factory_widget_bind(self, factory, list_item):
        box = list_item.get_child()
        label = box.get_first_child()
        widget = list_item.get_item()
        label.set_text(widget.name)

    #retorna los valores que esten en la lista
    def filtrar(self, item, listmodel):
        return self.buscador.upper() in item.name.upper()

    #tener a mano la barra de busqueda
    def _get_search_entry_widget(self, dropdown):
        popover = dropdown.get_last_child()
        box = popover.get_child()
        box2 = box.get_first_child()
        search_entry = box2.get_first_child()
        return search_entry

    #compara el search con la lista por el filtro
    def _on_search_widget_changed(self, search_entry):
        self.buscador = search_entry.get_text()
        self.filtro_lista_custum.changed(Gtk.FilterChange.DIFFERENT)

#Run aplication
class MyApp(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def do_activate(self):
        active_window = self.props.active_window
        if active_window:
            active_window.present()
        else:
            self.win = MainWindow(application=self)
            self.win.present()


app = MyApp(application_id="com.myapplicationexample",
            flags= Gio.ApplicationFlags.FLAGS_NONE)
app.run(sys.argv)
