from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy import properties as P
from kivy.animation import Animation
from kivymd.uix.screen import MDScreen


KV = """
<HomeMainScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 1,1,1,1
        MDBoxLayout:
            id: banner
            orientation: 'vertical'
            size_hint_y: None
            height: root.banner_height
            canvas:
                Color:
                    rgba: 1,1,1,root.banner_opacity
                Rectangle:
                    pos: self.pos
                    size: self.size
                    source: "assets/banner.jpg"
            canvas.after:
                Color:
                    rgba: 1,1,1,1
                Rectangle:
                    pos: self.pos
                    size: self.width, dp(50)
                    source: "assets/wave.png"
        MDBoxLayout:
            orientation: 'vertical'
            md_bg_color: 1,1,1,1
            MDCard:
                opacity: 0
                id: description
                elevation: 10
                size_hint: .7, None
                radius: [self.height*.05]
                height: self.minimum_height # (root.height-dp((banner.height+30)))
                pos_hint: {'center_x': .5}
                md_bg_color: .3,.3,.3,1
                MDLabel:
                    text:
                        "Lorem ipsum dolor, sit amet consectetur adipisicing elit." \
                        + " omnis modi reiciendis, incidunt nihil illum nesciunt " \
                        + "dicta sint! Voluptas dignissimos perferendis."
                    padding: dp(20), dp(30)
                    font_name: "assets/GothamRounded-Light.otf"
                    line_height: 1.2
                    halign: "center"
                    color: 1,1,1
                    adaptive_height: True
        MDFloatLayout:
            size_hint_y: None
            height: dp(20)
            MDCard:
                id: card
                orientation: 'vertical'
                size_hint: .7,None
                height: root.width*.8
                md_bg_color: .5,.5,.5,1
                radius: [self.height*.05]
                elevation: 10
                pos_hint: {'center_x': .5}
                y: dp(50)
                padding: dp(20), dp(20)
                spacing: dp(30)
                FitImage:
                    id: image
                    source: "assets/banner.jpg"
                    radius: [self.height*.05]
                MDFillRoundFlatButton:
                    text: "READ MORE"
                    pos_hint: {'center_x': .5}
                    md_bg_color: .3,.3,.3,1
                    on_release: root.activate = not root.activate

"""

Builder.load_string(KV)


class HomeMainScreen(MDScreen):
    activate = P.BooleanProperty(0)
    banner_height = P.NumericProperty("200dp")
    banner_opacity = P.NumericProperty(1)

    def on_activate(self, *args):
        if self.activate:
            pos_y = self.top - (self.ids.card.height + dp(30))
            anim_banner = Animation(banner_height=self.height / 2, banner_opacity=0.3)
            anim_banner.start(self)
            anim_opacity = Animation(opacity=1)
            anim_pos = Animation(y=pos_y)
            anim_pos.start(self.ids.card)
            anim_pos.bind(
                on_complete=lambda *_: anim_opacity.start(self.ids.description)
            )
        else:
            anim_banner = Animation(banner_height=dp(200), banner_opacity=1)
            anim_pos = Animation(y=dp(50))
            anim_opacity = Animation(opacity=0)
            anim_opacity.start(self.ids.description)
            anim_opacity.bind(on_complete=lambda *_: anim_pos.start(self.ids.card))
            anim_opacity.bind(on_complete=lambda *_: anim_banner.start(self))


class MainScreenApp(MDApp):
    def build(self):
        return HomeMainScreen()


if __name__ == "__main__":
    MainScreenApp().run()
