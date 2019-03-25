import tkinter as tk
import socket


class Window(tk.Frame):
    """
    Simple program to control the UR10 robot over TCP/IP
    This code is not build for future use, it just shows how commands can be send.
    """
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.socket_inst = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.label_console = tk.Label(self, text="...")
        self.label_r_position = tk.Label(self, text="unknown position")

        # X Y Z position of the robot
        self.r_pos_X = 0.000
        self.r_pos_Y = -0.800
        self.r_pos_Z = 0.500

        # Rotation of the X, Y, Z TCP
        self.r_pos_Rx = 0.000
        self.r_pos_Ry = 3.100
        self.r_pos_Rz = 0.000

        self.r_pos_A = 0.400
        self.r_pos_V = 0.400
        # MAX a=1.3962634015954636, v=1.0471975511965976)

        self.init_window()


#Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("UR10 Movement GUI")
        # allowing the widget to take the full space of the root window
        self.pack(fill=tk.BOTH, expand=1)

        self.label_console.pack()
        self.label_r_position.pack()

        # creating a button instance
        button_quit = tk.Button(self, text="Exit", command=self.client_exit)

        button_connectSocket = tk.Button(self, text="Open connection", command=self.connect_socket)
        button_reconnectSocket = tk.Button(self, text="reconnect", command=self.reconnect_socket)

        button_rSetBasePosition = tk.Button(self, text="set base position", command=self.set_base_position)

        button_rMovePositiveX = tk.Button(self, repeatdelay=500, repeatinterval=1200, text="X +", command=lambda: self.r_move_x_axis("positive"))
        button_rMoveNegativeX = tk.Button(self, repeatdelay=500, repeatinterval=1200, text="X -", command=lambda: self.r_move_x_axis("negative"))

        button_rMovePositiveY = tk.Button(self, repeatdelay=500, repeatinterval=1200, text="Y +", command=lambda: self.r_move_y_axis("positive"))
        button_rMoveNegativeY = tk.Button(self, repeatdelay=500, repeatinterval=1200, text="Y -", command=lambda: self.r_move_y_axis("negative"))

        button_rMovePositiveZ = tk.Button(self, repeatdelay=500, repeatinterval=1200, text="Z +", command=lambda: self.r_move_z_axis("positive"))
        button_rMoveNegativeZ = tk.Button(self, repeatdelay=500, repeatinterval=1200, text="Z -", command=lambda: self.r_move_z_axis("negative"))

        # placing the button on my window
        self.label_r_position.place(x=30, y=30)
        button_quit.place(x=0, y=60)
        button_connectSocket.place(x=0, y=90)
        button_reconnectSocket.place(x=140, y=90)
        button_rSetBasePosition.place(x=0, y=120)

        button_rMoveNegativeX.place(x=0, y=180)
        button_rMovePositiveX.place(x=70, y=180)

        button_rMovePositiveY.place(x=35, y=160)
        button_rMoveNegativeY.place(x=35, y=200)

        button_rMovePositiveZ.place(x=120, y=165)
        button_rMoveNegativeZ.place(x=120, y=195)

    def set_output(self, output_string):
        self.label_console.configure(text=output_string)
        self.label_console.update()

    def client_exit(self):
        """
        Exits the program and closes the socket connection.
        :return:
        """
        self.socket_inst.close()
        exit()

    def reconnect_socket(self):
        self.socket_inst.close()
        self.socket_inst = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_socket()

    def connect_socket(self):
        """
        Opens a socket connection with the robot for communication.
        :return:
        """
        host = "192.168.0.11"            # Ip addres of the robot
        port = 30002                     # Portnr of the robot
        self.socket_inst.settimeout(5)   # 5 seconds
        try:
            self.set_output("Connecting")
            print("Connecting...")
            self.socket_inst.connect((host, port))
        except OSError as error:
            self.set_output("OS error: {0}".format(error))
            print("OS error: {0}".format(error))
            return

        self.r_disable_magnet()
        print(self.socket_inst.recv(1024))

    def get_actual_tcp_pose(self):
        """
        Gives the current position of the robot
        :return:
        """
        # self.socket_inst.send(b"get_actual_tcp_pose()"+ b"\n")
        # data = self.socket_inst.recv(1024)
        # self.label_r_position.configure(text=bytes(data).decode())
        # self.label_r_position.update()

    def set_base_position(self):
        """
        Must be used first. Sets the robot in a hardcoded base position.
        :return:
        """
        self.socket_inst.send(b"movej(p[0.000, -0.800, 0.500, 0.000, 3.1000, 0.0000], a=0.15, v=0.1)" + b"\n")

    def r_enable_magnet(self):
        """
        Enables Digital IO 8
        :return:1
        """
        self.socket_inst.send(b"set_digital_out(8, True)"+ b"\n")

    def r_disable_magnet(self):
        """
        Disables Digital IO 8
        :return:
        """
        self.socket_inst.send(b"set_digital_out(8, False)"+ b"\n")

    def r_move_create_command(self):
        command = "movej(p[" + str(self.r_pos_X) + ", " + str(self.r_pos_Y) + ", " + str(self.r_pos_Z) + ", " \
                  + str(self.r_pos_Rx) + ", " + str(self.r_pos_Ry) + ", " + str(self.r_pos_Rz) + "], " \
                  + str(self.r_pos_A) + ", " + str(self.r_pos_V) + ")" + "\n"
        command = command.encode()
        return command

        # self.socket_inst.send (b"movej(p"
        #                        b"[" + r_pos_X + b", -0.800, 0.500, "
        #                        b"0.000, 3.1000, 0.0000], "
        #                        b"a=0.1962634015954636, v=0.1471975511965976)" + b"\n")


    def r_move_send_command(self, command):
        try:
            self.socket_inst.send(command)
        except OSError as error:
            self.set_output("OS error: {0}".format(error))
            print("OS error: {0}".format(error))
            return False
        return True

    def r_move_x_axis(self, direction):
        """
        Increments the robot on its x axis, True for positive, False for negative
        :return:
        """
        if direction == "positive":
            self.r_pos_X = self.r_pos_X + 0.020
        else:
            self.r_pos_X = self.r_pos_X - 0.020

        if self.r_move_send_command(self.r_move_create_command()):
            self.set_output("Movement " + direction + "  X: " + str(self.r_pos_X))
            print("Movement " + direction + " X: " + str(self.r_pos_X))

    def r_move_y_axis(self, direction):
        """
        Increments the robot on its y axis, True for positive, False for negative
        :return:
        """
        if direction == "positive":
            self.r_pos_Y = self.r_pos_Y + 0.020
        else:
            self.r_pos_Y = self.r_pos_Y - 0.020

        if self.r_move_send_command(self.r_move_create_command()):
            self.set_output("Movement " + direction + "  Y: " + str(self.r_pos_Y))
            print("Movement " + direction + " Y: " + str(self.r_pos_Y))

    def r_move_z_axis(self, direction):
        """
        Increments the robot on its z axis, True for positive, False for negative
        :return:
        """
        if direction == "positive":
            self.r_pos_Z = self.r_pos_Z + 0.020
        else:
            self.r_pos_Z = self.r_pos_Z - 0.020

        if self.r_move_send_command(self.r_move_create_command()):
            self.set_output("Movement " + direction + "  Z: " + str(self.r_pos_Z))
            print("Movement " + direction + " Z: " + str(self.r_pos_Z))


root = tk.Tk()
root.geometry("400x300")

app = Window(root)
root.mainloop()