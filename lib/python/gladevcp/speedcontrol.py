#!/usr/bin/env python

# GladeVcp Widget 
# JogWheel widget, to simulate a real jogwheel
# mostly to be used in a sim config
#
#
# Copyright (c) 2013 Norbert Schechner
# based on the pyvcp jogwheel widget from Anders Wallin
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import gtk
import gobject
from math import pi

# This is needed to make the hal pin, making them directly with hal, will
# not allow to use them in glade without linuxcnc beeing started
from hal_widgets import _HalSpeedControlBase

class SpeedControl(gtk.VBox, _HalSpeedControlBase):
    '''
    Here goes the description of the widget

    '''

    __gtype_name__ = 'SpeedControl'
    __gproperties__ = {
        'height'  : ( gobject.TYPE_INT, 'The height of the widget in pixel', 'Set the height of the widget',
                    24, 96, 36, gobject.PARAM_READWRITE|gobject.PARAM_CONSTRUCT),
        'value' : (gobject.TYPE_FLOAT, 'Value', 'The  value to set',
                    0.001, 99999.0, 10.0, gobject.PARAM_READWRITE | gobject.PARAM_CONSTRUCT),
        'min' : (gobject.TYPE_FLOAT, 'Min Value', 'The min allowed value to apply',
                    0.0, 99999.0, 0.0, gobject.PARAM_READWRITE | gobject.PARAM_CONSTRUCT),
        'max' : (gobject.TYPE_FLOAT, 'Max Value', 'The max allowed value to apply',
                    0.001, 99999.0, 100.0, gobject.PARAM_READWRITE | gobject.PARAM_CONSTRUCT),
        'increment' : (gobject.TYPE_FLOAT, 'Increment Value', 'The incrementvalue to apply',
                    0.001, 99999.0, 5.0, gobject.PARAM_READWRITE | gobject.PARAM_CONSTRUCT),
        'inc_speed'  : ( gobject.TYPE_INT, 'The speed of the increments', 'Set the timer delay for the increment speed',
                    20, 300, 100, gobject.PARAM_READWRITE|gobject.PARAM_CONSTRUCT),
        'unit' : ( gobject.TYPE_STRING, 'unit', 'Sets the unit to be shown in the bar after the value',
                    "", gobject.PARAM_READWRITE | gobject.PARAM_CONSTRUCT),
        'color' : (gtk.gdk.Color.__gtype__, 'color', 'Sets the color of the bar',
                        gobject.PARAM_READWRITE),
        'template' : (gobject.TYPE_STRING, 'Text template for bar value',
                'Text template to display. Python formatting may be used for one variable',
                "%.1f", gobject.PARAM_READWRITE | gobject.PARAM_CONSTRUCT),
                      }
    __gproperties = __gproperties__

    __gsignals__ = {
                    'value_changed': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_FLOAT,)),
#                    'min_reached': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_BOOLEAN,)),
#                    'max_reached': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_BOOLEAN,)),
                    'exit': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ()),
                   }

    def __init__(self, size = 36, value = 0, min = 0, max = 100, increment = 5, inc_speed = 100, unit = "%", color = "#FF00FF", template = "%.1f"):
        super(SpeedControl, self).__init__()

        # basic settings
        self._size = size
        self._value = value
        self._min = min
        self._max = max
        self.color = gtk.gdk.Color(color)
        # print("color = ", color)
        # print("Converted = ",self.color)
        self._unit = unit
        self._increment = increment
        self._template = template
        self._speed = inc_speed

        # print(size, value, min, max, increment, unit, color, template)

        self.adjustment = gtk.Adjustment(self._value, self._min, self._max, self._increment, 0)
        self.adjustment.connect("value_changed", self.on_value_changed)

        self.btn_plus = gtk.Button("+")
        self.btn_plus.connect("pressed", self.on_btn_plus_pressed)
        self.btn_plus.connect("released", self.on_btn_plus_released)
        self.btn_minus = gtk.Button("-")
        self.btn_minus.connect("pressed", self.on_btn_minus_pressed)
        self.btn_minus.connect("released", self.on_btn_minus_released)
        
        #self.btn_debug = gtk.Button("debug")
        #self.btn_debug.connect("pressed", self.on_btn_debug_pressed)

        self.draw = gtk.DrawingArea()
        self.draw.connect("expose-event", self.expose)
