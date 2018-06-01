# -*- coding: utf-8 -*-
"""
***************************************************************************
*   Copyright (c) 2018 <TheMarkster>                                      *
*                                                                         *
*   This file is a supplement to the FreeCAD CAx development system.      *
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU Lesser General Public License (LGPL)    *
*   as published by the Free Software Foundation; either version 2 of     *
*   the License, or (at your option) any later version.                   *
*                                                                         *
*   This software is distributed in the hope that it will be useful,      *
*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
*   GNU Library General Public License at http://www.gnu.org/licenses     *
*   for more details.                                                     *
*                                                                         *
*   For more information about the GNU Library General Public License     *
*   write to the Free Software Foundation, Inc., 59 Temple Place,         *
*   Suite 330, Boston, MA  02111-1307 USA                                 *
*                                                                         *
***************************************************************************
"""

#OS: Windows 10
#Word size of OS: 64-bit
#Word size of FreeCAD: 64-bit
#Version: 0.17.13519 (Git)
#Build type: Release
#Branch: releases/FreeCAD-0-17
#Hash: 1a8b868018f45ea486c0023fdbfeb06febc1fb89
#Python version: 2.7.14
#Qt version: 4.8.7
#Coin version: 4.0.0a
#OCC version: 7.2.0
#Locale: English/UnitedStates (en_US)


"""
FCHoneycombMaker

This is a macro to aid in creation of 2 rectangular arrays of hexagons laid out in a honeycomb pattern.  Parameters,
including hexagon radius, separation between hexagons, etc., can be modified via an included spreadsheet.
"""

__title__ = "FCHoneycombMaker"
__author__ = "TheMarkster"
__url__ = "https://github.com/mwganson/FCHoneycombMaker"
__Wiki__ = "https://github.com/mwganson/FCHoneycombMaker/blob/master/README.md"
__date__ = "2018.06.01" #year.month.date
__version__ = __date__




import FreeCAD
import math
import Part,Draft
from PySide import QtCore, QtGui

RADIUS = 2
SEPARATION = .25 
PLATE_WIDTH = 20
PLATE_LENGTH = 55
PLATE_HEIGHT = 5



if not App.ActiveDocument:
    App.newDocument()
worksheet = App.ActiveDocument.addObject("Spreadsheet::Sheet", "EditMe")
worksheet.setColumnWidth('A',150)
set = worksheet.set

worksheet.mergeCells('A11:G25')
msg1 = """Instructions:

You should only run the macro once unless you want to start again from scratch.

Edit the values in column B to define your honeycomb.  You can also edit the objects (plate, arrays, etc.), but it's 
probably better to do all the editing here in the spreadsheet at least until you get it more or less like you want it before
doing some final tweaking directly on the objects.

Hexagon radius -- the circumradius of the individual hexagons (circle with each vertex on its circumference).

Hexagon separation -- distance between each hexagon, the thickness of the grid produced after cutting the hexagons from the plate.

Plate dimensions -- sets the dimensions of the plate out of which the honeycomb can be cut.  These values are used to calculate
the countX and countY variables.  You can delete the plate object if you wish to apply the hexagon arrays to a different structure.

Tweak X,Y,Z -- Edit these to move both hexagon arrays independently of the plate object, for example to center the arrays inside 
the plate.

CountX and CountY -- number of hexagons in the 2 arrays.  These are calculated based on the plate size, radius of hexagons, and 
separation between them, but you will probably want to modify these manually.  Just remember if you modify them you are replacing 
the formulas in those cells with immediate values, and thus they won't be recalulated for you if other changes are made.

If you would prefer a round plate, simply delete the plate object and replace it with a cylinder, and then use the Tweak values 
and countX and countY variables to arrange the hexagon arrays to your liking.

The final step in the process is to fuse the arrays together, and then cut them out of the plate.

If you want to create a border (or have margins) you can resize the plate independtly of the honeycomb by adjusting its properties 
in the data tab in the combo view.  To do this you'll need to click the round expression engine icon, and then choose discard, just 
bear in mind this will break the links to the spreadsheet.
"""
set('A13', msg1)


aliases={'radius':'B2', 'separation':'B3', 'width':'B4', 'length':'B5', 'height':'B6', 'tweakX':'B8','tweakY':'B9','tweakZ':'B10',
'xInterval':'E2', 'yInterval':'E3', 'firstX':'E4', 'firstY':'E5','countX':'E6', 'countY':'E7'

 }

for k,v in aliases.items():
   worksheet.setAlias(v,k)



