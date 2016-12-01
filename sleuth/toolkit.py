#!/usr/bin/env python3

__author__ = 'rafael'
__version__ = '0.0.0'

"""
This modules provides methods for checking: DNS, ICMP, sockets, HTTP status code,
HTTP redirect & status information from header, and the ability to execute a
command on a remote system using an SSH session.

>>> from toolkit import Toolkit
>>> tool = Toolkit()
>>> print(tool.check_dns('google.com', ['8.8.8.8'], 'a'))
74.125.138.139 ,74.125.138.102 ,74.125.138.100 ,74.125.138.113 ,74.125.138.101 ,74.125.138.138
>>> print(tool.check_socket('google.com', 't80'))
Open
>>> print(tool.check_ping('yahoo.com', 3, 1500))
0%,66.061
>>> print(tool.check_http_code('https://google.com'))
200
>>> print(tool.check_header('http://yahoo.com'))
HTTP/1.1 301 Redirect -> Location: https://www.yahoo.com/ -> HTTP/1.1 200 OK
>>> print(tool.check_ssh('rafael', 'Levittown', '10.0.1.24', 'uname'))
Darwin
>>>
"""

import dns.resolver
import socket
import subprocess
import urllib.request

# TODO sudo pip3 install dnspython3
# TODO place package in /usr/local/bin


