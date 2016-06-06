/** Test a composite accessor containing a spontaneous accessor.
 *  This test contains an accessor that produces a counting sequence that is then
 *  fed into a TestGain accessor, which multiplies the counting sequence by 4.
 *
 *  @accessor test/TestCompositeSpontaneous
 *  @output output A counting sequence with increments of 4.
 *  @author Edward A. Lee
 *  @version $$Id: TestCompositeSpontaneous.js 546 2016-02-03 02:07:57Z cxh $$
 */

exports.setup = function() {
    this.output('output', {'type':'number'});
    var gen = this.instantiate('TestSpontaneous', 'test/TestSpontaneous');
    var gain = this.instantiate('TestGain', 'test/TestGain');
    gain.setParameter('gain', 4);
    this.connect(gen, 'output', gain, 'input');
    this.connect(gain, 'scaled', 'output');
};

// NOTE: If you provide a fire() function for a composite accessor,
// then it is up to you to invoke react() on the contained accessors.

// NOTE: If you provide an initialize() function for a composite accessor,
// then it is up to you to initialize the contained accessors.
