#! /usr/bin/env python
import paramiko,sys,signal,subprocess,time

def connection_establishment(host):
   try:
      client = paramiko.SSHClient()
      client.load_system_host_keys()
      client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      client.connect(host, 22, username='USERNAME', password='PASSWORD')
      channel = client.invoke_shell()
      out = channel.recv(1)
   except paramiko.AuthenticationException as error:
      print 'Authentication Error'
      exit()
   return (channel,client)

def connection_teardown(client):
   client.close()

def execute_command(command, channel, wait):
  channel.send(command)
  time.sleep(wait)
  out = channel.recv(1024)
  return (out)
    
def signal_handler(sig, frame):
    print('Exiting gracefully Ctrl-C detected...')
    sys.exit(0)

def main():

    try:
        with open('upgrade.txt', 'r') as f:
            lines = f.readlines()
    except IOError:
        print 'Could not read file /etc/hosts'
    
    for host in lines:
        print host,

        p = subprocess.Popen(["sshpass -p PASSWORD scp -o StrictHostKeyChecking=no avoImage_avctacs_3.7.0.11.bin USERNAME@" + host.strip() + ":/tmp/avoImage_avctacs_3.7.0.11.bin"], stdout=subprocess.PIPE ,shell=True)
        print p.communicate()[0]

        channel,client = connection_establishment(host.strip())

        stdout=execute_command('md5sum /tmp/avoImage_avctacs_3.7.0.11.bin\n',channel,2)
        print stdout

        connection_teardown(client)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)  # catch ctrl-c and call handler to terminate the script
    main()
