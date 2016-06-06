/** Test accessor that implements an interface defined by another.
 *  To show that base class functionality if not inherited, this
 *  accessor reacts only to the numeric input and does not print
 *  any fire message, even though the base class has a fire() function
 *  that does.
 *
 *  @accessor test/TestImplement
 *  @author Edward A. Lee
 *  @version $$Id: TestImplement.js 546 2016-02-03 02:07:57Z cxh $$
 */

exports.setup = function() {
    this.implement('test/TestAccessor');
};

exports.initialize = function() {
    this.addInputHandler('numeric', function() {
        this.send('numericPlusP', this.get('numeric') + this.getParameter('p'));
    });
};
