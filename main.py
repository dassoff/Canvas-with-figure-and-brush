from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.graphics import *
from kivymd.uix.list import IRightBodyTouch
from kivy.utils import get_color_from_hex, get_hex_from_color
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.gridlayout import MDGridLayout

size_line = 5
type_edit = "Rectangle"
count = 1


class Holst(Image):
    def on_touch_down(self, touch):

        global count, x1, y1, x2, y2

        if count == 1:
            x1 = touch.x
            y1 = touch.y

            count += 1

        elif count == 2:
            x2 = touch.x
            y2 = touch.y

            count += 1

        try:
            with self.canvas:
                if x1 and x2 and y1 and y2 > 0:
                    s = get_color_from_hex(app.config.get('Pick', 'color'))

                    if app.type_edit == "line" and self.collide_point(touch.x + size_line / 2, touch.y + size_line / 2):
                        if(app.config.get('Pick', 'mode') == 'figure' and app.config.get('Pick', 'clear') == 'false'):
                            Color(s[0], s[1], s[2], s[3])
                            Rectangle(
                                pos=[((x1+x2)/2)-((x2-x1)/2), ((y1+y2)/2)-((y2-y1)/2)],
                                size=[x2-x1, y2-y1],
                                segments=4
                            )
                            x1, x2, y1, y2 = 0, 0, 0, 0
                            count = 1

                        elif(app.config.get('Pick', 'mode') == 'pen' and app.config.get('Pick', 'clear') == 'false'):
                            Color(s[0], s[1], s[2], s[3])
                            touch.ud["line"] = Line(
                                points=[touch.x-size_line/4, touch.y-size_line/4],
                                width=size_line/2
                            )
                        elif (app.config.get('Pick', 'clear') == 'true'):
                            Color(255, 255, 255, 1)
                            touch.ud["line"] = Line(
                                points=[touch.x - size_line / 4, touch.y - size_line / 4],
                                width=size_line / 2
                            )
        except:
            pass

    def on_touch_move(self, touch):
        try:
            with self.canvas:
                if(app.config.get('Pick', 'clear') == 'true'):
                    Color(255, 255, 255, 1)
                elif(app.config.get('Pick', 'clear') == 'false'):
                    s = get_color_from_hex(app.config.get('Pick', 'color'))
                    Color(s[0], s[1], s[2], s[3])
                if app.type_edit == "line" and self.collide_point(touch.x+size_line/2, touch.y+size_line/2):
                    touch.ud["line"].points += [touch.x-size_line/4, touch.y-size_line/4]
        except:
            pass


class IRightContainer(IRightBodyTouch, MDAnchorLayout):
    adaptive_height = True

class DSC(MDGridLayout):
    pass

class MyApp(MDApp):
    def switch_screen(self, screen):
        global count, x1, y1, x2, y2
        self.screen.ids.sm.current = screen
        x1, x2, y1, y2 = 0, 0, 0, 0
        count = 1

    def build_config(self, config):
        config.setdefaults(
            'Pick', {
                'color': '#000000ff',
                'mode': 'figure',
                'clear': 'false'

            }
        )

    def switch_mode(self, btn):
        if btn.active:
            self.config.set('Pick', 'mode', 'figure')
            self.config.set('Pick', 'clear', 'false')
        else:
            self.config.set('Pick', 'mode', 'pen')
            self.config.set('Pick', 'clear', 'false')
        self.config.write()


    def clear_line(self):
        self.config.set('Pick', 'clear', 'true')
        self.config.write()

    def show_dialog_color(self):
        if not self.dialog:
            color = ['#ff0000ff',
                      '#800080ff',
                      '#ffff00ff',
                      '#008000ff',
                      '#000000ff',
                      '#d2691eff',
                      '#00ffffff',
                      '#008080ff',
                      '#0000ffff',
                      '#ff4500ff',
                      '#c71585ff',
                      ]


            content = DSC()
            for item in color:
                btn = MDFloatingActionButton(
                    md_bg_color=item

                )
                btn.bind(on_press=self.switch_color)

                content.add_widget(btn)
            self.dialog=MDDialog(
                title='Выберите цвет',
                type='custom',
                content_cls=content
            )
            self.dialog.open()


    def switch_color(self,btn):

        color = None
        match get_hex_from_color(btn.md_bg_color):
            case '#ff0000ff':
                color = '#ff0000ff'

            case '#800080ff':
                color = '#800080ff'

            case '#ffff00ff':
                color = '#ffff00ff'

            case '#008000ff':
                color = '#008000ff'

            case '#000000ff':
                color = '#000000ff'

            case '#d2691eff':
                color = '#d2691eff'

            case '#00ffffff':
                color = '#00ffffff'

            case '#008080ff':
                color = '#008080ff'

            case '#0000ffff':
                color = '#0000ffff'

            case '#ff4500ff':
                color = '#ff4500ff'

            case '#c71585ff':
                color = '#c71585ff'

        self.config.set('Pick', 'color', color)
        self.config.write()
        self.screen.ids.color_btn.md_bg_color = btn.md_bg_color
        self.dialog.dismiss()
        self.dialog=None

    def clear_canvas(self):
        self.screen.ids.holst.canvas.clear()

    def build(self):
        self.type_edit = 'line'
        self.screen=Builder.load_file('ui.kv')
        self.dialog = None

        self.config.set('Pick', 'clear', 'false')
        self.config.write()
        self.theme_cls.primary_palette = "Purple"
        return self.screen

app = MyApp()
app.run()