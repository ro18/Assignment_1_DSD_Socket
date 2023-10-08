import socket


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
        self.eof_token = None

    def receive_message_ending_with_token(self, active_socket, buffer_size, eof_token):
        """
        Same implementation as in receive_message_ending_with_token() in server.py
        A helper method to receives a bytearray message of arbitrary size sent on the socket.
        This method returns the message WITHOUT the eof_token at the end of the last packet.
        :param active_socket: a socket object that is connected to the server
        :param buffer_size: the buffer size of each recv() call
        :param eof_token: a token that denotes the end of the message.
        :return: a bytearray message with the eof_token stripped from the end.
        """
        #print("in receive_message_ending_with_token:client")
       
        response= bytearray()
        while True:
            server_dir= active_socket.recv(buffer_size)
        
            #print(f"sentserver dir :{server_dir}")
           
            if server_dir[-11:]== eof_token:
                
                response += server_dir[:-11]
                break
            response+=server_dir
        #print(f"dir from client:{response.decode()}")
        return response.decode()



    def initialize(self, host, port):
        """
        1) Creates a socket object and connects to the server.
        2) receives the random token (10 bytes) used to indicate end of messages.
        3) Displays the current working directory returned from the server (output of get_working_directory_info() at the server).
        Use the helper method: receive_message_ending_with_token() to receive the message from the server.
        :param host: the ip address of the server
        :param port: the port number of the server
        :return: the created socket object
        :return: the eof_token
        """

        # print('Connected to server at IP:', host, 'and Port:', port)

        # print('Handshake Done. EOF is:', eof_token)

        mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mysocket.connect((host, port))
        eof_token = mysocket.recv(1024)
        print('Connected to server at IP:', host, 'and Port:', port)
        print('Handshake Done. EOF is:', eof_token.decode())
        current_directory_server = self.receive_message_ending_with_token(mysocket,1024,eof_token)
        print(current_directory_server)
        return (mysocket,eof_token)

            
        



       



    def issue_cd(self, command_and_arg, client_socket, eof_token):
        """
        Sends the full cd command entered by the user to the server. The server changes its cwd accordingly and sends back
        the new cwd info.
        Use the helper method: receive_message_ending_with_token() to receive the message from the server.
        :param command_and_arg: full command (with argument) provided by the user.
        :param client_socket: the active client socket object.
        :param eof_token: a token to indicate the end of the message.
        """
        #print(f"in issue cd and cmd:{command_and_arg}")
        #print(f"client socket:{client_socket}")
       # client_socket.
        final_user_cmd = command_and_arg.encode()+eof_token
        client_socket.sendall(final_user_cmd)




    def issue_mkdir(self, command_and_arg, client_socket, eof_token):
        """
        Sends the full mkdir command entered by the user to the server. The server creates the sub directory and sends back
        the new cwd info.
        Use the helper method: receive_message_ending_with_token() to receive the message from the server.
        :param command_and_arg: full command (with argument) provided by the user.
        :param client_socket: the active client socket object.
        :param eof_token: a token to indicate the end of the message.
        """
        final_user_cmd = command_and_arg.encode()+eof_token
        client_socket.sendall(final_user_cmd)



        #raise NotImplementedError('Your implementation here.')

    def issue_rm(self, command_and_arg, client_socket, eof_token):
        """
        Sends the full rm command entered by the user to the server. The server removes the file or directory and sends back
        the new cwd info.
        Use the helper method: receive_message_ending_with_token() to receive the message from the server.
        :param command_and_arg: full command (with argument) provided by the user.
        :param client_socket: the active client socket object.
        :param eof_token: a token to indicate the end of the message.
        
        """
        final_user_cmd = command_and_arg.encode()+eof_token
        client_socket.sendall(final_user_cmd)

        #raise NotImplementedError('Your implementation here.')

    def issue_ul(self, command_and_arg, client_socket, eof_token):
        """
        Sends the full ul command entered by the user to the server. Then, it reads the file to be uploaded as binary
        and sends it to the server. The server creates the file on its end and sends back the new cwd info.
        Use the helper method: receive_message_ending_with_token() to receive the message from the server.
        :param command_and_arg: full command (with argument) provided by the user.
        :param client_socket: the active client socket object.
        :param eof_token: a token to indicate the end of the message.
        """
        raise NotImplementedError('Your implementation here.')

    def issue_dl(self, command_and_arg, client_socket, eof_token):
        """
        Sends the full dl command entered by the user to the server. Then, it receives the content of the file via the
        socket and re-creates the file in the local directory of the client. Finally, it receives the latest cwd info from
        the server.
        Use the helper method: receive_message_ending_with_token() to receive the message from the server.
        :param command_and_arg: full command (with argument) provided by the user.
        :param client_socket: the active client socket object.
        :param eof_token: a token to indicate the end of the message.
        :return:
        """
        final_user_cmd = command_and_arg.encode()+eof_token
        client_socket.sendall(final_user_cmd)

        file_content = bytearray()
        while True:
            packet = client_socket.recv(1024)
            if packet[-11:] == eof_token:
                file_content += packet[:-11]
                break
            file_content += packet
        

    def issue_info(self,command_and_arg, client_socket, eof_token):
        """
        Sends the full info command entered by the user to the server. The server reads the file and sends back the size of
        the file.
        Use the helper method: receive_message_ending_with_token() to receive the message from the server.
        :param command_and_arg: full command (with argument) provided by the user.
        :param client_socket: the active client socket object.
        :param eof_token: a token to indicate the end of the message.
        :return: the size of file in string
        """
        raise NotImplementedError('Your implementation here.')


    def issue_mv(self,command_and_arg, client_socket, eof_token):
        """
        Sends the full mv command entered by the user to the server. The server moves the file to the specified directory and sends back
        the updated. This command can also act as renaming the file in the same directory. 
        Use the helper method: receive_message_ending_with_token() to receive the message from the server.
        :param command_and_arg: full command (with argument) provided by the user.
        :param client_socket: the active client socket object.
        :param eof_token: a token to indicate the end of the message.
        """
        raise NotImplementedError('Your implementation here.')

    def start(self):
        """
        1) Initialization
        2) Accepts user input and issue commands until exit.
        """
        # initialize
       
        client_socket,eof_token=self.initialize(self.host,self.port)
        #client_socket.sendall(b'heee')

        #print(f"Sock is: {sock} ")

        #print(f"TOKEN IS:{eof_token}")
        while True:
            #print("next round")
            user_input = input("Enter your command:")
            if user_input=="exit": 
                client_socket.close()
                break
            else:
                #call the corresponding command function or exit
                #print("in else")

                cmd = user_input.split()
                #print(f"cmd given by you is:{cmd}")
                if cmd[0] == "cd":
                    #print("in cd")
                    self.issue_cd(user_input,client_socket,eof_token)

                elif cmd[0] == "mkdir":
                    self.issue_mkdir(user_input,client_socket,eof_token)

                elif cmd[0] == "rm":
                    self.issue_rm(user_input,client_socket,eof_token)
                elif cmd[0] == "mv":
                    self.issue_mv(user_input,client_socket,eof_token)
                elif cmd[0] == "dl":
                    self.issue_dl(user_input,client_socket,eof_token)
                elif cmd[0] == "ul":
                    self.issue_ul(user_input,client_socket,eof_token)
                elif cmd[0] == "info":
                    self.issue_info(user_input,client_socket,eof_token)
                    # elif cmd == "exit":
                    #     self.issue_info(user_input.decode(),client_socket,eof_token)
                
                cwd = self.receive_message_ending_with_token(client_socket,1024,eof_token) 
                print(cwd)

        print('Exiting the application.')





        
       
               
                    
            


def run_client():
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 65432  # The port used by the server

    client = Client(HOST, PORT)
    client.start()


if __name__ == '__main__':
    run_client()
