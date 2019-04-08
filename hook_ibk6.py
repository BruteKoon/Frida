import frida
import sys
import time
def on_message(message, data):
            print(message)

#stack trace
package_name = "com.ibk.smsmanager"

j_code = """
    console.log("[*] start script");
    Java.perform(function(){
        var threadef = Java.use('java.lang.Thread')
        var threadinstance = threadef.$new()

        function Where(stack){
            var at = ""
            for(var i = 0; i < stack.length; ++i){
                at += stack[i].toString() + "\\n"
            }
            return at
        }

        var Activity = Java.use("org.apache.http.client.methods.HttpPost");
        console.log("==== hooking finish ==== ")
        Activity.$init.overload('java.lang.String').implementation = function(a){
            var stack = threadinstance.currentThread().getStackTrace()
            var full_call_stack = Where(stack)
            console.log("Http Post is called")
            console.log("==== Http post call stack ==== ")
            console.log(full_call_stack)
            this.$init.overload('java.lang.String').call(this, a)
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
