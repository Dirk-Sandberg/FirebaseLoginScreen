"""
Buttons
=======

Copyright (c) 2015 Andrés Rodríguez and KivyMD contributors -
    KivyMD library up to version 0.1.2
Copyright (c) 2019 Ivanov Yuri and KivyMD contributors -
    KivyMD library version 0.1.3 and higher

For suggestions and questions:
<kivydevelopment@gmail.com>

This file is distributed under the terms of the same license,
as the Kivy framework.

`Material Design spec, Buttons <https://material.io/design/components/buttons.html>`

`Material Design spec, Buttons: floating action button <https://material.io/design/components/buttons-floating-action-button.html>`

Example
-------

from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory

from kivymd.theming import ThemeManager

Builder.load_string('''
#:import MDToolbar kivymd.toolbar.MDToolbar
#:import MDIconButton kivymd.button.MDIconButton
#:import MDFloatingActionButton kivymd.button.MDFloatingActionButton
#:import MDFlatButton kivymd.button.MDFlatButton
#:import MDRaisedButton kivymd.button.MDRaisedButton
#:import MDRectangleFlatButton kivymd.button.MDRectangleFlatButton
#:import MDRoundFlatButton kivymd.button.MDRoundFlatButton
#:import MDRoundFlatIconButton kivymd.button.MDRoundFlatIconButton
#:import MDFillRoundFlatButton kivymd.button.MDFillRoundFlatButton
#:import MDTextButton kivymd.button.MDTextButton


<ExampleButtons@BoxLayout>
    orientation: 'vertical'

    MDToolbar:
        id: toolbar
        title: app.title
        md_bg_color: app.theme_cls.primary_color
        background_palette: 'Primary'
        elevation: 10
        left_action_items: [['dots-vertical', lambda x: None]]

    Screen:
        BoxLayout:
            size_hint_y: None
            height: '56'
            spacing: '10dp'
            pos_hint: {'center_y': .9}

            Widget:

            MDIconButton:
                icon: 'sd'

            MDFloatingActionButton:
                icon: 'plus'
                opposite_colors: True
                elevation_normal: 8

            MDFloatingActionButton:
                icon: 'check'
                opposite_colors: True
                elevation_normal: 8
                md_bg_color: app.theme_cls.primary_color

            MDIconButton:
                icon: 'sd'
                theme_text_color: 'Custom'
                text_color: app.theme_cls.primary_color

            Widget:

        MDFlatButton:
            text: 'MDFlatButton'
            pos_hint: {'center_x': .5, 'center_y': .75}

        MDRaisedButton:
            text: "MDRaisedButton"
            elevation_normal: 2
            opposite_colors: True
            pos_hint: {'center_x': .5, 'center_y': .65}

        MDRectangleFlatButton:
            text: "MDRectangleFlatButton"
            pos_hint: {'center_x': .5, 'center_y': .55}

        MDRectangleFlatIconButton:
            text: "MDRectangleFlatIconButton"
            icon: "language-python"
            pos_hint: {'center_x': .5, 'center_y': .45}
            width: dp(230)

        MDRoundFlatButton:
            text: "MDRoundFlatButton"
            icon: "language-python"
            pos_hint: {'center_x': .5, 'center_y': .35}

        MDRoundFlatIconButton:
            text: "MDRoundFlatIconButton"
            icon: "language-python"
            pos_hint: {'center_x': .5, 'center_y': .25}
             width: dp(200)

        MDFillRoundFlatButton:
            text: "MDFillRoundFlatButton"
            pos_hint: {'center_x': .5, 'center_y': .15}

        MDTextButton:
            text: "MDTextButton"
            pos_hint: {'center_x': .5, 'center_y': .05}
''')


class Example(App):
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Blue'
    title = "Example Buttons"
    main_widget = None

    def build(self):
        return Factory.ExampleButtons()


Example().run()
"""

