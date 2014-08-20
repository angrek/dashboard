from ssh import SSHClient

client = SSHClient()
client.load_system_host_keys()
client.connect("u2jdpdb", username="wrehfiel")
stdin, stdout, stderr = client.exec_command('oslevel -s')
#print "stderr: ", stderr.readlines()
#for line in stdout.readlines()
t = stdout.readlines()[0]
print t
