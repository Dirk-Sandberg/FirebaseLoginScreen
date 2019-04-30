from kivy.animation import Animation

def animate(widget, **kwargs):
    anim = Animation(**kwargs)
    anim.start(widget)