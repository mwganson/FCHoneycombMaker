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
__date__ = "2018.07.04" #year.month.date
__version__ = __date__




import FreeCAD
import math
import Part,Draft,DraftTools
from PySide import QtCore, QtGui
import ProfileLib.RegularPolygon
import Sketcher

RADIUS = 2
SEPARATION = .25 
PLATE_WIDTH = 20
PLATE_LENGTH = 55
PLATE_HEIGHT = 5

DraftTools.msg('\nFCHoneycombMaker v'+__version__+'\n')


def makeHexagonSketch(sketchName):
    #would use the polygon tool, but is buggy and sometimes creates squares instead of hexagons, so the manual way
    sketch = App.ActiveDocument.getObject(sketchName)
#we just place the vertices any old where and then constrain them into place later
    sketch.addGeometry(Part.LineSegment(App.Vector(-2.000000,1.448548,0),App.Vector(0.500515,2.469759,0)),False)
    sketch.addGeometry(Part.LineSegment(App.Vector(0.500515,2.469759,0),App.Vector(2.000000,1.696951,0)),False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
    sketch.addGeometry(Part.LineSegment(App.Vector(2.000000,1.696951,0),App.Vector(2.736140,-0.676675,0)),False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
    sketch.addGeometry(Part.LineSegment(App.Vector(2.736140,-0.676675,0),App.Vector(1.000000,-2.415493,0)),False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
    sketch.addGeometry(Part.LineSegment(App.Vector(1.000000,-2.415493,0),App.Vector(-3.000000,-1.000000,0)),False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1)) 
    sketch.addGeometry(Part.LineSegment(App.Vector(-3.000000,-1.000000,0),App.Vector(-2.000000,1.365748,0)),False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',4,2,5,1)) 
    sketch.addConstraint(Sketcher.Constraint('Coincident',5,2,0,1)) 
    sketch.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0),App.Vector(0,0,1),3.535498),False) #construction circle
    sketch.addConstraint(Sketcher.Constraint('Coincident',6,3,-1,1)) 
    sketch.addConstraint(Sketcher.Constraint('Radius',6,3.535498)) 
    sketch.setDatum(7,App.Units.Quantity('2.000000 mm'))
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',4,2,6)) #constrain all vertices to the circumference
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,1,6)) 
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,2,6)) 
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',1,2,6)) 
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',2,2,6)) 
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',3,2,6)) 
    sketch.toggleConstruction(6) 
    sketch.addConstraint(Sketcher.Constraint('Equal',5,0)) #set all lines equal
    sketch.addConstraint(Sketcher.Constraint('Equal',0,1)) 
    sketch.addConstraint(Sketcher.Constraint('Equal',1,2)) 
    sketch.addConstraint(Sketcher.Constraint('Equal',2,3)) 
    sketch.addConstraint(Sketcher.Constraint('Equal',3,4)) 
    sketch.addConstraint(Sketcher.Constraint('Horizontal',0)) #make one of them horizontal
    sketch.setExpression('Constraints[7]', u'EditMe.radius')





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

