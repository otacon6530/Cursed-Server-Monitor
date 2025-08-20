import win32serviceutil
import win32service
import win32event
import servicemanager
import time
import subprocess

class ServMonService(win32serviceutil.ServiceFramework):
    _svc_name_ = "ServMonService"
    _svc_display_name_ = "Server Monitor Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.running = False
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ""))
        self.main()

    def main(self):
        while self.running:
            # Call your function here, e.g.:
            subprocess.call(['python', 'servmon.py', 'sql'])
            time.sleep(5)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(ServMonService)
