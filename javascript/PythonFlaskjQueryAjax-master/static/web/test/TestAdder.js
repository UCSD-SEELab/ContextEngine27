/** Test accessor that adds its input values.
 *
 *  @accessor test/TestAdder
 *  @input inputLeft The left input, a number with default 0.
 *  @input inputRight The right input, a number with default 0.
 *  @output sum The sum of the two inputs.
 *  @author Edward A. Lee
 *  @version $$Id: TestAdder.js 546 2016-02-03 02:07:57Z cxh $$
 */

exports.setup = function() {
    this.input('inputLeft', {'type':'number', 'value':0});
    this.input('inputRight', {'type':'number', 'value':0});
    this.output('sum', {'type':'number'});
};

exports.fire = function() {
    this.send('sum', this.get('inputLeft') + this.get('inputRight'));
};