#        self.connect("min_reached", self._min_limit)
#        self.connect("max_reached", self._max_limit)

        self.table = gtk.Table(rows=2,columns=5)
        self.table.attach( self.btn_minus, 0, 1, 0, 1, gtk.SHRINK, gtk.SHRINK )
        self.table.attach( self.draw, 1, 4, 0, 1, gtk.FILL|gtk.EXPAND, gtk.EXPAND )
        self.table.attach( self.btn_plus, 4, 5, 0, 1, gtk.SHRINK, gtk.SHRINK )

        # self.table.attach( self.btn_debug, 1, 4, 1, 2, gtk.SHRINK, gtk.SHRINK )

        self.add(self.table)
        self.show_all()
        self.connect("destroy", gtk.main_quit)

        self._update_widget()

    def _update_widget(self):
        self.btn_plus.set_size_request(self._size,self._size)
        self.btn_minus.set_size_request(self._size,self._size)

    # this draws our widget on the screen
    def expose(self, widget, event):
        # create the cairo window
        # I do not know why this works without importing cairo
        self.cr = widget.window.cairo_create()

        # call to paint the widget
        self._draw_widget()

    # draws the frame, meaning the background
    def _draw_widget(self):
        w = self.draw.allocation.width

        # draw a rectangle with rounded edges and a black frame
        linewith = self._size / 24
        if linewith < 1:
            linewith = 1
        radius = self._size / 7.5
        if radius < 1:
            radius = 1

        # fill the rectangle with selected color
        # first get the width of the area to fill
        percentage = (self._value - self._min) * 100 / (self._max - self._min)
        width_to_fill = w * percentage / 100
        r, g, b = self.get_color_tuple(self.color)
        self.cr.set_source_rgb(r, g, b)

        # get the middle points of the corner radius
        tl = [radius, radius]                               # Top Left
        tr = [width_to_fill - radius, radius]               # Top Right
        br = [width_to_fill - radius, self._size - radius]  # Bottom Left
        bl = [radius, self._size - radius]                  # Bottom Right

        # could be written shorter, but this way it is easier to understand
        self.cr.arc(tl[0], tl[1], radius, 2 * (pi/2), 3 * (pi/2))
        self.cr.arc(tr[0], tr[1], radius, 3 * (pi/2), 4 * (pi/2))
        self.cr.arc(br[0], br[1], radius, 0 * (pi/2), 1 * (pi/2))
        self.cr.arc(bl[0], bl[1], radius, 1 * (pi/2), 2 * (pi/2))
        self.cr.close_path()
        self.cr.fill()

        self.cr.set_line_width(linewith)
        self.cr.set_source_rgb(0, 0, 0)
        
        # get the middle points of the corner radius
        tl = [radius, radius]                   # Top Left
        tr = [w - radius, radius]               # Top Right
        bl = [w - radius, self._size - radius]  # Bottom Left
        br = [radius, self._size - radius]      # Bottom Right
        
        # could be written shorter, but this way it is easier to understand
        self.cr.arc(tl[0], tl[1], radius, 2 * (pi/2), 3 * (pi/2))
        self.cr.arc(tr[0], tr[1], radius, 3 * (pi/2), 4 * (pi/2))
        self.cr.arc(bl[0], bl[1], radius, 0 * (pi/2), 1 * (pi/2))
        self.cr.arc(br[0], br[1], radius, 1 * (pi/2), 2 * (pi/2))
        self.cr.close_path()

        # draw the label in the bar
        self.cr.set_source_rgb(0 ,0 ,0)
        self.cr.set_font_size(self._size / 3)

        tmpl = lambda s: self._template % s
        label = tmpl(self._value)
        if self._unit:
            label += " " + self._unit

        w,h = self.cr.text_extents(label)[2:4]
        self.draw.set_size_request(int(w) + int(h), self._size)
        left = self.draw.allocation.width /2
        top = self._size / 2
        self.cr.move_to(left - w / 2 , top + h / 2)
        self.cr.show_text(label)
        self.cr.stroke()

    # This allows to set the value from external, i.e. propertys
    def set_value(self, value):
        self.adjustment.set_value(value)
        self.queue_draw()

    # Will return the value to external call
    # so it will do also to hal_widget_base
    def get_value(self):
        return self._value

    def on_value_changed(self, widget):
        value = widget.get_value()
        self.emit("value_changed", value)
        # if the value does change from outside, i.e. changing the adjustment 
        # we are not 
        if value != self._value:
            self._value = value
            self.set_value(self._value)

    def on_btn_plus_pressed(self, widget):
        self.timer_id = gobject.timeout_add(self._speed, self.increase)

    def on_btn_plus_released(self, widget):
        gobject.source_remove(self.timer_id)
        
    def increase(self):
        value = self.adjustment.get_value()
        value += self._increment
        if value > self._max:
            value = self._max
            self.btn_plus.set_sensitive(False)
            self.set_value(value)
            return False
        elif not self.btn_minus.get_sensitive():
            self.btn_minus.set_sensitive(True)
        self.set_value(value)
        return True

    def on_btn_minus_pressed(self,widget):
        self.timer_id = gobject.timeout_add(self._speed, self.decrease)

    def on_btn_minus_released(self,widget):
        gobject.source_remove(self.timer_id)

    def decrease(self):
        value = self.adjustment.get_value()
        value -= self._increment
        if value < self._min:
            value = self._min
            self.btn_minus.set_sensitive(False)
            self.set_value(value)
            return False
        elif not self.btn_plus.get_sensitive():
            self.btn_plus.set_sensitive(True)
        self.set_value(value)
        return True

