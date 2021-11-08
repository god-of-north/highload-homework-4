import os
from subprocess import Popen


s = Popen(['python3', os.path.join(os.environ.get('$APP_HOME'), 'project', 'cache.py')])
                      
#w = Popen(['gunicorn', '--bind', '0.0.0.0:5000', 'manage:app'])
#w = Popen(['gunicorn', '--bind', '0.0.0.0:5000', 'manage:app', '-k', 'gevent', '--worker-connections', '1000'])
#w = Popen(['gunicorn', '--bind', '0.0.0.0:5000', 'manage:app', '-w', '1', '--threads', '12'])
w = Popen(['gunicorn', '--bind', '0.0.0.0:5000', 'manage:app', '-w', '4'])

s.wait()
w.wait()
 
