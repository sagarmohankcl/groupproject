# groupproject

For running the Server: python chatserver.py
For running the Python Client: python chat_client.py
For running the Android Client: Build the project in android studio

Connection Settings:
For running the client on the same machine as the server. Run two copies of the chat_client.py file with the following setting:
On first client: client_port = 8080 (line 25), self.port = 8081 (line 829)
One second client:  client_port = 8081 (line 25), self.port = 8080 (line 829)

Note: In this working version of chat_client.py, a small bug persists: To add a contact, substitute the line 363 with 
self.options['search']['USER'] = contact ) 
and 
line 365 with 
response = (self.connect_remote_server(self.options['search'])) 

Since renaming the variable from 'options' to 'request' didn't merge properly in the last version.





  
