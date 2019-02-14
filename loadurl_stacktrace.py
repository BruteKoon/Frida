import frida
import sys

package_name1 = "com.example.user.webview2"
package_name2 = "com.example.user.tutorial1"

def get_messages_from_js(message, data):
            print(message)
 

hook_code = """
    var Color = {
        RESET: "\x1b[39;49;00m", Black: "0;01", Blue: "4;01", Cyan: "6;01", Gray: "7;11", Green: "2;01", Purple: "5;01", Red: "1;01", Yellow: "3;01",
        Light: {
            Black: "0;11", Blue: "4;11", Cyan: "6;11", Gray: "7;01", Green: "2;11", Purple: "5;11", Red: "1;11", Yellow: "3;11"
        }
    };

var LOG = function (input, kwargs) {
    kwargs = kwargs || {};
    var logLevel = kwargs['l'] || 'log', colorPrefix = '\x1b[3', colorSuffix = 'm';
    if (typeof input === 'object')
        input = JSON.stringify(input, null, kwargs['i'] ? 2 : null);
    if (kwargs['c'])
        input = colorPrefix + kwargs['c'] + colorSuffix + input + Color.RESET;
    console[logLevel](input);
};

var printBacktrace = function () {
    Java.perform(function() {
        var android_util_Log = Java.use('android.util.Log'), java_lang_Exception = Java.use('java.lang.Exception');
        // getting stacktrace by throwing an exception
        LOG(android_util_Log.getStackTraceString(java_lang_Exception.$new()), { c: Color.Red });
    });
};


var Main = function() {
    Java.perform(function () { 
        Java.use('android.webkit.WebView').loadUrl.overload("java.lang.String").implementation = function (s) {
            LOG('overload', { c: Color.Light.Red });
            printBacktrace();
            return true;
        }
    });
};

Java.perform(Main)

"""
device = frida.get_device_manager().enumerate_devices()[-1]
pid = device.spawn(package_name1)
session = device.attach(pid)
script = session.create_script(hook_code)
script.on('message',get_messages_from_js)
script.load()
sys.stdin.read()