set('A1', 'User Variables')
set('D1','Calculated Values')
set('A2', 'Hexagon Radius:')
set(aliases['radius'], str(RADIUS))
set('A3', 'Hexagon Separation:')
set(aliases['separation'], str(SEPARATION))
set('A4', 'Plate Width:')
set(aliases['width'], str(PLATE_WIDTH))
set('A5', 'Plate Length:')
set(aliases['length'], str(PLATE_LENGTH))
set('A6', 'Plate Height:')
set(aliases['height'], str(PLATE_HEIGHT))
set('A8', 'Tweak X:')
set(aliases['tweakX'],u'0')
set('A9', 'Tweak Y:')
set(aliases['tweakY'],u'0')
set('A10', 'Tweak Z:')
set(aliases['tweakZ'],u'0')




set('D2','X Interval:')
set(aliases['xInterval'],'=2*sin(60deg)*(B2*2+(B3-0.267949*B2))')
set('D3', 'Y Interval:')
set(aliases['yInterval'], '=2*B2+(B3-0.267949*B2)' )
set('D4', 'First X:')
set(aliases['firstX'], '=B2')
set('D5', 'First Y:')
set(aliases['firstY'], '=B2')
set('D6', 'Count X:')
set(aliases['countX'], '=round((B5) / E2)')
set('D7', 'Count Y:')
set(aliases['countY'], '=round((B4) / E3)')


#plate = Part.makeBox(PLATE_WIDTH,PLATE_LENGTH,PLATE_HEIGHT)
#plate = Part.makeBox(worksheet.B4, worksheet.B5, worksheet.B6)
App.ActiveDocument.addObject("Part::Box", "Plate")
plateObject = App.ActiveDocument.getObject("Plate")
App.ActiveDocument.Plate.setExpression('Length', u'EditMe.length')
App.ActiveDocument.Plate.setExpression('Width', u'EditMe.width')
App.ActiveDocument.Plate.setExpression('Height', u'EditMe.height')

#xInterval = float(worksheet.getContents(aliases['xInterval']))
xInterval = 2*math.sin(math.pi/180.0*60)*(RADIUS*2+(SEPARATION-0.267949))
yInterval = 2*RADIUS+(SEPARATION-0.267949)
#yInterval = float(worksheet.getContents(aliases['yInterval']))
firstX = RADIUS
firstY = RADIUS

countY = int((PLATE_LENGTH) / yInterval)
countX = int((PLATE_WIDTH) / xInterval)




App.ActiveDocument.addObject("Part::RegularPolygon","Hexagon")
App.ActiveDocument.Hexagon.Polygon=6
App.ActiveDocument.Hexagon.setExpression('Circumradius','EditMe.radius')
hexagonObject = App.ActiveDocument.getObject("Hexagon")
Gui.ActiveDocument.getObject("Hexagon").Visibility=False


extrudedHexagonObject = App.ActiveDocument.addObject('Part::Extrusion', 'ExtrudedHexagon')
extrudedHexagonObject.Base = hexagonObject
extrudedHexagonObject.setExpression('LengthFwd','EditMe.height')
extrudedHexagonObject.Solid=True
#extrudedHexagonObject.Placement=App.Placement(App.Vector(firstX,firstY,0),App.Rotation(0,0,0),App.Vector(0,0,0))
extrudedHexagonObject.setExpression('Placement.Base.x','EditMe.firstX+EditMe.tweakX')
extrudedHexagonObject.setExpression('Placement.Base.y','EditMe.firstY+EditMe.tweakY')
extrudedHexagonObject.setExpression('Placement.Base.z', 'EditMe.tweakZ')

xvector = App.Vector(xInterval,0,0)
yvector = App.Vector(0, yInterval,0)
row1Array = Draft.makeArray(extrudedHexagonObject, xvector,yvector,countX,countY,"HoneyCombRow1Array")
row2Array = Draft.makeArray(extrudedHexagonObject, xvector,yvector,countX,countY,"HoneyCombRow2Array")
row2Array.Placement = App.Placement(App.Vector(math.sin(60*math.pi/180.0)*(RADIUS*2+(SEPARATION-0.267949)),yInterval,0),App.Rotation(0,0,0),App.Vector(0,0,0))
row2Array.setExpression('Placement.Base.x','sin(60deg) * (EditMe.radius * 2 + (EditMe.separation-0.267949*EditMe.radius))')

row2Array.setExpression('Placement.Base.y','EditMe.yInterval/2.0')
row1Array.setExpression('IntervalX.x','EditMe.xInterval')
row1Array.setExpression('IntervalY.y','EditMe.yInterval')
row1Array.setExpression('NumberX','EditMe.countX')
row1Array.setExpression('NumberY','EditMe.countY')

row2Array.setExpression('IntervalX.x','EditMe.xInterval')
row2Array.setExpression('IntervalY.y','EditMe.yInterval')
row2Array.setExpression('NumberX','EditMe.countX')
row2Array.setExpression('NumberY','EditMe.countY')

App.ActiveDocument.recompute()