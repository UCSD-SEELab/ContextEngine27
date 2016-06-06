/** Test accessor that multiplies its input by a scale factor.
 *
 *  @accessor test/TestGain
 *  @param gain The gain, a number with default 2.
 *  @param input The input, a number with default 0.
 *  @param scaled The output, the result of input * gain.
 *  @author Edward A. Lee
 *  @version $$Id: TestGain.js 546 2016-02-03 02:07:57Z cxh $$
 */

exports.setup = function() {
    this.input('input', {'type':'number', 'value':0});
    this.output('scaled', {'type':'number'});
    this.parameter('gain', {'type':'number', 'value':2});
};

exports.initialize = function() {
	console.log("In Gain");
	this.send('scaled', this.get('input') * this.getParameter('gain'));
};
