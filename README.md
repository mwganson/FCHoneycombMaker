# FCHoneycombMaker


Creates a parametric honeycomb grid.

## New version: 2019.07.04

I've made some major changes.  No longer is any additional workbench required. <br/>
<br/>
When you execute the macro it creates a spreadsheet called "EditMe", which is what should be edited if you want to change the parameters of the Honeycomb grid.  An option is presented to the user whether to create a Part Design workbench body or a Part Workbench object.<br/>
<br/>
If you choose Part Workbench object you will get an object called "HoneycombGrid", which is a Part::Cut object created by cutting a fusion of 2 arrays of extruded hexagons out of a Part::Cube object.  This object is fully parametric.  Just make your changes in the EditMe spreadsheet.<br/>
<br/>
<img src="honeycombmaker-screenshot1.png" alt="screenshot1"><br/>
<br/>
If you choose a Part Design body you will get a new Body object called "HoneycombBody".  There will also be a hidden object called "BaseFeatureFace".  Do not delete this object.  It is the object used for the BaseFeature in the new body.  The Pad in the new body is called HoneycombPad.  It is a pad of one of the BaseFeature's faces, rather than the pad of a sketch.  It would not be parametric if I had made a sketch and padded it.  If you would like a sketch you can make one in the Draft workbench.  Select the "BaseFeatureFace" object, then in Draft menu select Draft to Sketch.  The sketch will only be partially constrained and will have a great many degrees of freedom, but should be editable and able to be used in Pad or Pocket operations.<br/>
<br/>
<img src="honeycombmaker-pd-screenshot.png" alt="pd-screenshot">

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



If you'd prefer a different shape as the base you could easily swap out the extruded hexagon with a sphere or, as I did in the image below, an ellipsoid shaped somewhat like an egg.  Could be used to create egg crate designs.

<img src="honeycombmaker-screenshot8.png" alt="screenshot8">

All you need to do to make that change is to change the Base property in the 2 arrays from extruded hexagon to the new object.  The hexagon is linked (its radius) to the spreadsheet, and the extruded hexagon is also linked (its length forward), so you might want to hook those links with the new object if you want its relevant properties updated when you change values in the spreadsheet.  Just click the expression engine icon in the property (combo view, data tab) and enter EditMe.height, EditMe.radius, or whichever value you want to link with for that property of that object.

Because we use draft array objects for the arrays, these can also be easily extended into the z direction if you want to, for example, to create a hollowed out interior.  Just set the ZNumber property in both arrays to the desired number.  You can also link the ZInterval to the spreadsheet using EditMe.xInterval or EditMe.yInterval or something like EditMe.height+EditMe.separation.

<img src="honeycombmaker-screenshot9.png" alt="screenshot9">

For more z direction modifications, look at how I set the placement offset for array2 relative to array1, and perhaps employ something similar for the z direction offsets:

<img src="honeycombmaker-screenshot10.png" alt="screenshot10">


<img src="honeycombmaker-screenshot10.png" alt="screenshot10">
