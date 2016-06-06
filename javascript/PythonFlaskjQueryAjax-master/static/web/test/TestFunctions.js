/** Test top-level functions provided by the host.
 *
 *  @accessor test/TestFunctions
 *  @output getResource Outputs the contents of index.html if the host implements
 *   this.getResource() and can serve contents given 'index.html' as the URI.
 *  @output httpRequest Outputs the contents of index.html if the host implements
 *   httpRequest() and can serve contents given 'index.html' as the URL.
 *  @output readURL Outputs the contents of index.html if the host implements
 *   readURL() and can serve contents given 'index.html' as the URL.
 *  @author Edward A. Lee
 *  @version $$Id: TestFunctions.js 546 2016-02-03 02:07:57Z cxh $$
 */

exports.setup = function() {
    this.output('getResource', {'type':'string'});
    this.output('httpRequest', {'type':'string'});
    this.output('readURL', {'type':'string'});
};

exports.fire = function() {
    try {
        this.send('getResource', this.getResource('index.html', 3000));
    } catch(exception) {
        this.send('getResource', 'FAILED: ' + exception);
    }
    try {
        this.send('httpRequest', httpRequest('index.html', 'GET'));
    } catch(exception) {
        this.send('httpRequest', 'FAILED: ' + exception);
    }
    try {
        this.send('readURL', readURL('index.html'));
    } catch(exception) {
        this.send('readURL', 'FAILED: ' + exception);
    }
};
