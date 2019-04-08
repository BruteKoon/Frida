import frida
import sys
import time
def on_message(message, data):
            print(message)

#url Destination and method(post)
package_name = "com.ibk.smsmanager"

j_code = """
    console.log("[*] start script");
    Java.perform(function(){
        var Activity = Java.use("com.example.kbtest.JSONParser");
        console.log("[*] ==== overload start === ")
        Activity.makeHttpRequest.overload('java.lang.String','java.lang.String','java.util.List').implementation = function(a,b,c){
            console.log(a)
            console.log(b)
            console.log("overload finish")
        }
    });
    console.log("[*] Finish ");
"""

device = frida.get_usb_device(timeout=10)
pid = device.spawn("com.ibk.smsmanager")
process = device.attach(pid)
script = process.create_script(j_code);

script.on('message', on_message)
print('[*] on Going')
script.load()
sys.stdin.read()
