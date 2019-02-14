import frida
import sys
import time
def on_message(message, data):
            print(message)


package_name = "com.example.user.webview2"

j_code = """
    console.log("[*] start script");
    Java.perform(function(){
        var webview = Java.use("android.webkit.WebView");
        console.log("class start:-----------------");
        webview.loadUrl.overload("java.lang.String").implementation = function(s){
            console.log("original loadurl " + s);
            this.loadUrl("https://www.google.com");
        };
    });
"""

device = frida.get_usb_device(timeout=10)
pid = device.spawn("com.example.user.webview2")
process = device.attach(pid)
script = process.create_script(j_code);

script.on('message', on_message)
print('[*] on Going')
script.load()
sys.stdin.read()
