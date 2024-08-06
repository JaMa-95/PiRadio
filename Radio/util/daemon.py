import sys, os, atexit
import time
import psutil
from signal import SIGTERM
from Radio.util.util import get_project_root


class Daemon:
    """
    A generic daemon class.
    
    Usage: subclass the Daemon class and override the run() method
    """
    def __init__(self, pidfile, stdin='/dev/null', stdout='', stderr=""):
        root = get_project_root()
        if not stdout:
            stdout = root / "out.txt"
        if not stderr:
            stderr = root / "error.txt"
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
    
    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError as e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError as e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        open(self.pidfile,'w+').write("%s\n" % pid)
    
    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            text = "Starting daemon: " + self.pidfile + "\n"
            sys.stderr.write(text)
            with open(self.pidfile, "r") as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)
        
        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        sys.stdout.write("STOPPING daemon: " + self.pidfile + "\n")
        try:
            text = "STOPPING daemon: " + self.pidfile + "\n"
            sys.stderr.write(text)
            with open(self.pidfile, "r") as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None
        if not pid: 
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return # not an error in a restart
        
        self._stop()

        if os.path.exists(self.pidfile):
            os.remove(self.pidfile)
        try:
            print("DELETE PID ", pid)
            import subprocess
            # subprocess.run("kill -9 " + str(pid), shell = True, executable="/bin/bash")
            
            print("ABC")
            p = psutil.Process(pid)
            print("CDE")
            p.terminate()
            """
            print("DEF")
            os.kill(pid, SIGTERM)
            print("ASD")
            time.sleep(0.1)
            """
            print("DELETED PID")
        except psutil.NoSuchProcess:
            print(f"No such process with PID {pid}")
        except psutil.AccessDenied:
            print(f"Access denied when trying to terminate process with PID {pid}")
        except OSError as err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print(str(err))
                sys.exit(1)
        except Exception as e:
            print(f"An error occurred: {e}")
        
        print("DELETE ABC")
        if os.path.exists(self.pidfile):
            os.remove(self.pidfile)
 

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def run(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """


if __name__ == "__main__":
    daemon = Daemon("/tmp/PiRadio.pid")
    daemon.stop()