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
            print(f"Accepted connection from {client_address}")
            
            eof_token=self.generate_random_eof_token()
            conn.send(eof_token.encode())

            self.server_socket = conn
            client_thread = ClientThread(self,conn, client_address,eof_token)
            client_thread.start()

    def get_working_directory_info(self, working_directory):
        """
        Creates a string representation of a working directory and its contents.
        :param working_directory: path to the directory
        :return: string of the directory and its contents.
        """
        dirs = "\n-- " + "\n-- ".join(
            [i.name for i in Path(working_directory).iterdir() if i.is_dir() ]
            
        )
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
       
        response= bytearray()
        while True:
            client_cmd= active_socket.recv(buffer_size)
           
            if client_cmd[-11:]== eof_token.encode():
                
                response += client_cmd[:-11]
                break
            response+=client_cmd
        return response


            


    def handle_cd(self, current_working_directory, new_working_directory):
        """
        Handles the client cd commands. Reads the client command and changes the current_working_directory variable
        accordingly. Returns the absolute path of the new current working directory.
        :param current_working_directory: string of current working directory
        :param new_working_directory: name of the sub directory or '..' for parent
        :return: absolute path of new current working directory
        """
        cwd=os.path.join(current_working_directory,new_working_directory) 
        return os.path.abspath(cwd)


    def handle_mkdir(self, current_working_directory, directory_name):
        """
        Handles the client mkdir commands. Creates a new sub directory with the given name in the current working directory.
        :param current_working_directory: string of current working directory
        :param directory_name: name of new sub directory
        """

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
        path = os.path.join(current_working_directory,object_name)
        print(f"rm path:{path}")

        if os.path.isfile(os.path.join(current_working_directory,object_name)):
            os.remove(path)

        else:
            shutil.rmtree(path)


    def handle_ul(
        self, current_working_directory, file_name, service_socket, eof_token ):
        """
        Handles the client ul commands. First, it reads the payload, i.e. file content from the client, then creates the
        file in the current working directory.
        Use the helper method: receive_message_ending_with_token() to receive the message from the client.
        :param current_working_directory: string of current working directory
        :param file_name: name of the file to be created.
        :param service_socket: active socket with the client to read the payload/contents from.
        :param eof_token: a token to indicate the end of the message.
        """


        file_content = self.receive_message_ending_with_token(service_socket,1024,eof_token)

        path = os.path.join(current_working_directory,file_name)

        client = os.path.abspath(path)

        with open(client, 'wb') as f:
           f.write(file_content)

    def handle_dl(
        self, current_working_directory, file_name, service_socket, eof_token):
        """
        Handles the client dl commands. First, it loads the given file as binary, then sends it to the client via the
        given socket.
        :param current_working_directory: string of current working directory
        :param file_name: name of the file to be sent to client
        :param service_socket: active service socket with the client
        :param eof_token: a token to indicate the end of the message.
        """
        file_content = bytearray()
        filepath = os.path.join(current_working_directory,file_name)
        with open(filepath, 'rb') as f:
            file_content = f.read()

        file_content_with_token = file_content + eof_token.encode()
        service_socket.sendall(file_content_with_token)


        

    def handle_info(self,current_working_directory, file_name,service_socket,eof_token):
        """
        Handles the client info commands. Reads the size of a given file. 
        :param current_working_directory: string of current working directory
        :param file_name: name of sub directory or file to remove
        :param service_socket: active service socket with the client
        :param eof_token: a token to indicate the end of the message.
        """

        file_content = bytearray()
        filepath = os.path.join(current_working_directory,file_name)
        with open(filepath, 'rb') as f:
            file_content = f.read()

        file_size = str(len(file_content))
        service_socket.sendall((file_size+eof_token).encode())
    
    def handle_mv(self,current_working_directory, file_name, destination_name):
        """
        Handles the client mv commands. First, it looks for the file in the current directory, then it moves or renames 
        to the destination file depending on the nature of the request.
        :param current_working_directory: string of current working directory
        :param file_name: name of the file tp be moved / renamed
        :param destination_name: destination directory or new filename
        """
        original_filepath = os.path.join(current_working_directory,file_name)

        found=False
        for root,dirs,files in os.walk(os.path.abspath(current_working_directory)):
            for name in dirs:
                if name == destination_name[:-1]:
                    found=True
                    new_path = os.path.join(root,name)
                    shutil.move(original_filepath,new_path)
                    self.current_directory= name
                    break

  

        if found == False:
            for root,dirs,files in os.walk(os.path.abspath(current_working_directory)):
                for name in files:

                    if name == file_name:
                        new_path = os.path.join(current_working_directory,destination_name)
                        os.rename(original_filepath,new_path)


class ClientThread(Thread):
    def __init__(self, server: Server, service_socket: socket.socket, address: str,eof_token:str):
        Thread.__init__(self)
        self.server_obj = server
        self.service_socket = service_socket
        self.address = address
        self.eof_token=eof_token


    def run(self):
        print ("Connection from : ", self.address)
        self.current_directory=os.path.dirname(__file__)
        self.service_socket.sendall((self.server_obj.get_working_directory_info((self.current_directory))+self.eof_token).encode())

        
        while True:
            
            user_command = self.server_obj.receive_message_ending_with_token(self.service_socket,1024,self.eof_token)
            cmd=user_command.decode().split()

            if user_command == "exit": break

            if cmd[0] == "cd":
                self.current_directory=self.server_obj.handle_cd(self.current_directory,cmd[1])

            elif cmd[0] == "mkdir":
                self.server_obj.handle_mkdir(self.current_directory,cmd[1])

            elif cmd[0] == "rm":
                self.server_obj.handle_rm(self.current_directory,cmd[1])

            elif cmd[0] == "mv":
                self.server_obj.handle_mv(self.current_directory,cmd[1],cmd[2])

            elif cmd[0] == "dl":
                self.server_obj.handle_dl(self.current_directory,cmd[1],self.service_socket,self.eof_token)
                
            elif cmd[0] == "ul":
                self.server_obj.handle_ul(self.current_directory,cmd[1],self.service_socket,self.eof_token)

            elif cmd[0] == "info":
                self.server_obj.handle_info(self.current_directory,cmd[1],self.service_socket,self.eof_token)

            time.sleep(1) 

            dir_info = self.server_obj.get_working_directory_info(self.current_directory)

            self.service_socket.sendall((dir_info+self.eof_token).encode())



        print('Connection closed from:', self.address)


def run_server():
    HOST = "127.0.0.1"
    PORT = 65432

    server = Server(HOST, PORT)
    server.start()


if __name__ == "__main__":
    run_server()
