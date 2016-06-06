/** Test WebSocketClient.
 *
 *  @accessor test/TestWebSocketClient
 *  @author Christopher Brooks
 *  @version $$Id: TestWebSocketClient.js 663 2016-04-05 00:10:46Z cxh $$
 */

exports.setup = function() {
    var client = this.instantiate('WebSocketClient', 'net/WebSocketClient');
};

// NOTE: If you provide a fire() function for a composite accessor,
// then it is up to you to invoke react() on the contained accessors.

// NOTE: If you provide an initialize() function for a composite accessor,
// then it is up to you to initialize the contained accessors.
