/** Test accessor that spontaneously produces outputs once per time interval.
 *  This implementation produces a counting sequence.
 *
 *  @accessor test/TestSpontaneous
 *  @parameter interval The interval between outputs in milliseconds.
 *  @output output Output for the counting sequence, of type number.
 *  @author Edward A. Lee
 *  @version $$Id: TestSpontaneous.js 546 2016-02-03 02:07:57Z cxh $$
 */

exports.setup = function() {
    this.parameter('interval', {'type':'number', 'value':10});
    this.output('output', {'type': 'number'});
};

// These variables will not be visible to subclasses.
var handle = null;
var count = 0;

exports.initialize = function() {
    count = 0;
    // Need to record 'this' for use in the callback.
    var thiz = this;
    handle = setInterval(function() {
        console.log("Value in spontaneously: " + count);     
        thiz.send('output', count++);
    }, this.getParameter('interval'));
};

exports.wrapup = function() {
    if (handle) {
        clearInterval(handle);
        handle = null;
    }
};
