import frida
import sys

package_name = "com.example.user.webview2"


def get_messages_from_js(message, data):
            print(message)

hook_code ="""
        console.log("hooking")
        Interceptor.attach(Module.findExportByName("libc.so", "open"),{
            onEnter : function(args){
                console.log("enter")
                this.flag = false;
                var filename = Memory.readCString(ptr(args[0]));
                console.log(filename)
                if (filename.indexOf("/dev/ashmem") != -1) {
                    console.log("backtrace")
		    this.flag = true;
		    var backtrace = Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress).join("");
		    console.log("file name [ " + Memory.readCString(ptr(args[0])) + " ]Backtrace:" + backtrace);
		}
        },
            onLeaver: function(retval){
                console.log("leave")
                if (this.flag)
	            console.warn("retval: " + retval);
            }

        });
"""



device = frida.get_device_manager().enumerate_devices()[-1]
pid = device.spawn(package_name)
session = device.attach(pid)
script = session.create_script(hook_code)
script.on('message',get_messages_from_js)
script.load()
sys.stdin.read()