from kivy.clock import Clock
from kivy.graphics.context_instructions import Color
from kivy.graphics.stencil_instructions import StencilPush, StencilUse,\
    StencilPop, StencilUnUse
from kivy.graphics.vertex_instructions import Ellipse, RoundedRectangle
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty, BoundedNumericProperty,\
    ListProperty, AliasProperty, BooleanProperty, NumericProperty,\
    OptionProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation

from kivymd.backgroundcolorbehavior import SpecificBackgroundColorBehavior
from kivymd.ripplebehavior import CircularRippleBehavior,\
    RectangularRippleBehavior
from kivymd.elevation import CommonElevationBehavior,\
    RectangularElevationBehavior, CircularElevationBehavior
from kivymd.theming import ThemableBehavior

Builder.load_string('''
#:import Animation kivy.animation.Animation
#:import md_icons kivymd.icon_definitions.md_icons
#:import colors kivymd.color_definitions.colors
#:import MDIcon kivymd.label.MDIcon
#:import MDLabel kivymd.label.MDLabel
#:import images_path kivymd.images_path


<BaseButton>
    size_hint: (None, None)
    anchor_x: 'center'
    anchor_y: 'center'


<BaseFlatButton>


<BaseRaisedButton>


<BaseRoundButton>
    canvas:
        Clear
        Color:
            rgba: self._current_button_color
        Ellipse:
            size: self.size
            pos: self.pos

    size: (dp(48), dp(48))
    lbl_txt: lbl_txt
    padding: dp(12)
    theme_text_color: 'Primary'

    MDIcon:
        id: lbl_txt
        icon: root.icon
        theme_text_color: root.theme_text_color
        text_color: root.text_color
        disabled: root.disabled
        valign: 'middle'
        halign: 'center'
        opposite_colors: root.opposite_colors


<BaseRectangularButton>
    canvas:
        Clear
        Color:
            rgba: self._current_button_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: (root._radius, )

    lbl_txt: lbl_txt
    height: dp(36) if not root._height else root._height
    width: lbl_txt.texture_size[0] + root.increment_width
    padding: (dp(8), 0)
    theme_text_color: 'Primary'

    MDLabel:
        id: lbl_txt
        text: root.text if root.button_label else ''
        font_style: 'Button'
        can_capitalize: root.can_capitalize
        size_hint_x: None
        text_size: (None, root.height)
        height: self.texture_size[1]
        theme_text_color: root.theme_text_color
        text_color: root.text_color
        disabled: root.disabled
        valign: 'middle'
        halign: 'center'
        opposite_colors: root.opposite_colors


<MDRoundFlatButton>
    canvas.before:
        Color:
            rgba: root.theme_cls.primary_color
        Line:
            width: 1
            rounded_rectangle:
                (self.x, self.y, self.width, self.height,\
                root._radius, root._radius, root._radius, root._radius,\
                self.height)

    theme_text_color: 'Custom'
    text_color: root.theme_cls.primary_color


<MDFillRoundFlatButton>
    canvas.before:
        Color:
            rgba: root.theme_cls.primary_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [root._radius, ]

    text_color: root.specific_text_color


<MDRectangleFlatButton>
    canvas.before:
        Color:
            rgba: root.theme_cls.primary_color
        Line:
            width: 1
            rectangle: (self.x, self.y, self.width, self.height)

    theme_text_color: 'Custom'
    text_color: root.theme_cls.primary_color


<MDRectangleFlatIconButton>
    canvas.before:
        Color:
            rgba: app.theme_cls.primary_color
        Line:
            width: 1
            rectangle: (self.x, self.y, self.width, self.height)

    size_hint_x: None
    width: dp(150)

    BoxLayout:
        spacing: dp(10)

        MDIcon:
            id: lbl_ic
            icon: root.icon
            theme_text_color: 'Custom'
            text_color: root.theme_cls.primary_color
            size_hint_x: None
            width: self.texture_size[0]

        MDLabel:
            id: lbl_txt
            text: root.text
            font_style: 'Button'
            can_capitalize: root.can_capitalize
            shorten: True
            theme_text_color: 'Custom'
            text_color: root.theme_cls.primary_color


<MDRoundFlatIconButton>
    size_hint_x: None
    width: dp(150)

    BoxLayout:
        spacing: dp(10)

        MDIcon:
            id: lbl_ic
            icon: root.icon
            theme_text_color: 'Custom'
            text_color: root.theme_cls.primary_color
            size_hint_x: None
            width: self.texture_size[0]

        MDLabel:
            id: lbl_txt
            text: root.text
            font_style: 'Button'
            can_capitalize: root.can_capitalize
            shorten: True
            theme_text_color: 'Custom'
            text_color: root.theme_cls.primary_color


<MDRaisedButton>
    md_bg_color: (0,0,0,1)#root.theme_cls.primary_color
    theme_text_color: 'Custom'
    text_color: (0,0,0,1)#root.specific_text_color


<MDFloatingActionButton>
    # Defaults to 56-by-56 and a backround of the accent color according to
    # guidelines
    size: (dp(56), dp(56))
    md_bg_color: root.theme_cls.accent_color
    theme_text_color: 'Custom'
    text_color: root.specific_text_color


<MDTextButton>
    size_hint: None, None
    size: self.texture_size
    #color:
    #    root.theme_cls.primary_color if not len(root.custom_color)\
    #    else root.custom_color
    #background_down: '{}transparent.png'.format(images_path)
    #background_normal: '{}transparent.png'.format(images_path)
    opacity: 1
''')


