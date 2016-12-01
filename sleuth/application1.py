#!/usr/bin/env python3

import element

__author__ = 'rafael'


google = element.NetElement('google.com',
                    'Web server',
                    dns_types=('a',),
                    dns_servers=('8.8.8.8',),
                    ports=('t80', 't443'),
                    urls=('http://www.google.com', 'https://google.com'),
                    note=None)


def main():
    print('Checking application1; please wait...')
    print(google)


if __name__ == '__main__':
    main()
