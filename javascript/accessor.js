var Accessor = class Accessor {
  
 	var instance;
 
	function createInstance() {
	    var object = new Accessor();
	    return object;
	}

	return {
	    getInstance: function () {
	        if (!instance) {
	            instance = createInstance();
	        }
	        return instance;
	    }
	};

	constructor(accessorList) {
    this.accessorList = accessorList;    
  }


  //Passes relevant parameters to Tesla.py 
  function passToTesla(accList) {
  		$.ajax({
		  type: "POST",
		  url: "~/python/Tesla.py",
		  data: { accList }
		}).done(function( o ) {
		   console.log("Finished Tesla Execution.";
		});            
	}

};