class BaseButton(ThemableBehavior, ButtonBehavior,
                 SpecificBackgroundColorBehavior, AnchorLayout):
    """
    Abstract base class for all MD buttons. This class handles the button's
    colors (disabled/down colors handled in children classes as those depend on
    type of button) as well as the disabled state.
    """

    _md_bg_color_down = ListProperty(None, allownone=True)
    _md_bg_color_disabled = ListProperty(None, allownone=True)
    _current_button_color = ListProperty([.0, .0, .0, .0])
    theme_text_color = OptionProperty(None, allownone=True,
                                      options=['Primary', 'Secondary', 'Hint',
                                               'Error', 'Custom',
                                               'ContrastParentBackground'])
    text_color = ListProperty(None, allownone=True)
    opposite_colors = BooleanProperty(False)
    font_name = StringProperty()

    def on_font_name(self, instance, value):
        instance.ids.lbl_txt.font_name = value

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):
        self._update_color()

    def on_md_bg_color(self, instance, value):
        self._update_color()

    def _update_color(self):
        if not self.disabled:
            self._current_button_color = self.md_bg_color
        else:
            self._current_button_color = self.md_bg_color_disabled

    def _call_get_bg_color_down(self):
        return self._get_md_bg_color_down()

    def _get_md_bg_color_down(self):
        if self._md_bg_color_down:
            return self._md_bg_color_down
        else:
            raise NotImplementedError

    def _set_md_bg_color_down(self, value):
        self._md_bg_color_down = value

    md_bg_color_down = AliasProperty(_call_get_bg_color_down,
                                     _set_md_bg_color_down)

    def _call_get_bg_color_disabled(self):
        return self._get_md_bg_color_disabled()

    def _get_md_bg_color_disabled(self):
        if self._md_bg_color_disabled:
            return self._md_bg_color_disabled
        else:
            raise NotImplementedError

    def _set_md_bg_color_disabled(self, value):
        self._md_bg_color_disabled = value

    md_bg_color_disabled = AliasProperty(_call_get_bg_color_disabled,
                                         _set_md_bg_color_disabled)

    def on_disabled(self, instance, value):
        if self.disabled:
            self._current_button_color = self.md_bg_color_disabled
        else:
            self._current_button_color = self.md_bg_color


