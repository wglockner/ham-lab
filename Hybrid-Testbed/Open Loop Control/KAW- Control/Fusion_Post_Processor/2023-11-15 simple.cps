/**
  Copyright (C) 2012-2021 by Autodesk, Inc.
  All rights reserved.

  Export to simple list post processor configuration.
  CURRENTLY ONLY CONFIGURED FOR ADDITIVE FFF

  $Revision: 43470 147f5cf60e9217cf9c3365dc511a0f631d89bb16 $
  $Date: 2021-10-13 20:53:32 $

  FORKID {A110AA28-D6B1-4fbb-B598-EAB9866DA91A}
*/

description = "Export toolpath to Kawasaki AS Language";
vendor = "JDH";
vendorUrl = "imse.iastate.edu";
legal = "Copyright (C) 2012-2021 by Autodesk, Inc.; ISU 2023";
certificationLevel = 100000;

longDescription = "A post processor for sending Fusion 360 programs to the Kawasaki robots using AS language.";

capabilities = CAPABILITY_MILLING, CAPABILITY_ADDITIVE, CAPABILITY_INTERMEDIATE;
extension = ".pg";
setCodePage("utf-8");

allowMachineChangeOnSection = true;
allowHelicalMoves = true;
allowSpiralMoves = true;
allowedCircularPlanes = undefined;
allowFeedPerRevolutionDrilling = true;
maximumCircularSweep = toRad(1000000);
minimumCircularRadius = spatial(0.001, MM);
maximumCircularRadius = spatial(1000000, MM);

properties = {
    RapidFeed: {
        title       : "Rapid feed rate (mm/s)",
        description : "Set the robot feed rate (mm/s) during rapid positioning moves.",
        group       : "Parameters",
        type        : "integer",
        value       : 250,
        scope       : "post"
    },
    AssignHome: {
      title      : "Assign Current Position as WCS",
      description: "Set the current location and orientation as the WCS origin.",
      group      : "Parameters",
      type       : "boolean",
      value      : "true",
      scope      : "post"
    },
    xOffset: {
        title       : "X-home in base coordinates.",
        description : "The distance from the base coodinate system in X.",
        group       : "Coordinate System",
        type        : "integer",
        value       : 1156.0,
        scope       : "post"
    },
    yOffset: {
        title       : "Y-home in base coordinates.",
        description : "The distance from the base coodinate system in Y.",
        group       : "Coordinate System",
        type        : "integer",
        value       : 919,
        scope       : "post"
    },
    zOffset: {
        title       : "Z-home in base coordinates.",
        description : "The distance from the base coodinate system in Z.",
        group       : "Coordinate System",
        type        : "integer",
        value       : 1240,
        scope       : "post"
    },
    oOffset: {
        title       : "O-home in base coordinates.",
        description : "The distance from the base coodinate system in O.",
        group       : "Coordinate System",
        type        : "integer",
        value       : 90,
        scope       : "post"
    },
    aOffset: {
        title       : "A-home in base coordinates.",
        description : "The distance from the base coodinate system in A.",
        group       : "Coordinate System",
        type        : "integer",
        value       : 90,
        scope       : "post"
    },
    tOffset: {
        title       : "T-home in base coordinates.",
        description : "The distance from the base coodinate system in T.",
        group       : "Coordinate System",
        type        : "integer",
        value       : 45,
        scope       : "post"
    }
    }

var TRANSbuffer = [];

var xyzFormat = createFormat({decimals:4, prefix:" "});
var feedFormat = createFormat({decimals:2});
var tFormat = createFormat({decimals:3, prefix:" "});

var LMOVEformat = createFormat({prefix:"linear.t", suffix:" "});
var CMOVEformat = createFormat({prefix:"circular.t", suffix:" "});
var TRANSidx = 1;


function onOpen() {
    
    writeln(".PROGRAM JDH" + programName);
    writeln("ACCURACY 0.01 ALWAYS");
    if (getProperty("AssignHome")){
        setWCS();
    }
    var workpiece = getWorkpiece();
    var delta = Vector.diff(workpiece.upper, workpiece.lower);

    // REDIRECT TO THE TRANSFORMATION BUFFER
    redirectToBuffer();
    writeln(".TRANS");
    TRANSbuffer+=getRedirectionBuffer();
}

var X;
var Y;
var Z;
var TX;
var TY;
var TZ;


function writeComment(str){
    writeln(";"+str);
}

