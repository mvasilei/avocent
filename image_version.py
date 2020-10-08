#! /usr/bin/env python
import paramiko,sys,signal

def signal_handler(sig, frame):
    print('Exiting gracefully Ctrl-C detected...')
    sys.exit(0)

def main():

    try:
        with open('all_ts.txt', 'r') as f:
            lines = f.readlines()
    except IOError:
        print 'Could not read file /etc/hosts'
    
    for host in lines:
        print host,
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(host.strip(), username='USERNAME', password='PASSWORD')
        stdin, stdout, stderr=client.exec_command('show /system/information')
        for line in stdout:
            if 'firmware' in line: 
                print line,

        stdin, stdout, stderr=client.exec_command('exit')

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)  # catch ctrl-c and call handler to terminate the script
    main()
