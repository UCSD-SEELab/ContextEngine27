/** Test accessor that is similar to its base class, except that it requires
 *  the 'util' module. This tests both require() and this.extend().
 *
 *  @accessor test/TestRequire
 *  @parameter p A parameter with default value 42.
 *  @input untyped An untyped input that will accept any JavaScript object.
 *  @input numeric A numeric input.
 *  @input boolean A boolean input.
 *  @output typeOfUntyped Produces the type (a string) of the input named 'untyped'.
 *  @output jsonOfUntyped Produces a JSON representation of the input named 'untyped',
 *   created using the util module.
 *  @output numericPlusP Produces the value of the 'numeric' input plus 'p'.
 *  @output negation Produces the negation of the 'boolean' input.
 *  @author Edward A. Lee
 *  @version $$Id: TestRequire.js 546 2016-02-03 02:07:57Z cxh $$
 */

var util = require('util');

exports.setup = function() {
    this.extend('test/TestAccessor');
};

exports.initialize = function() {
    // Test ability to invoke superclass function from overridden function.
    this.ssuper.initialize();
};

/** Override the base class to use util. */
exports.formatOutput = function(value) {
    return util.format('JSON for untyped input using util.format(): %j', value);
};