function redirectTRANS(x, y, z, tx, ty, tz, linear){
    redirectToBuffer();
    var polar = getPolarPosition(tx, ty, tz);
    o = polar.second.x + getProperty("oOffset");
    a = polar.second.y + getProperty("aOffset");
    t = polar.second.z + getProperty("tOffset");
    x = x + getProperty("xOffset");
    y = y + getProperty("yOffset");
    z = z + getProperty("zOffset");

    if(linear){
        var movePrefix = LMOVEformat.format(TRANSidx);
    } else{
        var movePrefix = CMOVEformat.format(TRANSidx)
    }
    writeln(movePrefix + 
        xyzFormat.format(x) + xyzFormat.format(y) + xyzFormat.format(z) + tFormat.format(o) + tFormat.format(a) + tFormat.format(t)
    )

    TRANSbuffer+=getRedirectionBuffer();
    TRANSidx+=1
    closeRedirection();
}

function setWCS(){
    writeln("HERE #wcs");
    writeln("SETHOME 0.1 #wcs");
}

function onSection() {
  setTranslation(currentSection.workOrigin);
  setRotation(currentSection.workPlane);

  var initialPosition = getFramePosition(currentSection.getInitialPosition());
  var ta = getFrameDirection(currentSection.getInitialToolAxis());

  X = initialPosition.x;
  Y = initialPosition.y;
  Z = initialPosition.z;
  TX = ta.x;
  TY = ta.y;
  TZ = ta.z;
}

function onRapid(x, y, z) {
    onLinear5D(x, y, z, TX, TY, TZ, getProperty("RapidFeed")*60);
}

function onLinear(x, y, z, feed) {
    onLinear5D(x, y, z, TX, TY, TZ, feed);
}

function onCircular(clockwise, cx, cy, cz, x, y, z, feed) {
    //var pos = getCurrentPosition();
    //writeComment("start:\t\t"+pos);
    //writeComment("mid:\t\t"+ getPositionU(.5));
    //writeComment("end: \t\t(" + xyzFormat.format(x) + ", " + xyzFormat.format(y) + ", " + xyzFormat.format(z) +")");
    //writeComment("center: \t(" + xyzFormat.format(cx) + ", " + xyzFormat.format(cy) + ", " + xyzFormat.format(cz) +")");
    //writeComment("radius: \t"+xyzFormat.format(getCircularRadius()));
    //writeComment("sweep: \t"+xyzFormat.format(getCircularSweep()*90/3.14159))
    writeln("SPEED " + feedFormat.format(feed/60) + " mm/s ALWAYS");

    var sweep = getCircularSweep()*180/3.14159;
    var mid = getPositionU(0.5);
    if (sweep>=360.0){
        // KRI AS can't handle 360-degree arcs. Divide into two for now.
        var midmid = getPositionU(0.25);
        writeln("C1MOVE " + CMOVEformat.format(TRANSidx));
        redirectTRANS(midmid.x, midmid.y, midmid.z, TX, TY, TZ, false);
        writeln("C2MOVE " + CMOVEformat.format(TRANSidx));
        redirectTRANS(mid.x, mid.y, mid.z, TX, TY, TZ, false); 
        // write 2nd half of arc move
        var latemid = getPositionU(0.75);
        writeln("C1MOVE " + CMOVEformat.format(TRANSidx));
        redirectTRANS(latemid.x, latemid.y, latemid.z, TX, TY, TZ, false);
        writeln("C2MOVE " + CMOVEformat.format(TRANSidx));
        redirectTRANS(x, y, z, TX, TY, TZ, false); 
    }else{
        // Write the middle point on the arc to C1MOVE
        writeln("C1MOVE " + CMOVEformat.format(TRANSidx));
        redirectTRANS(mid.x, mid.y, mid.z, TX, TY, TZ, false);
        // Write the arc end point to C2MOVE
        writeln("C2MOVE " + CMOVEformat.format(TRANSidx));
        redirectTRANS(x, y, z, TX, TY, TZ, false);
        //writeln("BREAK");
    }
}

function onRapid5D(x, y, z, tx, ty, tz) {
    onLinear5D(x, y, z, tx, ty, tz, getProperty("RapidFeed")*60);
}

function onLinear5D(x, y, z, tx, ty, tz, feed) {
    // Write linear move to x, y, z and vector tx, ty, tz at feed rate
    writeln("SPEED " + feedFormat.format(feed/60) + " mm/s");
    writeln("LMOVE " + LMOVEformat.format(TRANSidx));
    redirectTRANS(x, y, z, tx, ty, tz, true);
    //writeln("BREAK");
}



function onClose() {
    // Close out the program section
    writeln(".STOP");
    writeln(".END");

    // Write the transformation pose buffer
    TRANSbuffer += ".END\n;END OF TRANS";
    writeComment("Starting buffer output");
    writeln(TRANSbuffer);
}
