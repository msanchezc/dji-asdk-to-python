import socket
import json
import threading
import logging

from .message_builder import MessageBuilder


from dji_asdk_to_python.utils.process_message import (
    process_return_type,
    process_error_message,
)

from dji_asdk_to_python.errors import (
    CustomError,
    SocketError,
    JsonError,
    CommunicationError,
)


class SocketUtils:
    APP_PORT = 11111
    FIRST_MESSAGE_LENGTH = 7

    # fmt: off
    @staticmethod
    def getIp():
        return [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
    # fmt: on

    @staticmethod
    def send(
        message,
        app_ip,
        callback,
        timeout,
        return_type,
        blocking=False,
        listener=None
    ):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)  # timeout
        try:
            sock.connect((app_ip, SocketUtils.APP_PORT))
            sock.send(message.encode("utf-8"))
        except socket.error as e:
            return SocketError("%s" % e)
        except socket.timeout as e:
            return SocketError("%s" % e)

        if blocking:
            return SocketUtils.receive(sock, callback, timeout, return_type)
        else:
            if listener is not None:
                t = threading.Thread(
                    target=SocketUtils.listener_receiver, args=[sock, listener]
                )
                t.start()
            else:
                t = threading.Thread(
                    target=SocketUtils.receive,
                    args=[sock, callback, timeout, return_type],
                )
                t.start()

    @staticmethod
    def receive_data_from_sock(sock, timeout):
        sock.settimeout(timeout)  # timeout
        server_message = None
        try:
            sock_file = sock.makefile()
            server_message = sock_file.readline()
            if server_message is not None:
                server_message = json.loads(server_message)
            else:
                server_message = SocketError(
                    "Socket error, packages lost on data")
        except socket.error as e:
            server_message = SocketError("%s" % e)
        except socket.timeout as e:
            server_message = SocketError("%s" % e)
        except UnicodeDecodeError as e:
            server_message = SocketError("%s" % e)
        except json.JSONDecodeError as e:
            server_message = JsonError(
                "%s is malformed: %s" % (server_message, e))
        return server_message

    @staticmethod
    def listener_receiver(sock, listener):
        listener.sock = sock
        timeout = 31536000  # 1 year in seconds
        listener.sock = sock  # link listener with socket
        while listener.running:
            server_message = SocketUtils.receive_data_from_sock(sock, timeout)
            if not listener.running:
                break
            server_message = SocketUtils.parse_message(server_message, None)
            if not listener.running:
                break
            if isinstance(server_message, CustomError):
                logging.error("Bad listener message, error: %s" %
                              server_message)
            from dji_asdk_to_python.utils.listener_utils import (
                process_message_listener
            )
            process_message_listener(listener, server_message)

    @staticmethod
    def parse_message(server_message, return_type):
        result = None
        if server_message[MessageBuilder.SUCCESS] == MessageBuilder.FALSE:
            result = process_error_message(server_message)
        else:
            result = process_return_type(server_message, return_type)
        return result

    @staticmethod
    def receive(sock, callback, timeout, return_type):
        server_message = SocketUtils.receive_data_from_sock(sock, timeout)

        if server_message is None:
            error = CommunicationError("Socket %s returns None" % sock)
            if callback:
                return callback(error)
            else:
                return error

        if isinstance(server_message, CustomError):
            if callback:
                return callback(server_message)
            else:
                return server_message

        result = SocketUtils.parse_message(server_message, return_type)

        sock.close()

        if callback:
            return callback(result)
        else:
            return result
