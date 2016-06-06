/** Display data on the console.
 *
 *  @accessor test/TestDisplay
 *  @param input The output
 *  @author Christopher Brooks
 *  @version $$Id: TestDisplay.js 748 2016-04-29 21:51:14Z cxh $$
 */

exports.setup = function() {
    this.input('input');
    this.output('output');
};

exports.initialize = function() {
    this.addInputHandler('input', function() {
        var inputValue = this.get('input');
        console.log(inputValue);
        this.send('output', inputValue);
    });
};
