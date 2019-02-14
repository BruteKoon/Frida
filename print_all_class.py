import sys
import frida

def on_message(message,data):
    print "[%s] -> %s" % (message, data)


PACKAGE_NAME = "com.example.user.webview1"

jscode = """
Java.perform(function(){
    Java.enumerateLoadedClasses(
    { 
      onMatch: function(className)
      {
        send(className);
      },
      onComplete:function(){}
    });

});
"""
    
try:
    device = frida.get_usb_device(timeout=10)
    pid = device.spawn([PACKAGE_NAME])  
    print("App is starting ... pid : {}".format(pid))
    process = device.attach(pid)
    device.resume(pid)
    script = process.create_script(jscode)
    script.on('message',on_message)
    print('[*] Running Frida')
    script.load()
    sys.stdin.read()
except Exception as e:
    print(e)
