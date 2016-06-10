
/* Algunas de las funciones de este documento han sido extraídas de las siguientes páginas web:
http://www.gpsvisualizer.com/calculators
 */

        function getdistance(lat1, lon1, lat2, lon2) {
          var p = 0.017453292519943295;    // Math.PI / 180
          var c = Math.cos;
          var a = 0.5 - c((lat2 - lat1) * p)/2 +
                  c(lat1 * p) * c(lat2 * p) *
                  (1 - c((lon2 - lon1) * p))/2;

          return 12742 * Math.asin(Math.sqrt(a)); // 2 * R; R = 6371 km
        }

        function comma2point (number) {
            number = number+''; // force number into a string context
            return (number.replace(/,/g,'.'));
        }

        function deg2rad (deg) {
            return (parseFloat(comma2point(deg)) * 3.14159265358979/180);
        }

        function rad2deg (radians) {
            return (Math.round(10000000 * parseFloat(radians) * 180/3.14159265358979) / 10000000);
        }

        function distanceTo(start_lat,start_lon,distance,bearing) { // input is in degrees, km, degrees
            // http://www.fcc.gov/mb/audio/bickel/sprong.html
            var ending_point = []; // output
            var earth_radius = 6378137; // equatorial radius
            // var earth_radius = 6356752; // polar radius
            // var earth_radius = 6371000; // typical radius
            var start_lat_rad = deg2rad(start_lat);
            var start_lon_rad = deg2rad(start_lon);
            //var distance = parseDistance(distance_text);

            bearing = -bearing+90;

            if (Math.abs(bearing) >= 360) { bearing = bearing % 360; }
            bearing = (bearing < 0) ? bearing+360 : bearing;

            var isig = (bearing <= 180) ? 1 : 0; // western half of circle = 0, eastern half = 1
            var a = 360-bearing; // this subroutine measures angles COUNTER-clockwise, so +3 becomes +357
            a = deg2rad(a); var bb = (Math.PI/2)-start_lat_rad; var cc = distance/earth_radius;
            var sin_bb = Math.sin(bb); var cos_bb = Math.cos(bb); var cos_cc = Math.cos(cc);
            var cos_aa = cos_bb*cos_cc+(sin_bb*Math.sin(cc)*Math.cos(a));
            if (cos_aa <= -1) { cos_aa = -1; } if (cos_aa >= 1) { cos_aa = 1; }
            var aa = (cos_aa.toFixed(15) == 1) ? 0 : Math.acos(cos_aa);
            var cos_c = (cos_cc-(cos_aa*cos_bb))/(Math.sin(aa)*sin_bb);
            if (cos_c <= -1) { cos_c = -1; } if (cos_c >= 1) { cos_c = 1; }
            var c = (cos_c.toFixed(15) == 1) ? 0 : Math.acos(cos_c);
            var end_lat_rad = (Math.PI/2)-aa;
            var end_lon_rad = start_lon_rad-c;
            if (isig == 1) { end_lon_rad = start_lon_rad + c; }
            if (end_lon_rad > Math.PI) { end_lon_rad = end_lon_rad - (2*Math.PI); }
            if (end_lon_rad < (0-Math.PI)) { end_lon_rad = end_lon_rad + (2*Math.PI); }
            ending_point[0] = rad2deg(end_lat_rad); ending_point[1] = rad2deg(end_lon_rad);

            return (ending_point);
        }


        //-----------------------------------------------------------------------------------------------------
