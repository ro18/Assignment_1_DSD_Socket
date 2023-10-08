import socket
import random
from threading import Thread
import os
import shutil
from pathlib import Path
import time
import secrets

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None

    def start(self):
        """
        1) Create server, bind and start listening.
        2) Accept clinet connections and serve the requested commands.

        Note: Use ClientThread for each client connection.
        """
            # Create a socket
            # Bind the socket to the specified address and port

            # Listen for incoming connections

            # print(f"Server listening on {self.host}:{self.port}")

            # while True:
            # Accept incoming connections
            # print(f"Accepted connection from {client_address}")
            # send random eof token

            # try:
            #     # Handle the client requests using ClientThread
            # except Exception as e:
            #     print(f"Error: {e}")
            # finally:
            #     print("Connection closed.")
            #     client_socket.close()

        server_socket =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen()
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            conn, client_address = server_socket.accept()
            #print(f"Accepted connection  {conn}")
            print(f"Accepted connection from {client_address}")
            
            eof_token=self.generate_random_eof_token()
            conn.send(eof_token.encode())
            # Kuser_input = conn.recv(1024).decode()
            # print(f"User sent: {user_input}")
            self.server_socket = conn
            client_thread = ClientThread(self,conn, client_address,eof_token)
            client_thread.start()


                



         

        #raise NotImplementedError("Your implementation here.")




    def get_working_directory_info(self, working_directory):
        """
        Creates a string representation of a working directory and its contents.
        :param working_directory: path to the directory
        :return: string of the directory and its contents.
        """
        dirs = "\n-- " + "\n-- ".join(
            [i.name for i in Path(working_directory).iterdir() if i.is_dir() ]
            
        )
        #print(f"dirs:{dir}")
        files = "\n-- " + "\n-- ".join(
            [i.name for i in Path(working_directory).iterdir() if i.is_file()]
            

        )
        dir_info = f"Current Directory: {working_directory}:\n|{dirs}{files}"
        return dir_info

    def generate_random_eof_token(self):
        """Helper method to generates a random token that starts with '<' and ends with '>'.
        The total length of the token (including '<' and '>') should be 10.
        Examples: '<1f56xc5d>', '<KfOVnVMV>'
        return: the generated token.
        """
        START_TOKEN="<"
        END_TOKEN=">"
        EOF_TOKEN = secrets.token_hex(8)[0:9]
        EOF_TOKEN = START_TOKEN+EOF_TOKEN+END_TOKEN
        return EOF_TOKEN

    def receive_message_ending_with_token(self, active_socket, buffer_size, eof_token):
        """
        Same implementation as in receive_message_ending_with_token() in client.py
        A helper method to receives a bytearray message of arbitrary size sent on the socket.
        This method returns the message WITHOUT the eof_token at the end of the last packet.
        :param active_socket: a socket object that is connected to the server
        :param buffer_size: the buffer size of each recv() call
        :param eof_token: a token that denotes the end of the message.
        :return: a bytearray message with the eof_token stripped from the end.
        """
        #print("in receive_message_ending_with_token:server")
       
        response= bytearray()
        while True:
            client_cmd= active_socket.recv(buffer_size)
           
            if client_cmd[-11:]== eof_token.encode():
                
                response += client_cmd[:-11]
                break
            response+=client_cmd
        #print(f"cmd from client:{response.decode()}")
        return response.decode()


            


    def handle_cd(self, current_working_directory, new_working_directory):
        """
        Handles the client cd commands. Reads the client command and changes the current_working_directory variable
        accordingly. Returns the absolute path of the new current working directory.
        :param current_working_directory: string of current working directory
        :param new_working_directory: name of the sub directory or '..' for parent
        :return: absolute path of new current working directory
        """
        #print(f"in handle_cd:{current_working_directory}:{new_working_directory}")
        #print(f"{current_working_directory}/{new_working_directory}")
        cwd=current_working_directory+"/"+new_working_directory # use path.join here
        #print(f"new dir:{os.path.abspath(cwd)}")

        return os.path.abspath(cwd)

        #raise NotImplementedError("Your implementation here.")

    def handle_mkdir(self, current_working_directory, directory_name):
        """
        Handles the client mkdir commands. Creates a new sub directory with the given name in the current working directory.
        :param current_working_directory: string of current working directory
        :param directory_name: name of new sub directory
        """
        #print(f"in handle_mkdir:{current_working_directory}:{directory_name}")
       # print(f"new dir:{os.path.abspath(current_working_directory)}")
        path = os.path.join(current_working_directory,directory_name)
        os.mkdir(path)
        self.current_directory = path




    def handle_rm(self, current_working_directory, object_name):
        """
        Handles the client rm commands. Removes the given file or sub directory. Uses the appropriate removal method
        based on the object type (directory/file).
        :param current_working_directory: string of current working directory
        :param object_name: name of sub directory or file to remove
        """
        if os.path.isfile(object_name):
            path = os.path.join(current_working_directory,object_name)
            print("path file:{path}")
            os.remove(object_name)

        else:
            path = os.path.join(current_working_directory,object_name)
            print("path dir:{path}")
            os.rmdir(path)

        #self.current_directory = path
        
        #raise NotImplementedError("Your implementation here.")

    def handle_ul(
        self, current_working_directory, file_name, service_socket, eof_tokens ):
        """
        Handles the client ul commands. First, it reads the payload, i.e. file content from the client, then creates the
        file in the current working directory.
        Use the helper method: receive_message_ending_with_token() to receive the message from the client.
        :param current_working_directory: string of current working directory
        :param file_name: name of the file to be created.
        :param service_socket: active socket with the client to read the payload/contents from.
        :param eof_token: a token to indicate the end of the message.
        """
        raise NotImplementedError("Your implementation here.")

    def handle_dl(
        self, current_working_directory, file_name, service_socket, eof_token
    ):
        """
        Handles the client dl commands. First, it loads the given file as binary, then sends it to the client via the
        given socket.
        :param current_working_directory: string of current working directory
        :param file_name: name of the file to be sent to client
        :param service_socket: active service socket with the client
        :param eof_token: a token to indicate the end of the message.
        """

        with open(file_name.decode(), 'rb') as f:
            file_content = f.read()
        file_content_with_token = file_content + eof_token.encode()
        service_socket.sendall(file_content_with_token)


        

    def handle_info(self,current_working_directory, file_name):
        """
        Handles the client info commands. Reads the size of a given file. 
        :param current_working_directory: string of current working directory
        :param file_name: name of sub directory or file to remove
        """
        raise NotImplementedError('Your implementation here.')
    
    def handle_mv(self,current_working_directory, file_name, destination_name):
        """
        Handles the client mv commands. First, it looks for the file in the current directory, then it moves or renames 
        to the destination file depending on the nature of the request.
        :param current_working_directory: string of current working directory
        :param file_name: name of the file tp be moved / renamed
        :param destination_name: destination directory or new filename
        """
        raise NotImplementedError('Your implementation here.')


