import frida
import sys
import time
def on_message(message, data):
            print(message)

#post / get / url constructor hook
package_name = "com.ibk.smsmanager"

j_code = """
    console.log("[*] start script");
    Java.perform(function(){
        console.log("[*] ==== hooking start === ")
        
        var Activity2 = Java.use("org.apache.http.client.methods.HttpGet");
        Activity2.$init.overload('java.lang.String').implementation = function(a){
            console.log("HttpGet is called")
            this.$init.overload('java.lang.String').call(this, a)
        }

        var Activity = Java.use("org.apache.http.client.methods.HttpPost");
        Activity.$init.overload('java.lang.String').implementation = function(a){
            console.log("HttpPost is called")
            console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()))
            this.$init.overload('java.lang.String').call(this, a)
        }

        var Activity3 = Java.use("java.net.URL");
        Activity3.$init.overload('java.lang.String').implementation = function(a){
            console.log("URL is called")
            this.$init.overload('java.lang.String').call(this, a)
        }


        console.log("=== hooking finish ====")

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