class Toolkit:

    def __init__(self):
        self.dns_data = None
        self.socket_data = None
        self.loss_data = None
        self.rtt_data = None
        self.http_code = None
        self.header_data = None
        self.ssh_data = None

    @property
    def dns_data(self):
        return self.__dns_data

    @dns_data.setter
    def dns_data(self, value):
        self.__dns_data = value

    @dns_data.deleter
    def dns_data(self):
        del self.__dns_data

    @property
    def socket_data(self):
        return self.__socket_data

    @socket_data.setter
    def socket_data(self, value):
        self.__socket_data = value

    @socket_data.deleter
    def socket_data(self):
        del self.__socket_data

    @property
    def loss_data(self):
        return self.__loss_data

    @loss_data.setter
    def loss_data(self, value):
        self.__loss_data = value

    @loss_data.deleter
    def loss_data(self):
        del self.__loss_data

    @property
    def rtt_data(self):
        #print('property', self.__rtt_data)
        return self.__rtt_data

    @rtt_data.setter
    def rtt_data(self, value):
        self.__rtt_data = value
        #print('setter', self.__rtt_data)

    @rtt_data.deleter
    def rtt_data(self):
        #print('deleter', self.__rtt_data)
        del self.__rtt_data

    @property
    def http_code(self):
        return self.__http_code

    @http_code.setter
    def http_code(self, value):
        self.__http_code = value

    @http_code.deleter
    def http_code(self):
        del self.__http_code

    @property
    def header_data(self):
        return self.__header_data

    @header_data.setter
    def header_data(self, value):
        self.__header_data = value

    @header_data.deleter
    def header_data(self):
        del self.__header_data

    @property
    def ssh_data(self):
        return self.__ssh_data

    @ssh_data.setter
    def ssh_data(self, value):
        self.__ssh_data = value

    @ssh_data.deleter
    def ssh_data(self):
        del self.__ssh_data

    def check_dns(self, node, nservers, qtype):
        """
        Process name resolution (DNS) queries on a given node (hostname or IP)
        using a name server from a given container of name servers (nservers),
        and a query type (qtype).

        Sets instance attribute self.dns_data with DNS resolution data or with
        exception details if an exception occurs.

        Returns instance attribute self.dns_data.

        Python module dependencies:
        pip3 install dnspython3 or pip install dnspython

        Example:
            from toolkit import Toolkit
            tool = Toolkit()
            tool.check_dns('google.com', ('8.8.8.8',), 'a')

            print(tool.dns_data)

        :param node: string, IP address or hostname in DNS.
        :param nservers: list of strings, DNS servers.
        :param qtype: string, one of the these query types: A/CNAME, MX, PTR.
        :return: string, DNS resolution data.
        """
        try:
            if type(node) is not str:
                raise TypeError('a string is required')
            if type(nservers) is not tuple:
                if type(nservers) is not list:
                    raise TypeError('a list or tuple is required')
            if type(qtype) is not str:
                raise TypeError('a string is required')
            assert qtype.lower() == 'a' or qtype.lower() == 'mx' or\
            qtype.lower() == 'ptr', 'unrecognized record type'
            _resolver = dns.resolver.Resolver()
            _resolver.nameservers = nservers
            if qtype.lower() == 'mx':
                try:
                    _answer = _resolver.query(node, qtype)
                    _data = ('Host {} preferance {}'.format(
                        rdata.exchange, rdata.preference) for rdata in _answer)
                except Exception:
                    return self.dns_data
            elif qtype.lower() == 'ptr':
                try:
                    _answer = _resolver.query(dns.reversename.from_address(node), qtype)
                    _data = (str(record) for record in _answer)
                except Exception:
                    return self.dns_data
            else:
                # Handles both A and CNAME records
                try:
                    _answer = _resolver.query(node, qtype)
                    _data = (str(address) for address in _answer)
                except Exception:
                    return self.dns_data

        except dns.exception.SyntaxError as e:
            self.dns_data = e  # 'Error; check IP address.'
        except dns.rdatatype.UnknownRdatatype as e:
            self.dns_data = e  # 'Error; check query type.'
        except dns.resolver.NoAnswer as e:
            self.dns_data = e  # 'Error; check query type.'
        except dns.resolver.NXDOMAIN as e:
            self.dns_data = e  # 'Error; check hostname.'
        except dns.exception.Timeout as e:
            self.dns_data = e  # 'Error; check connection & DNS server.'
        except AssertionError as e:
            self.dns_data = e
        except TypeError as e:
            self.dns_data = e
        else:
            self.dns_data = ', '.join(_data)

        return self.dns_data

    def check_socket(self, node, port):
        """
        Check the status of a given socket using node (hostname or IP) and a
        port number prepended with 't' for TCP or with 'u' for UDP.

        Sets instance attribute self.socket_data as 'Open' if the socket is open,
        'Unreachable' if socket is close, or with exception details if an
        exception occurs.

        Return instance attribute self.socket_data.

        Example:
            from toolkit import Toolkit
            tool = Toolkit()
            print(tool.check_socket('yahoo.com', 't80', 'tcp'))

            print(tool.socket_data)

        :param node: string, IP address or hostname in DNS.
        :param port: string, TCP/UDP port number prepended with 't' or 'u'
        :return: string, 'Open', 'Unreachable.'
        """
        try:
            if type(node) is not str:
                raise TypeError('a string is required')
            if type(port) is not str:
                raise TypeError('a string is required')
            assert port[0].lower() == 'u' or port[0].lower() == 't',\
                'port must be prepended with u or t, received {}'.format(port)
            assert 0 < int(port[1:]) < 65536, \
                'port must be an integer 0-65536, received {}'.format(port[1:])
            if port[0].lower() == 't':
                _sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            else:
                _sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            _sock.settimeout(3)  # Set timeout for 3 seconds
            s = _sock.connect_ex((node, int(port[1:])))
            _sock.close()
        except socket.error as e:
            self.socket_data = e
        except OverflowError as e:
            self.socket_data = e
        except AssertionError as e:
            self.socket_data = e
        except TypeError as e:
            self.socket_data = e
        except ValueError as e:
            self.socket_data = e
        else:
            if s == 0:
                self.socket_data = 'open'
            else:
                self.socket_data = 'unreachable'

        return self.socket_data

    def check_ping(self, node, count=9, frame_size=1000):
        """
        Executes a ping shell command in a Linux system with an awk operation
        to capture loss and average RTT counters.

        Sets instance attributes self.loss_data and self.rtt_data with the
        command's output packet-loss and average RTT-delay counters
        respectively, or with exception details if an exception occurs.

        Returns a tuple containing instance variables self.loss_data and
        self.rtt_data.

        Usage:

            from toolkit import Toolkit
            tool = Toolkit()
            print(tool.check_ping('google.com', 3, 56, False)

            print(tool.loss_data)
            print(tool.rtt_data)

        :param node: string, IP address or hostname in DNS.
        :param count: integer, number of echo requests.
        :param frame_size: integer, frame size 56-1500.
        :return: tuple, packet loss and average RTT in ms ('0%', 22.735)
        """
        _interval = '.2'  # 200ms
        try:
            if type(count) is not int or type(frame_size) is not int:
                raise TypeError('an integer is required')
            assert 1 <= count <= 10000, 'count must be from 1-10000'
            assert 56 <= frame_size <= 1500, 'frame-size must be from 56-1500'
            _size = frame_size - 28  # NEW, 20 IP header, 8 ICMP header, in bytes.
            _awk = "awk '/loss/ {loss=$6} /rtt/ {split($4, array, \"/\");" \
                   "print loss \",\" array[2]} /100%/ {print \"100%,Unreachable\"}'"
            _command = "ping -c {} -i {} -s {} {} | {}".format(
                count, _interval, _size, node, _awk)
            _output = subprocess.check_output(_command, shell=True).decode(
                'utf-8').strip()
            _returned_values = _output.split(',')
            assert len(_returned_values) == 2, 'execution error'
        except subprocess.CalledProcessError as e:
            self.loss_data = e
        except AssertionError as e:
            self.loss_data = e
        except TypeError as e:
            self.loss_data = e
        except ValueError as e:
            self.loss_data = e
        else:
            self.loss_data = _returned_values[0]
            self.rtt_data = _returned_values[1]
        return '{},{}'.format(self.loss_data, self.rtt_data)

    def check_http_code(self, url):
        """
        Check the HTTP status of a given URL/URI.

        Sets the value of instance attribute self.http_code with the http code
        from a given URL/URI or with exception details if an exception occurs.

        Returns instance attribute self.http_code.

        Example:
            from toolkit import Toolkit
            tool = Toolkit()
            print(tool.check_http_code('https://google.com'))

            print(tool.http_code)

        :param url: string, URL/URI to check.
        :return: string, HTTP status code.
        """
        try:
            if type(url) is not str:
                raise TypeError('a string is required')
            _connection = urllib.request.urlopen(url)
        except urllib.error.URLError as e:
            self.http_code = e
        except ConnectionResetError as e:
            self.http_code = e
        except TypeError as e:
            self.http_code = e
        except ValueError as e:
            self.http_code = e
        else:
            self.http_code = str(_connection.getcode())

        return self.http_code

    def check_header(self, uri, extra_fqdn=None):
        """
        Execute a CURL command on a UNIX/Linux system to obtain HTTP status
        code and redirect information from the HTTP header.

        Optionally, you can use an extra header. This is useful when the web
        engine renders an URL with something other than its name or IP address
        in the host portion of the URL.

        Sets the value of instance attribute self.header with the command
        output (http code and redirect data if any) or with exception details
        if an exception occurs.

        Returns instance attribute self.header_data.

        Examples:
            from toolkit import Toolkit()
            tool = Toolkit()

            print(tool.check_header('http://yahoo.com'))
            print(tool.check_header('https://www.cnn.com/', 'cnn.com:443:157.166.226.25'))

            print(tool.header_data)

        :param uri: string, URI, hostname, or IP address web services dependant.
        :param record: string, DNS information in the form of hostname:port:ip_address.
        :return: string, containing HTTP code and redirect information from header.
        """
        if extra_fqdn:
            extra_header = '--header "host:{}"'.format(extra_fqdn)
        else:
            extra_header = ''
        command = 'curl -G -I -L -k -s {} {} | egrep "HTTP|Location"'.format(
            extra_header, uri)

        try:
            if type(uri) is not str:
                raise TypeError('a string is required')
            if extra_fqdn is not None:
                if type(extra_fqdn) is not str:
                    raise TypeError('a string is required 1')
            _output1 = subprocess.check_output(command, shell=True).decode('utf-8').strip()
            _output = ' -> '.join(_output1.split('\r\n'))
        except TypeError as e:
            self.header_data = e
        except subprocess.CalledProcessError as e:
            self.header_data = e
        else:
            self.header_data = _output

        return self.header_data

    def check_ssh(self, username, password, node, command):
        """
        Execute a command over a SSH session on a Linux system using a given
        username, password, node (hostname or IP), and a shell command.

        Sets the value of instance attribute self.ssh_data with the command
        output or with exception details if an exception occurs.

        Returns instance attribute self.ssh_data.

        Example:
        from toolkit import Toolkit
        tool = Toolkit()
        print(tool.check_ssh('my_username', 'my_password', '1.1.1.1', 'pwd'))

        print(tool.ssh_data)

        Linux package dependencies
        Package dependencies: sudo apt-get install sshpass

        :param username: string, username
        :param password: string, password
        :param node: string, hostname or IP address
        :param command: string, command to execute
        :return:string, command output
        """
        try:
            if type(username) is not str or type(password) is not str:
                raise TypeError('string is needed')
            if type(node) is not str or type(command) is not str:
                raise TypeError('string is needed')
            _linux_command = 'sshpass -p {} ssh -o StrictHostKeyChecking=no -o ' \
                             'ConnectTimeout=9 {}@{} {}'. format(
                password, username, node, command)
            _output = subprocess.check_output(_linux_command, shell=True).decode('utf-8')
            self.ssh_data = _output.strip()
        except TypeError as e:
            self.ssh_data = e
        except subprocess.CalledProcessError as e:
            self.ssh_data = e

        return self.ssh_data


def main():
    tool = Toolkit()
    print(tool.check_dns('campus.com', ['8.8.8.8'], 'a'))
    print(tool.check_socket('google.com', 't80'))
    print(tool.check_ping('google.com', 3, 56))
    print(tool.check_http_code('https://yahoo.com'))
    print(tool.check_header('http://173.194.219.102', 'www.google.com'))
    print(tool.check_ssh('username', 'password', '1.2.3.4', 'uname'))


if __name__ == "__main__":
    main()

