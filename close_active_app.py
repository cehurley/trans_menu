__author__ = 'churley'
import os
import subprocess
import time

def clicked_cb():
        activewinid = subprocess.Popen('xprop -root _NET_ACTIVE_WINDOW', shell=True, stdout=subprocess.PIPE).communicate()[0].strip().split()[-1]
        afterx = activewinid.split('x')[-1]
        activewinid = '0x' + '0' * (8-len(afterx)) + afterx
        wins = [x.strip().split() for x in subprocess.Popen('wmctrl -lp', shell=True, stdout=subprocess.PIPE).communicate()[0].strip().split('\n') if x.strip()]

        print wins

        tvtime_wins = [x[0] for x in wins if len(x) > 4 and x[4] == 'tvtime']
        tvcontrol_wins = [x[0] for x in wins if len(x) == 6 and x[4] == 'Television' and x[5] == 'Controls']

        if tvcontrol_wins:
            tvcontrol_pid = [x[2] for x in wins if len(x) == 6 and x[4] == 'Television' and x[5] == 'Controls'][0]
        else:
            tvcontrol_pid = 0

        if activewinid in tvtime_wins or activewinid in tvcontrol_wins:
            for w in tvtime_wins:
                subprocess.call(['killall','tvtime'])
                subprocess.Popen('wmctrl -ic %s'%w, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            for w in tvcontrol_wins:
                if tvcontrol_pid:
                    subprocess.call(['kill','%s'%tvcontrol_pid])
                subprocess.Popen('wmctrl -ic %s'%w, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        elif activewinid in [x[0] for x in wins if x[4] == 'LEFTNAV']:
            pass
        else:
            subprocess.Popen('exec wmctrl -c :ACTIVE:', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()


if __name__=='__main__':
    #time.sleep(5)
    clicked_cb()
