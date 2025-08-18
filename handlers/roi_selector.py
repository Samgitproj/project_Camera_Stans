# handlers/roi_selector.py

# [SECTION: IMPORTS]
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple

from PyQt6 import QtCore, QtGui, QtWidgets


# [END: SECTION: IMPORTS]
# [END: Imports]
# [CLASS: Roi]
# [SECTION: CLASS: Roi]
@dataclass
class Roi:
    x: int
    y: int
    w: int
    h: int

# [END: SECTION: CLASS: Roi]
# [END: Roi]

# [CLASS: RoiSelector]
# [SECTION: CLASS: RoiSelector]
class RoiSelector(QtCore.QObject):
    """
    Eenvoudig ROI-tekenhulpmiddel op een QLabel met KeepAspectRatio rendering.
    Verwacht een callback die label->image coördinaten kan mappen:
      map_fn(qpoint: QtCore.QPoint) -> (ix, iy) in int of None als buiten beeld.
    """

    roiChanged = QtCore.pyqtSignal(object)  # Roi | None

# [FUNC: __init__]
    def __init__(self, label: QtWidgets.QLabel, map_label_to_image_fn):
        super().__init__(label)
        self._label = label
        self._map = map_label_to_image_fn
        self._active = False
        self._dragging = False
        self._p0_label: Optional[QtCore.QPoint] = None
        self._p1_label: Optional[QtCore.QPoint] = None
        self._roi_img: Optional[Roi] = None

        self._label.installEventFilter(self)

# [END: FUNC: __init__]
# [END: __init__]
# [FUNC: setActive]
    def setActive(self, on: bool) -> None:
        self._active = on
        self._dragging = False
        self._p0_label = None
        self._p1_label = None
        self._label.update()

# [END: FUNC: setActive]
# [END: setActive]
# [FUNC: clear]
    def clear(self) -> None:
        self._roi_img = None
        self._label.update()
        self.roiChanged.emit(None)

# [END: FUNC: clear]
# [END: clear]
# [FUNC: roi]
    def roi(self) -> Optional[Roi]:
        return self._roi_img

# [END: FUNC: roi]
# [END: roi]
# [FUNC: eventFilter]
    def eventFilter(self, obj, ev):
        if obj is self._label and self._active:
            et = ev.type()
            if (
                et == QtCore.QEvent.Type.MouseButtonPress
                and ev.buttons() & QtCore.Qt.MouseButton.LeftButton
            ):
                self._dragging = True
                self._p0_label = ev.position().toPoint()
                self._p1_label = self._p0_label
                self._label.update()
                return True
            elif et == QtCore.QEvent.Type.MouseMove and self._dragging:
                self._p1_label = ev.position().toPoint()
                self._label.update()
                return True
            elif et == QtCore.QEvent.Type.MouseButtonRelease and self._dragging:
                self._p1_label = ev.position().toPoint()
                self._dragging = False
                roi = self._build_roi()
                self._roi_img = roi
                self._label.update()
                self.roiChanged.emit(roi)
                return True
            elif et == QtCore.QEvent.Type.Paint:
                self._paint_overlay()
                return False
        return super().eventFilter(obj, ev)

# [END: FUNC: eventFilter]
# [END: eventFilter]
# [FUNC: _build_roi]
    def _build_roi(self) -> Optional[Roi]:
        if self._p0_label is None or self._p1_label is None:
            return None
        p0 = self._p0_label
        p1 = self._p1_label
        # Map beide punten naar image coords
        m0 = self._map(p0)
        m1 = self._map(p1)
        if m0 is None or m1 is None:
            return None
        x0, y0 = m0
        x1, y1 = m1
        x = min(x0, x1)
        y = min(y0, y1)
        w = abs(x1 - x0)
        h = abs(y1 - y0)
        if w <= 0 or h <= 0:
            return None
        return Roi(x=x, y=y, w=w, h=h)

# [END: FUNC: _build_roi]
# [END: _build_roi]
# [FUNC: _paint_overlay]
    def _paint_overlay(self) -> None:
        # Teken rechthoek in label-coords tijdens drag
        if self._label.pixmap() is None:
            return
        painter = QtGui.QPainter(self._label)
        pen = QtGui.QPen(QtGui.QColor(255, 0, 0), 2, QtCore.Qt.PenStyle.DashLine)
        painter.setPen(pen)
        if self._active and self._p0_label and self._p1_label:
            r = QtCore.QRect(self._p0_label, self._p1_label).normalized()
            painter.drawRect(r)
        # Teken bestaande ROI in label-coords (door image->label mapping inverse te benaderen via corners)
        if self._roi_img:
            # we projecteren vier hoeken naar label approx via inverse van map (lineair schalen rond content)
            # De map-functie is enkel label->image; we schatten label-rect uit image-size in de renderende widget.
            # De buitenste controller tekent meestal ook overlay, dus dit is optioneel.
            pass
        painter.end()
# [END: RoiSelector]
# [END: FUNC: _paint_overlay]
# [END: SECTION: CLASS: RoiSelector]
# [END: _paint_overlay]