class ClientThread(Thread):
    def __init__(self, server: Server, service_socket: socket.socket, address: str,eof_token:str):
        Thread.__init__(self)
        self.server_obj = server
        self.service_socket = service_socket
        self.address = address
        self.eof_token=eof_token


    def run(self):
        print ("Connection from : ", self.address)

        # establish working directory
        path="server"
        server=os.path.abspath(path)
        self.current_directory=os.path.dirname(server)
        #print(f"server_directory:{self.current_directory}")
        #self.cwd = self.server_obj.get_working_directory_info(current_directory)
        #print(self.server_obj.get_working_directory_info(self.current_directory))
        #print(self.service_socket.recv(1024).decode())
        self.service_socket.sendall((self.server_obj.get_working_directory_info((self.current_directory))+self.eof_token).encode())
        # send the current dir info

        
        while True:
            
            user_command = self.server_obj.receive_message_ending_with_token(self.service_socket,1024,self.eof_token)
            #print(f"user command :{user_command}")

        # get the command and arguments and call the corresponding method
            cmd=user_command.split()
            #print(f"after split:{cmd[0]}")

            if user_command == "exit": break

            if cmd[0] == "cd":
                #print(cmd)
                self.current_directory=self.server_obj.handle_cd(self.current_directory,cmd[1])
                #print(self.current_directory)
            elif cmd[0] == "mkdir":
                #print(cmd)
                self.server_obj.handle_mkdir(self.current_directory,cmd[1])
                #print(self.current_directory)

            elif cmd[0] == "rm":
                self.server_obj.handle_rm(self.current_directory,cmd[1])
                # elif cmd == "mv":
                #     self.issue_mv(user_command.decode(),client_socket,eof_token)
            elif cmd == "dl":
                self.server_obj.handle_dl(self.current_directory,cmd[1],self.service_socket,self.eof_token)
                # elif cmd == "ul":
                #     self.issue_ul(user_input.decode(),client_socket,eof_token)
                # elif cmd == "info":
                #     self.issue_info(user_input.decode(),client_socket,eof_token)
        # sleep for 1 second
            time.sleep(1) 

        # send current dir info
            dir_info = self.server_obj.get_working_directory_info(self.current_directory)
            #print("final")
            #print(dir_info+self.eof_token)
            self.service_socket.sendall((dir_info+self.eof_token).encode())



        print('Connection closed from:', self.address)


def run_server():
    HOST = "127.0.0.1"
    PORT = 65432

    server = Server(HOST, PORT)
    server.start()


if __name__ == "__main__":
    run_server()
