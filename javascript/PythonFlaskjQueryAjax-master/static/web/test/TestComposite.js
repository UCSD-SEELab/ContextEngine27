/** Test composite accessor.
 *  This accessor contains two accessors, a gain and an adder.
 *  It multiplies the input by 4 and adds the result to the input.
 *  The sum is sent to the output.
 *
 *  @accessor test/TestComposite
 *  @input input A numeric input with default value 0.
 *  @output output The result of x + 4x, where x is the value of the input.
 *  @author Edward A. Lee
 *  @version $$Id: TestComposite.js 546 2016-02-03 02:07:57Z cxh $$
 */

exports.setup = function() {
    this.input('input', {'type':'number', 'value':0});
    this.output('output', {'type':'number'});
    var gain = this.instantiate('TestGain', 'test/TestGain');
    gain.setParameter('gain', 4);
    var adder = this.instantiate('TestAdder', 'test/TestAdder');
    this.connect('input', adder, 'inputLeft');
    this.connect('input', gain, 'input');
    this.connect(gain, 'scaled', adder, 'inputRight');
    this.connect(adder, 'sum', 'output');
};

// NOTE: If you provide a fire() function for a composite accessor,
// then it is up to you to invoke react() on the contained accessors.

// NOTE: If you provide an initialize() function for a composite accessor,
// then it is up to you to initialize the contained accessors.