class BasePressedButton(BaseButton):
    """
    Abstract base class for those button which fade to a background color on
    press.
    """

    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            return False
        elif not self.collide_point(touch.x, touch.y):
            return False
        elif self in touch.ud:
            return False
        elif self.disabled:
            return False
        else:
            self.fade_bg =\
                Animation(duration=.5,
                          _current_button_color=self.md_bg_color_down)
            self.fade_bg.start(self)
            return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            self.fade_bg.stop_property(self, '_current_button_color')
            Animation(duration=.05,
                      _current_button_color=self.md_bg_color).start(self)
        return super().on_touch_up(touch)


class BaseFlatButton(BaseButton):
    """
    Abstract base class for flat buttons which do not elevate from material.

    Enforces the recommended down/disabled colors for flat buttons
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = (.0, .0, .0, .0)

    def _get_md_bg_color_down(self):
        if self.theme_cls.theme_style == 'Dark':
            c = get_color_from_hex('cccccc')
            c[3] = .25
        else:
            c = get_color_from_hex('999999')
            c[3] = .4
        return c

    def _get_md_bg_color_disabled(self):
        bg_c = self.md_bg_color
        if bg_c[3] == 0:  # transparent background
            c = bg_c
        else:
            if self.theme_cls.theme_style == 'Dark':
                c = (1., 1., 1., .12)
            else:
                c = (.0, .0, .0, .12)
        return c


class BaseRaisedButton(CommonElevationBehavior, BaseButton):
    """
    Abstract base class for raised buttons which elevate from material.
    Raised buttons are to be used sparingly to emphasise primary/important
    actions.

    Implements elevation behavior as well as the recommended down/disabled
    colors for raised buttons.
    """

    def __init__(self, **kwargs):
        if self.elevation_raised == 0 and self.elevation_normal + 6 <= 12:
            self.elevation_raised = self.elevation_normal + 6
        elif self.elevation_raised == 0:
            self.elevation_raised = 12
        super().__init__(**kwargs)
        self.elevation_press_anim = Animation(elevation=self.elevation_raised,
                                              duration=.2, t='out_quad')
        self.elevation_release_anim = Animation(
            elevation=self.elevation_normal, duration=.2, t='out_quad')

    _elev_norm = NumericProperty(2)

    def _get_elev_norm(self):
        return self._elev_norm

    def _set_elev_norm(self, value):
        self._elev_norm = value if value <= 12 else 12
        self._elev_raised = (value + 6) if value + 6 <= 12 else 12
        self.elevation = self._elev_norm
        self.elevation_release_anim = Animation(elevation=value,
                                                duration=.2, t='out_quad')

    elevation_normal = AliasProperty(
        _get_elev_norm, _set_elev_norm, bind=('_elev_norm',))
    _elev_raised = NumericProperty(8)

    def _get_elev_raised(self):
        return self._elev_raised

    def _set_elev_raised(self, value):
        self._elev_raised = value if value + self._elev_norm <= 12 else 12
        self.elevation_press_anim = Animation(elevation=value,
                                              duration=.2, t='out_quad')

    elevation_raised = AliasProperty(
        _get_elev_raised, _set_elev_raised, bind=('_elev_raised',))

    def on_disabled(self, instance, value):
        if self.disabled:
            self.elevation = 0
        else:
            self.elevation = self.elevation_normal
        super().on_disabled(instance, value)

    def on_touch_down(self, touch):
        if not self.disabled:
            if touch.is_mouse_scrolling:
                return False
            if not self.collide_point(touch.x, touch.y):
                return False
            if self in touch.ud:
                return False
            self.elevation_press_anim.stop(self)
            self.elevation_press_anim.start(self)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if not self.disabled:
            if touch.grab_current is not self:
                return super().on_touch_up(touch)
            self.elevation_release_anim.stop(self)
            self.elevation_release_anim.start(self)
        return super().on_touch_up(touch)

    def _get_md_bg_color_down(self):
        t = self.theme_cls
        c = self.md_bg_color  # Default to no change on touch
        # Material design specifies using darker hue when on Dark theme
        if t.theme_style == 'Dark':
            if self.md_bg_color == t.primary_color:
                c = t.primary_dark
            elif self.md_bg_color == t.accent_color:
                c = t.accent_dark
        return c

    def _get_md_bg_color_disabled(self):
        if self.theme_cls.theme_style == 'Dark':
            c = (1., 1., 1., .12)
        else:
            c = (.0, .0, .0, .12)
        return c


class BaseRoundButton(CircularRippleBehavior, BaseButton):
    """
    Abstract base class for all round buttons, bringing in the appropriate
    on-touch behavior
    """

    pass


class BaseRectangularButton(RectangularRippleBehavior, BaseButton):
    """
    Abstract base class for all rectangular buttons, bringing in the
    appropriate on-touch behavior. Also maintains the correct minimum width
    as stated in guidelines.
    """

    width = BoundedNumericProperty(dp(88), min=dp(88), max=None,
                                   errorhandler=lambda x: dp(88))
    text = StringProperty('')
    increment_width = NumericProperty(dp(32))
    _radius = NumericProperty(dp(2))
    _height = NumericProperty(dp(0))
    button_label = BooleanProperty(True)
    can_capitalize = BooleanProperty(True)


class MDIconButton(BaseRoundButton, BaseFlatButton, BasePressedButton):
    icon = StringProperty('checkbox-blank-circle')


class MDFlatButton(BaseRectangularButton, BaseFlatButton, BasePressedButton):
    pass


class BaseFlatIconButton(MDFlatButton):
    icon = StringProperty('android')
    text = StringProperty('')
    button_label = BooleanProperty(False)


class MDRaisedButton(BaseRectangularButton, RectangularElevationBehavior,
                     BaseRaisedButton, BasePressedButton):
    pass


class MDFloatingActionButton(BaseRoundButton, CircularElevationBehavior,
                             BaseRaisedButton):
    icon = StringProperty('android')
    background_palette = StringProperty('Accent')


class MDRectangleFlatButton(MDFlatButton):
    pass


class MDRoundFlatButton(MDFlatButton):
    _radius = NumericProperty(dp(18))

    def lay_canvas_instructions(self):
        with self.canvas.after:
            StencilPush()
            RoundedRectangle(size=self.size,
                             pos=self.pos,
                             radius=[self._radius, ])
            StencilUse()
            self.col_instruction = Color(rgba=self.ripple_color)
            self.ellipse =\
                Ellipse(size=(self.ripple_rad, self.ripple_rad),
                        pos=(self.ripple_pos[0] - self.ripple_rad / 2.,
                             self.ripple_pos[1] - self.ripple_rad / 2.))
            StencilUnUse()
            RoundedRectangle(size=self.size,
                             pos=self.pos,
                             radius=[self._radius, ])
            StencilPop()
        self.bind(ripple_color=self._set_color, ripple_rad=self._set_ellipse)


class MDTextButton(ThemableBehavior, Button):
    custom_color = ListProperty()
    """Custom user button color"""

    def animation_label(self):
        def set_default_state_label(*args):
            Animation(opacity=1, d=.1, t='in_out_cubic').start(self)

        anim = Animation(opacity=.5, d=.2, t='in_out_cubic')
        anim.bind(on_complete=set_default_state_label)
        anim.start(self)

    def on_press(self, *args):
        self.animation_label()
        return super().on_press(*args)


class MDFillRoundFlatButton(MDRoundFlatButton):
    pass


class MDRectangleFlatIconButton(BaseFlatIconButton):
    pass


class MDRoundFlatIconButton(MDRoundFlatButton, BaseFlatIconButton):
    pass
