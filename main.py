from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.graphics import Color, Line
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

import math


PHOSPHOR_GREEN = (0x39 / 255.0, 0xFF / 255.0, 0x14 / 255.0, 1.0)


class RadarWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.beam_angle = 0.0
        self.rotation_speed = 95.0  # degrees per second
        self.pulse_phase = 0.0

        # خلفية وخطوط الشبكة (ستايل هاكينج)
        with self.canvas.before:
            Color(PHOSPHOR_GREEN[0], PHOSPHOR_GREEN[1], PHOSPHOR_GREEN[2], 0.15)
            self.grid_h_lines = [Line(points=[0, 0, 0, 0], width=0.4) for _ in range(8)]
            self.grid_v_lines = [Line(points=[0, 0, 0, 0], width=0.4) for _ in range(8)]

        with self.canvas:
            # حلقات الرادار
            Color(*PHOSPHOR_GREEN)
            self.circles = [
                Line(circle=(0, 0, 0), width=1.2),
                Line(circle=(0, 0, 0), width=1.2),
                Line(circle=(0, 0, 0), width=1.2),
            ]

            # خطي كروس هير في المنتصف
            Color(PHOSPHOR_GREEN[0], PHOSPHOR_GREEN[1], PHOSPHOR_GREEN[2], 0.8)
            self.cross_h = Line(points=[0, 0, 0, 0], width=1.1)
            self.cross_v = Line(points=[0, 0, 0, 0], width=1.1)

            # شعاع الرادار
            Color(PHOSPHOR_GREEN[0], PHOSPHOR_GREEN[1], PHOSPHOR_GREEN[2], 0.85)
            self.beam_line = Line(points=[0, 0, 0, 0], width=2.0, cap="round")

            # نبضة توسّع للخارج (pulse)
            self.pulse_color = Color(
                PHOSPHOR_GREEN[0], PHOSPHOR_GREEN[1], PHOSPHOR_GREEN[2], 0.22
            )
            self.pulse_circle = Line(circle=(0, 0, 0), width=1.0)

        self.bind(pos=self._update_geometry, size=self._update_geometry)
        Clock.schedule_interval(self.update_beam, 0)

    def _center_and_radius(self):
        w, h = self.width, self.height
        if w <= 0 or h <= 0:
            return 0, 0, 0
        radius = min(w, h) * 0.4
        cx = self.x + w / 2.0
        cy = self.y + h / 2.0
        return cx, cy, radius

    def _update_geometry(self, *args):
        cx, cy, radius = self._center_and_radius()
        if radius <= 0:
            return

        # الحلقات المتداخلة
        for idx, circle in enumerate(self.circles, start=1):
            r = radius * idx / len(self.circles)
            circle.circle = (cx, cy, r)

        # الكروس هير
        left = cx - radius
        right = cx + radius
        bottom = cy - radius
        top = cy + radius
        self.cross_h.points = [left, cy, right, cy]
        self.cross_v.points = [cx, bottom, cx, top]

        # شبكة هاكينج (grid)
        self._update_grid(left, right, bottom, top)

        self._update_beam_geometry()
        self._update_pulse_geometry()

    def _update_grid(self, left, right, bottom, top):
        if not getattr(self, "grid_h_lines", None):
            return

        steps = len(self.grid_h_lines)
        for i, line in enumerate(self.grid_h_lines):
            y = bottom + (top - bottom) * (i / (steps - 1))
            line.points = [left, y, right, y]

        steps = len(self.grid_v_lines)
        for i, line in enumerate(self.grid_v_lines):
            x = left + (right - left) * (i / (steps - 1))
            line.points = [x, bottom, x, top]

    def _update_beam_geometry(self):
        cx, cy, radius = self._center_and_radius()
        if radius <= 0:
            return

        angle_rad = math.radians(self.beam_angle)
        x2 = cx + radius * math.cos(angle_rad)
        y2 = cy + radius * math.sin(angle_rad)

        self.beam_line.points = [cx, cy, x2, y2]

    def _update_pulse_geometry(self):
        cx, cy, radius = self._center_and_radius()
        if radius <= 0:
            return

        pulse_r = radius * (0.25 + 0.6 * self.pulse_phase)
        self.pulse_circle.circle = (cx, cy, pulse_r)

    def update_beam(self, dt):
        self.beam_angle = (self.beam_angle + self.rotation_speed * dt) % 360.0
        self.pulse_phase = (self.pulse_phase + dt * 0.4) % 1.0
        self._update_beam_geometry()
        self._update_pulse_geometry()


class NexusVisionApp(MDApp):
    def build(self):
        Window.clearcolor = (0, 0, 0, 1)

        root = MDBoxLayout(
            orientation="vertical",
            padding=dp(32),
            spacing=dp(24),
        )
        root.md_bg_color = (0, 0, 0, 1)

        radar = RadarWidget(size_hint=(1, 0.8))
        status_label = MDLabel(
            text="[ NEXUS VISION RADAR ]\n[ SEARCHING FOR TARGETS... ]",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.7, 1.0, 0.7, 1),
            font_style="Button",
            markup=False,
        )

        root.add_widget(radar)
        root.add_widget(status_label)

        return root


if __name__ == "__main__":
    NexusVisionApp().run()

