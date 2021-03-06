// Copyright (c) 2014-2015 The Regents of the University of California.
// All rights reserved.

// Permission is hereby granted, without written agreement and without
// license or royalty fees, to use, copy, modify, and distribute this
// software and its documentation for any purpose, provided that the above
// copyright notice and the following two paragraphs appear in all copies
// of this software.

// IN NO EVENT SHALL THE UNIVERSITY OF CALIFORNIA BE LIABLE TO ANY PARTY
// FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES
// ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF
// THE UNIVERSITY OF CALIFORNIA HAS BEEN ADVISED OF THE POSSIBILITY OF
// SUCH DAMAGE.

// THE UNIVERSITY OF CALIFORNIA SPECIFICALLY DISCLAIMS ANY WARRANTIES,
// INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
// MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE
// PROVIDED HEREUNDER IS ON AN "AS IS" BASIS, AND THE UNIVERSITY OF
// CALIFORNIA HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES,
// ENHANCEMENTS, OR MODIFICATIONS.

/** Retrieve a location given an address.
 *  The location is given as an object with two numeric fields,
 *  "latitude" and "longitude". For example,
 *  `{"latitude": 37.85, "longitude": -122.26}` is
 *  the location of Berkeley, California.
 *
 *  This accessor requires a "key" for the Google Geocoding API, which you can
 *  obtain for free at https://developers.google.com/maps/documentation/geocoding/intro .
 *
 *  This accessor does not block waiting for the response, but if any additional
 *  *address* input is received before a pending request has received a response
 *  or timed out, then the new request will be queued and sent out only after
 *  the pending request has completed. This strategy ensures that outputs are
 *  produced in the same order as the input requests.
 *
 *  @accessor services/GeoCoder
 *  @input {string} address The address, for example "Berkeley, CA".
 *  @output location The location, as an object with a 'latitude' and 'longitude'
 *   property.
 *  @parameter {string} key The key for the Google geocoding API.
 *  @output response An object containing the location information.
 *  @author Edward A. Lee
 *  @version $$Id: GeoCoder.js 546 2016-02-03 02:07:57Z cxh $$
 */

// Stop extra messages from jslint and jshint.  Note that there should
// be no space between the / and the * and global. See
// https://chess.eecs.berkeley.edu/ptexternal/wiki/Main/JSHint */
/*globals addInputHandler, get, getParameter, error, exports, extend, get, input, output, parameter, require, send */
/*jshint globalstrict: true*/
'use strict';

/** Set up the accessor by defining the inputs and outputs.
 */
exports.setup = function() {
    this.extend('net/REST');
    this.input('address');
    this.output('location');
    this.parameter('key', {'type':'string', 'value':'Enter Key Here'});
    
    // Change default values of the base class inputs.
    // Also, hide base class inputs, except trigger.
    // Note the need for quotation marks on the options parameter.
    this.input('options', {'visibility':'expert', 'value':'"https://maps.googleapis.com"'});
    this.input('command', {'visibility':'expert', 'value':'maps/api/geocode/json'});
    // NOTE: The value can be given as a JSON string or a JavaScript object.
    this.input('arguments', {'visibility':'expert', 'value':{"address":"Berkeley, CA", "key":"Enter Key Here"}});
    this.input('body', {'visibility':'expert'});
    this.input('trigger', {'visibility':'expert'});
    this.output('headers', {'visibility':'expert'});
    this.output('status', {'visibility':'expert'});
    this.parameter('outputCompleteResponsesOnly', {'visibility':'expert'});
};

exports.initialize = function() {
    // Be sure to call the superclass so that the trigger input handler gets registered.
    exports.ssuper.initialize.call(this);
    
    var key = this.getParameter('key');
    if (key == "Enter Key Here") {
        throw "GeoCoder:  You need a key, which you can obtain at https://developers.google.com/maps/documentation/geocoding/intro.";
    }
    var self = this;
    
    // Handle location information.
    this.addInputHandler('address', function() {
        var address = this.get('address');
        if (address) {
            // arguments is a reserved word, so we use args.
            var args = {
                'address' : address,
                'key' : key
            };
            self.send('arguments', args);
            self.send('trigger', true);
        } else {
            throw 'GeoCoder: No address.';
        }
    });
};

/** Filter the response, extracting the latitude and longitude and
 *  formatting.
 */
exports.filterResponse = function(response) {
    if (response) {
        // Note that for some hosts, the response is a string, needing to parsed,
        // and for some, its already been parsed.
        var parsed = response;
        if (typeof parsed === 'string') {
            try {
                parsed = JSON.parse(response);
            } catch (err) {
                error('GeoCoder: Unable to parse response: ' + err.message +
                        '\nResponse was: ' + response);
                // So that downstream actors don't just a previous location, send null.
                this.send('location', null);
            }
        }
        // NOTE: All of the following should be replaced with a generic
        // schema transformation utility.
        // FIXME: Just taking the first result if there are multiple matches.
        if (parsed.results &&
            parsed.results[0] &&
            parsed.results[0].geometry &&
            parsed.results[0].geometry.location &&
            parsed.results[0].geometry.location.lat &&
            parsed.results[0].geometry.location.lng) {
            this.send('location', {
                    "latitude": parsed.results[0].geometry.location.lat,
                    "longitude": parsed.results[0].geometry.location.lng
            });
        } else {
            error('GeoCoder: No matching location.');
            // So that downstream actors don't just a previous location, send null.
            this.send('location', null);
        }
    }
    return response;
};
