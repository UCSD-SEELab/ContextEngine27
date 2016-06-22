var LLA2_ECEF;
var LLA_DIST;


exports.setup = function() {
    this.input('input');
    this.output('output');      

    LLA2_ECEF = this.instantiate('LLA2_ECEF', 'geodesy/Lla2Ecef');
    LLA_DIST = this.instantiate('LLA_DIST', 'geodesy/LlaDist');  
};

exports.initialize = function() {
    
    console.log("Number: " + Number(this.get('input')));

	
	if (Number(this.get('input')) == 0) {
        console.log('Running LLA2_ECEF');
       
		this.connect('input', LLA2_ECEF, 'lat');
		this.connect('input', LLA2_ECEF, 'lon');
		this.connect('input', LLA2_ECEF, 'alt');
		this.connect(LLA2_ECEF, 'x', 'output');
	} else if (Number(this.get('input')) == 1) {
		console.log('Running LLA_DIST');
		
		this.connect('input', LLA_DIST, 'lat1');
		this.connect('input', LLA_DIST, 'lon1');
		this.connect('input', LLA_DIST, 'alt1');
		this.connect('input', LLA_DIST, 'lat2');
		this.connect('input', LLA_DIST, 'lon2');
		this.connect('input', LLA_DIST, 'alt2');
		this.connect(LLA_DIST, 'dist', 'output'); 
	} 
};
