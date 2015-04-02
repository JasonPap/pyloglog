#!/usr/bin/python

import os
import sys
import getopt

def usage():
	print "\t -h, --help to see usage manual."
	print "\t -o <filename> or --output <filename> to set the output filename. If not set, the default is FailedLogginsMapped.html"
	print "\t -i <filename> or --input <filename> to set the input filename. This argument in mandatory."
	print "\t -d <delimiter> or --delimiter <delimiter> to set the column separator char. Default is the comma ','"

def main():
	# Parsing of arguments #
	try:
		opts, args = getopt.getopt(sys.argv[1:], "ho:i:d:", ["help", "output=", "input=", "delimiter="])
	except getopt.GetoptError as err:
	# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
	input = None
	delimiter = ","
	output = "FailedLogginsMapped.html"
	for o, a in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-o", "--output"):
			output = a
		elif o in ("-i", "--input"):
			input = a
		elif o in ("-d", "--delimiter"):
			delimiter = a
		else:
			assert False, "unhandled option"
	
	if input is None:
		print "No input file was given. Use -h for help."
		sys.exit(3)
	
	aggregatedData = dict()	# key: lalo, value: occurrences
	with open(input) as inputFile:
		for line in inputFile:
			attr = line.split(delimiter)
			try:
				lalo = attr[3] + "," + attr[4]
			except:
				print line
				raise
			if lalo in aggregatedData:
				aggregatedData[lalo] += 1
			else:
				print "new lalo = " + lalo
				aggregatedData[lalo] = 1
	
	
	list2html = []
	multiplier = 100
	for datapoint in aggregatedData:
		entry = "[" + "'" + str(aggregatedData[datapoint]) + "'" + "," + datapoint + "," + str(multiplier*aggregatedData[datapoint]) + "]"
		list2html.append(entry)
	
	text2html = ",".join(list2html)
	with open(output, "a+") as outputfile:
		outputfile.seek(0)
		outputfile.write(htmlstart)
		outputfile.write(text2html)
		outputfile.write(htmltail)
	
	print "done"


htmlstart = """<!DOCTYPE html>
<html> 
<head> 
  <meta http-equiv="content-type" content="text/html; charset=UTF-8" /> 
  <title>Google Maps Multiple Markers</title> 
  <script src="http://maps.google.com/maps/api/js?sensor=false"></script>
  <script src="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.10.1.min.js"></script>
</head> 
<body>
  <div id="map" style="width: 1920x; height: 1080px;"></div>

  <script type="text/javascript">
    // Define your locations: HTML content for the info window, latitude, longitude
    var locations = ["""	
	
htmltail =""" ];
    //ENDING
    // Setup the different icons and shadows
    var iconURLPrefix = 'http://maps.google.com/mapfiles/ms/icons/';
    
    var icons = [
      iconURLPrefix + 'red-dot.png',
     // iconURLPrefix + 'green-dot.png',
      iconURLPrefix + 'blue-dot.png',
    //  iconURLPrefix + 'orange-dot.png',
    //  iconURLPrefix + 'purple-dot.png',
    //  iconURLPrefix + 'pink-dot.png',      
    //  iconURLPrefix + 'yellow-dot.png'
    ]
    var icons_length = icons.length;
    
    
    var shadow = {
      anchor: new google.maps.Point(15,33),
      url: iconURLPrefix + 'msmarker.shadow.png'
    };

    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 3,
      center: new google.maps.LatLng(0,0),
      mapTypeId: google.maps.MapTypeId.ROADMAP,
      mapTypeControl: false,
      streetViewControl: false,
      panControl: false,
      zoomControlOptions: {
         position: google.maps.ControlPosition.LEFT_BOTTOM
      }
    });

    var infowindow = new google.maps.InfoWindow({
      maxWidth: 160
    });

    var marker;
    var markers = new Array();
    
    var iconCounter = 0;
    
    // Add the markers and infowindows to the map
    for (var i = 0; i < locations.length; i++){
        if(i>=20000)
            temp_icon = iconURLPrefix + 'yellow-dot.png';
        else
            temp_icon = icons[iconCounter];
		marker = new google.maps.Marker({
        position: new google.maps.LatLng(locations[i][1], locations[i][2]),
        map: map,
        icon : temp_icon,
        shadow: shadow
      });
		
		///radius code
		// Add circle overlay and bind to marker
		var circle = new google.maps.Circle({
		  map: map,
		  radius: locations[i][3],  
		  fillColor: '#AA0000'
		});
		circle.bindTo('center', marker, 'position');
		//
		
      markers.push(marker);

      google.maps.event.addListener(marker, 'click', (function(marker, i) {
        return function() {
          infowindow.setContent(locations[i][0]);
          infowindow.open(map, marker);
        }
      })(marker, i));
      
      iconCounter++;
      // We only have a limited number of possible icon colors, so we may have to restart the counter
      if(iconCounter >= icons_length){
      	iconCounter = 0;
      }
    }

    function AutoCenter() {
      //  Create a new viewpoint bound
      var bounds = new google.maps.LatLngBounds();
      //  Go through each...
      $.each(markers, function (index, marker) {
        bounds.extend(marker.position);
      });
      //  Fit these bounds to the map
      map.fitBounds(bounds);
    }
    //AutoCenter();
  </script> 
</body>
</html>
"""


if __name__ == "__main__":
        main()