#    def on_btn_debug_pressed(self,widget):
#        col = self.get_property("color")
#        print("Got Property",col)

    # returns the separate RGB color numbers from the color widget
    def _convert_to_rgb(self, spec):
        color = spec.to_string()
        temp = color.strip("#")
        r = temp[0:4]
        g = temp[4:8]
        b = temp[8:]
        return (int(r, 16), int(g, 16), int(b, 16))

    def get_color_tuple(gtk_color,c):
        return (c.red_float, c.green_float, c.blue_float)

    def set_digits(self, digits):
        if int(digits) > 0:
            self._template = "%.{0}f".format(int(digits))
        else:
            self._template = "%d"

    def set_adjustment(self, adjustment):
        self.adjustment = adjustment
        self.adjustment.connect("value_changed", self.on_value_changed)
        self._min = self.adjustment.get_lower()
        self._max = self.adjustment.get_upper()
        self.adjustment.set_page_size(adjustment.get_page_size())
        self._value = self.adjustment.get_value()
        self.set_value(self._value)    
        
    # Get properties
    def do_get_property(self, property):
        name = property.name.replace('-', '_')
        if name in self.__gproperties.keys():
            if name == 'color':
                col = getattr(self, name)
                colorstring = col.to_string()
                print("col = ",col)
                print("colorstring = ",colorstring)
                return getattr(self, name)
            return getattr(self, name)
        else:
            raise AttributeError('unknown property %s' % property.name)

    # Set properties
    def do_set_property(self, property, value):
        try:
            name = property.name.replace('-', '_')
            if name in self.__gproperties.keys():
                setattr(self, name, value)
                if name == "height":
                    self._size = value
                    self._update_widget()
                if name == "value":
                    self.set_value(value)
                if name == "min":
                    self._min = value
                    self.adjustment.lower = value
                if name == "max":
                    self._max = value
                    self.adjustment.upper = value
                if name == "increment":
                    self._increment = value
                if name == "inc_speed":
                    self._speed = value
                if name == "unit":
                    self._unit = value
                if name == "color":
                    self.color = value
                    print("New Color with property = ", self.color)
                if name == "template":
                    self._template = value
                self._draw_widget()
            else:
                raise AttributeError('unknown property %s' % property.name)
        except:
            pass

# for testing without glade editor:
# to show some behavior and setting options  

def main():
    window = gtk.Window()
    speedcontrol = SpeedControl()
    window.add(speedcontrol)
    window.set_title("Button Speed Control")
    window.set_position(gtk.WIN_POS_CENTER)
    window.show_all()
    speedcontrol.set_property("height", 48)
    speedcontrol.set_property("unit", "mm/min")
    speedcontrol.set_property("color", gtk.gdk.Color("#FF8116"))
    speedcontrol.set_property("min", 0)
    speedcontrol.set_property("max", 15000)
    speedcontrol.set_property("increment", 250.123)
    speedcontrol.set_property("inc_speed", 100)
    speedcontrol.set_property("value", 10000)
    speedcontrol.set_property("template", "%.3f")
    #speedcontrol.set_digits(1)

    gtk.main()

if __name__ == "__main__":
    main()