If you want to create a border (or have margins) you can resize the plate independently of the honeycomb by adjusting its properties 
in the data tab in the combo view.  To do this you'll need to click the round expression engine icon, and then choose discard, just 
bear in mind this will break the links to the spreadsheet.
"""
set('A13', msg1)


aliases={'radius':'B2', 'separation':'B3', 'width':'B4', 'length':'B5', 'height':'B6', 'tweakX':'B8','tweakY':'B9','tweakZ':'B10',
'xInterval':'E2', 'yInterval':'E3', 'firstX':'E4', 'firstY':'E5','countX':'E6', 'countY':'E7','array2XPos':'E8','array2YPos':'E9',

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
set ('D8', 'Array2 XPos:')
set (aliases['array2XPos'], '=sin(60deg)*(B2*2+B3-0.26794899999999999*B2)')
set ('D9', 'Array2 YPos:')
set (aliases['array2YPos'],'=E3/2')

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
#row2Array.setExpression('Placement.Base.x','sin(60deg) * (EditMe.radius * 2 + (EditMe.separation-0.267949*EditMe.radius))')
row2Array.setExpression('Placement.Base.x','EditMe.array2XPos')
#row2Array.setExpression('Placement.Base.y','EditMe.yInterval/2.0')
row2Array.setExpression('Placement.Base.y','EditMe.array2YPos')
row1Array.setExpression('IntervalX.x','EditMe.xInterval')
row1Array.setExpression('IntervalY.y','EditMe.yInterval')
row1Array.setExpression('NumberX','EditMe.countX')
row1Array.setExpression('NumberY','EditMe.countY')

row2Array.setExpression('IntervalX.x','EditMe.xInterval')
row2Array.setExpression('IntervalY.y','EditMe.yInterval')
row2Array.setExpression('NumberX','EditMe.countX')
row2Array.setExpression('NumberY','EditMe.countY')

#part design stuff
window = QtGui.QApplication.activeWindow()
items=('Add Part Design Compatibility (requires Lattice2 workbench)','Skip Part Design Compatibility')
item,ok = QtGui.QInputDialog.getItem(window, "Part Design Compatibility", "Make this Part Design compatible?\nRequires DeepSOIC's Lattice2 workbench.\nTools -> Addon Manager -> lattice2 -> Install/Update.", items, 0, False)
if ok:
    if item == items[0]:
        docName = App.activeDocument().Label
        try:
            import lattice2LinearArray
            import lattice2Executer
            import lattice2PDPattern
        except:
            msg = QtGui.QMessageBox()
            msg.setWindowTitle('Message from Management')
            msg.setText('You need to install Lattice2 workbench.  Exiting ungracefully...')
            msg.exec_()
            App.ActiveDocument.recompute()
            raise StandardError('Lattice2 not found.')

        App.activeDocument().addObject('PartDesign::Body','plate_body')
        Gui.activeView().setActiveObject('pdbody',App.activeDocument().plate_body)
        App.ActiveDocument.addObject('PartDesign::AdditiveBox','Box')
        App.ActiveDocument.plate_body.addObject(App.activeDocument().Box)
        App.ActiveDocument.Box.setExpression('Length', u'EditMe.length')
        App.ActiveDocument.Box.setExpression('Width', u'EditMe.width')
        App.ActiveDocument.Box.setExpression('Height', u'EditMe.height')

        App.activeDocument().addObject('PartDesign::Body','pd_row1_array')
        App.activeDocument().addObject('PartDesign::Body','pd_row2_array')

        Gui.activeView().setActiveObject('pdbody',App.activeDocument().pd_row1_array)
        App.activeDocument().pd_row1_array.newObject('Sketcher::SketchObject','hexagon_sketch')
        App.activeDocument().hexagon_sketch.Support = (App.activeDocument().XY_Plane001, [''])
        App.activeDocument().hexagon_sketch.MapMode = 'FlatFace'
        makeHexagonSketch('hexagon_sketch')
       
        App.activeDocument().pd_row1_array.newObject("PartDesign::Pad","hex_pad")
        App.activeDocument().hex_pad.Profile = App.activeDocument().hexagon_sketch
        App.ActiveDocument.hex_pad.setExpression('Length', u'EditMe.height')

        Gui.activeView().setActiveObject('pdbody',App.activeDocument().pd_row2_array)
        App.activeDocument().pd_row2_array.newObject('Sketcher::SketchObject','hexagon_sketch2')
        App.activeDocument().hexagon_sketch.Support = (App.activeDocument().XY_Plane001, [''])
        App.activeDocument().hexagon_sketch.MapMode = 'FlatFace'
        makeHexagonSketch('hexagon_sketch2')


        App.activeDocument().pd_row2_array.newObject("PartDesign::Pad","hex_pad2")
        App.activeDocument().hex_pad2.Profile = App.activeDocument().hexagon_sketch2
        App.ActiveDocument.hex_pad2.setExpression('Length', u'EditMe.height')
        App.ActiveDocument.recompute()

        App.ActiveDocument.getObject("pd_row2_array").Placement = App.Placement(App.Vector(3.22,0,0),App.Rotation(App.Vector(0,0,1),0))
        App.ActiveDocument.pd_row2_array.setExpression('Placement.Base.x', u'EditMe.array2XPos')
        App.ActiveDocument.getObject("pd_row2_array").Placement = App.Placement(App.Vector(3.22,0,0),App.Rotation(App.Vector(0,0,1),0))
        App.ActiveDocument.getObject("pd_row2_array").Placement = App.Placement(App.Vector(3.21651,1.86,0),App.Rotation(App.Vector(0,0,1),0))
        App.ActiveDocument.pd_row2_array.setExpression('Placement.Base.y', u'EditMe.array2YPos')

        Gui.ActiveDocument.getObject("hexagon_sketch2").Visibility=False
        Gui.ActiveDocument.getObject("hexagon_sketch").Visibility=False
        Gui.activeView().setActiveObject('pdbody',App.activeDocument().pd_row2_array)
        f = lattice2LinearArray.makeLinearArray(name='LinearArray')
        f.Link = App.ActiveDocument.Box
        f.LinkSubelement = 'Edge9'
        f.GeneratorMode = 'StepN'
        lattice2Executer.executeFeature(f)
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(f)
        App.ActiveDocument.LinearArray.setExpression('Count', u'EditMe.countX+1')
        App.ActiveDocument.LinearArray.setExpression('Step', u'EditMe.xInterval')
        App.activeDocument().recompute()
        f = lattice2PDPattern.makeFeature()
        f.FeaturesToCopy = [App.ActiveDocument.hex_pad2]
        f.PlacementsTo = App.ActiveDocument.LinearArray
        f.Referencing = 'First item'
        lattice2Executer.executeFeature(f)
        f.PlacementsTo.ViewObject.hide()
        f.BaseFeature.ViewObject.hide()
        Gui.Selection.addSelection(f)

        Gui.ActiveDocument.ActiveView.setActiveObject('pdbody', App.ActiveDocument.getObject('pd_row1_array'))
        Gui.activateWorkbench("Lattice2Workbench")
        import PartDesignGui
        f = lattice2LinearArray.makeLinearArray(name='LinearArray')
        f.Link = App.ActiveDocument.Box
        f.LinkSubelement = 'Edge9'
        f.GeneratorMode = 'StepN'
        lattice2Executer.executeFeature(f)
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(f)
        App.ActiveDocument.LinearArray001.setExpression('Step', u'EditMe.xInterval')
        App.ActiveDocument.LinearArray001.setExpression('Count', u'EditMe.countX+1')
        App.activeDocument().recompute()
        f = lattice2PDPattern.makeFeature()
        f.FeaturesToCopy = [App.ActiveDocument.hex_pad]
        f.PlacementsTo = App.ActiveDocument.LinearArray001
        f.Referencing = 'First item'
        lattice2Executer.executeFeature(f)
        f.PlacementsTo.ViewObject.hide()
        f.BaseFeature.ViewObject.hide()
        Gui.Selection.addSelection(f)
        f = None

        f = lattice2LinearArray.makeLinearArray(name='LinearArray')
        f.Link = App.ActiveDocument.Box
        f.LinkSubelement = 'Edge2'
        f.GeneratorMode = 'StepN'
        lattice2Executer.executeFeature(f)
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(f)
        App.ActiveDocument.LinearArray002.setExpression('Count', u'EditMe.countY+1')
        App.ActiveDocument.LinearArray002.setExpression('Step', u'EditMe.yInterval')
        App.activeDocument().recompute()
        f = lattice2PDPattern.makeFeature()
        f.FeaturesToCopy = [App.ActiveDocument.LatticePattern001]
        f.PlacementsTo = App.ActiveDocument.LinearArray002
        f.Referencing = 'First item'
        lattice2Executer.executeFeature(f)
        f.PlacementsTo.ViewObject.hide()
        f.BaseFeature.ViewObject.hide()
        Gui.Selection.addSelection(f)
        f = None
        Gui.activateWorkbench('PartDesignWorkbench')
        Gui.ActiveDocument.ActiveView.setActiveObject('pdbody', App.ActiveDocument.getObject('pd_row2_array'))
        Gui.activateWorkbench("Lattice2Workbench")
        import PartDesignGui
        f = lattice2LinearArray.makeLinearArray(name='LinearArray')
        f.Link = App.ActiveDocument.Box
        f.LinkSubelement = 'Edge2'
        f.GeneratorMode = 'StepN'
        lattice2Executer.executeFeature(f)
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(f)
        App.ActiveDocument.LinearArray003.setExpression('Step', u'EditMe.yInterval')
        App.ActiveDocument.LinearArray003.setExpression('Count', u'EditMe.countY+1')
        App.activeDocument().recompute()
        f = lattice2PDPattern.makeFeature()
        f.FeaturesToCopy = [App.ActiveDocument.LatticePattern]
        f.PlacementsTo = App.ActiveDocument.LinearArray003
        f.Referencing = 'First item'
        lattice2Executer.executeFeature(f)
        f.PlacementsTo.ViewObject.hide()
        f.BaseFeature.ViewObject.hide()
        Gui.Selection.addSelection(f)


        App.ActiveDocument.plate_body.setExpression('Placement.Base.x', u'EditMe.tweakX')
        App.ActiveDocument.plate_body.setExpression('Placement.Base.y', u'EditMe.tweakY')
        App.ActiveDocument.plate_body.setExpression('Placement.Base.z', u'EditMe.tweakZ')
        App.ActiveDocument.pd_row1_array.setExpression('Placement.Base.x', u'EditMe.tweakX')
        App.ActiveDocument.pd_row1_array.setExpression('Placement.Base.y', u'EditMe.tweakY')
        App.ActiveDocument.pd_row1_array.setExpression('Placement.Base.z', u'EditMe.tweakZ')
        App.ActiveDocument.pd_row2_array.setExpression('Placement.Base.x', u'EditMe.array2XPos + EditMe.tweakX')
        App.ActiveDocument.pd_row2_array.setExpression('Placement.Base.y', u'EditMe.array2YPos + EditMe.tweakY')
        App.ActiveDocument.pd_row2_array.setExpression('Placement.Base.z', u'EditMe.tweakZ')

        #uncomment these if you just want to make the part/draft objects invisible
        #App.ActiveDocument.getObject('Plate').Visibility=False
        #App.ActiveDocument.getObject("HoneyCombRow2Array").Visibility=False
        #App.ActiveDocument.getObject("HoneyCombRow1Array").Visibility=False

        #and comment these to keep them from getting removed
        App.ActiveDocument.removeObject('Plate')
        App.ActiveDocument.removeObject("HoneyCombRow2Array")
        App.ActiveDocument.removeObject("HoneyCombRow1Array")
        App.ActiveDocument.removeObject("ExtrudedHexagon")
        App.ActiveDocument.removeObject("Hexagon")


App.ActiveDocument.recompute()


