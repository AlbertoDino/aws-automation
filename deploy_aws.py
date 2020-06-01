#
# Simple script that automates some simple commands:
# 1: copies a zip file from local to a aws server instance.
#    a /temp/ folder needs to exists with read and write grants by any user ( chmod 777 )
# 2: unzip the artifact zip file into the apache www/html folder.
#    require unzip to be installed ( apt-get install zip unzip ) 
#
# Requires paramiko ( http://www.paramiko.org/ ) 
import paramiko as pk

# vars
artifact      = 'myartifact.zip'
host          = 'ec2-my.compute.amazonaws.com'
key           = pk.RSAKey.from_private_key_file('C:/mykey.pem')
artifact_path = './aws/{}'.format(artifact)
remote_dir    = 'temp/{}'.format(artifact)

# Commands list
commands = [ "sudo cp -f temp/{} /var/www/html/".format(artifact)
            ,"sudo unzip -o temp/{} -d /var/www/html/".format(artifact)]

# SSH Connection to server
client = pk.SSHClient()
client.set_missing_host_key_policy(pk.AutoAddPolicy())
print('Connecting to '+host+' ...')
client.connect(host,username='ubuntu',pkey=key)
print('ok.')

# SFTP Copying artifact to server 
print('Copying {} to server {} ...'.format(artifact_path,remote_dir))
sftp = client.open_sftp()
sftp.put(artifact_path,remote_dir)
sftp.close()
print('ok.')

# Commands executions
try:
    for cmd in commands:
        print("> "+cmd)
        stdin, stdout, stderr = client.exec_command(cmd)
        out_lines             = stdout.read().splitlines()
        for line in out_lines:
            print(line)
        str_error = stderr.read()
        if str_error: 
            print('--Errors')
            print(str_error)
        else:
            print('ok.')
finally:
    client.close()
