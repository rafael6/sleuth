#!/usr/bin/env python3

__author__ = 'rafael'
__version__ = '0.0.0'

from toolkit import Toolkit
import validators
import readline

# TODO sudo pip3 install validators
# TODO set internal and external DNS servers
# TODO place package in /usr/local/bin

external_dns = ('8.8.8.8',)
intenal_dns = ('8.8.8.8',)


def dns_handler(f):
    def wrapper():
        int_choices = ('', 'i', 'int', 'internal')
        ext_choices = ('e', 'ext', 'external')

        hostname = input('Hostname > ')

        if hostname == '':
            print('Must enter a hostname or IP address; try again.')
            main()
        resolver = input('Enter DNS server [int] or ext > ').lower()
        if resolver in int_choices:
            resolver = intenal_dns
        elif resolver in ext_choices:
            resolver = external_dns
        else:
            print('Not a valid selection; try again.')
            main()
        query_type = input('Enter query type [A-Record], CNAME, MX, PTR > ').lower()
        if query_type == '':
            query_type = 'a'
        f(hostname, resolver, query_type)
        tool.dns_data = None
        main()
    return wrapper


def ping_handler(f):
    def wrapper():
        try:
            hostname = input('Hostname > ')
            if hostname == '':
                print('Must enter a hostname or IP address; try again.')
                main()

            echos = input('Enter number of echo requests [9] > ')
            if echos == '':
                echos = '9'
            assert 1 <= int(echos) <= 10000, '10,000 pings maximum.'

            mtu = input('Enter frame MTU [1000] > ')
            if mtu == '':
                mtu = '1000'
            assert 56 <= int(mtu) <= 10000, 'frame-size must be from 56-1500.'
        except ValueError:
            print('Invalid input; try again.')
            main()
        except AssertionError as e:
            print(e)
            main()
        f(hostname, int(echos), int(mtu))
        tool.loss_data = None
        tool.rtt_data = None
        main()
    return wrapper


def socket_handler(f):
    def wrapper():
        hostname = input('Hostname > ')
        if hostname == '':
            print('Must enter a hostname or IP address; try again.')
            main()
        port = input('Enter a port (Example: t80, u3852) > ')
        try:
            assert port[0].lower() == 'u' or port[0].lower() == 't',\
                'Port must be prepended with u or t; you entered {}.'.format(port)
            int(port[1:])
        except AssertionError as e:
            print(e)
            main()
        except ValueError:
            print('Port must be a number in the range of 0-65535')
            main()
        f(hostname, port)
        tool.socket_data = None
        main()
    return wrapper


def url_handler(f):
    def wrapper():
        url = input('URL > ').lower()
        if validators.url(url):
            f(url)
        else:
            print('Enter a valid URL.')
        tool.http_data = None
        main()
    return wrapper


def curl_handler(f):
    def wrapper():
        uri = input('URL > ').lower()
        if validators.url(uri):
            user_input = input('FQDN for additional header [no] > ').lower()
            if user_input == '' or user_input == 'no' or user_input == 'n':
                extra_fqdn = None
            else:
                extra_fqdn = user_input
            f(uri, extra_fqdn)
        else:
            print('Enter a valid URL.')
        tool.header_data = None
        main()
    return wrapper


@dns_handler
def get_dns(node, nservers, qtype):
    result = tool.check_dns(node, nservers, qtype)
    print('Record: {}  Resolution: {}'.format(node, result))


@ping_handler
def get_ping(node, count=9, mtu=1000):
    tool.check_ping(node, count, mtu)
    print('Host: {}  Loss: {}  RTT(ms): {}'.format(node, tool.loss_data, tool.rtt_data))


@socket_handler
def get_socket(node, prt):
    result = tool.check_socket(node, prt)
    print('Host: {}  Port: {}  Status: {}'.format(node, prt, result))


@url_handler
def get_url(site):
    status = tool.check_http_code(site)
    print('URI: {}  Status: {}'.format(site, status))


@curl_handler
def get_http_heather(uri, extra_fqdn=None):
    header = tool.check_header(uri, extra_fqdn)
    print('URL: {}  Status: {}'.format(uri, header))


def main():
    menu = {1: 'DNS', 2: 'PING', 3: 'SOCKET', 4: 'HTTP CODE', 5: 'HTTP HEADER', 6: 'EXIT'}
    invalid_msg = '\nInvalid selection; try again or Ctrl-C to exit.'

    print('''\033[1m\033[91m
                             (((Gohan)))\033[0m
           \033[1mEnter a number for selection or Ctrl-C to exit.\033[0m''')

    for key, val in sorted(menu.items()):
        print('\t', key, ': ', val, sep='')

    try:
        option = int(input('Enter selection number> '))
        selection = menu.get(
            option, invalid_msg)
        if selection == 'DNS':
            get_dns()
        elif selection == 'PING':
            get_ping()
        elif selection == 'SOCKET':
            get_socket()
        elif selection == 'HTTP CODE':
            get_url()
        elif selection == 'HTTP HEADER':
            get_http_heather()
        elif selection == 'EXIT':
            print('\nGoodbye')
            exit()
        else:
            print(selection)
    except ValueError:
        print(invalid_msg)
        main()
    except KeyboardInterrupt:
        print('\nGoodbye')
        exit()

if __name__ == "__main__":
    tool = Toolkit()
    main()