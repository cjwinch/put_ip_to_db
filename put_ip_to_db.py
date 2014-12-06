# Include the Dropbox SDK
import dropbox
import pickle
import StringIO
import socket

# Get your app key and secret from the Dropbox developer website
app_key = '...'
app_secret = '...'

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

try:
	access_token = pickle.load(open("dropbox_token.p", "rb"))

except IOError:
	# Have the user sign in and authorize this token
	authorize_url = flow.start()
	print '1. Go to: ' + authorize_url
	print '2. Click "Allow" (you might have to log in first)'
	print '3. Copy the authorization code.'
	code = raw_input("Enter the authorization code here: ").strip()

	access_token, user_id = flow.finish(code)

	pickle.dump( access_token, open( "dropbox_token.p", "wb" ) )


client = dropbox.client.DropboxClient(access_token)
#print 'linked account: ', client.account_info()

try:
	client.file_delete("rpi_ip_address.txt")
except dropbox.rest.ErrorResponse:
	pass

ip = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]

upload_str = StringIO.StringIO()
upload_str.write(ip)

response = client.put_file('rpi_ip_address.txt', upload_str)

print "uploaded:", response