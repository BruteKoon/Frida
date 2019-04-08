import frida
import sys
import time
def on_message(message, data):
            print(message)

#data information
package_name = "com.ibk.smsmanager"

j_code = """
    console.log("[*] start script");
    Java.perform(function(){
        var Activity = Java.use("com.example.kbtest.JSONParser");
        Activity.makeHttpRequest.overload('java.lang.String','java.lang.String','java.util.List').implementation = function(a,b,c){
            console.log("C & C Address : " + a)
            console.log("=== DATA === ")
            for(var i = 0; i<40; i++)
            {
                var item = c.get(i)
                console.log(item)
            }

        }
    });
    console.log("==== hooking Finish ====");
"""

device = frida.get_usb_device(timeout=10)
pid = device.spawn("com.ibk.smsmanager")
process = device.attach(pid)
script = process.create_script(j_code);

script.on('message', on_message)
print('[*] on Going')
script.load()
sys.stdin.read()
