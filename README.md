# FCHoneycombMaker
Aids in laying out rectangular array of hexagons to form a honeycomb grid.

When you execute the macro it creates a spreadsheet called "EditMe", a 6-sized regular polygon, which gets extruded into a prism, 2 rectangular areas of said hexagons, and a "plate", which is just a resized cube.

<img src="honeycombmaker-screenshot1.png" alt="screenshot1">

Modify the values in the spreadsheet to customize the honeycomb:

<img src="honeycombmaker-screenshot2.png" alt="screenshot2">

These are the same instructions found in the spreadsheet:

Instructions:

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
