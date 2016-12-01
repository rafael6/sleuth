#!/usr/bin/env python3

__author__ = 'rafael'
__version__ = '0.0.0'

from toolkit import Toolkit

# TODO place package in /usr/local/bin


class NetElement:
    def __init__(self, name, element_kind, **kwargs):
        self.Toolkit = Toolkit()
        self.name = name
        self.element_kind = element_kind
        self.nservers = kwargs['dns_servers']
        self.ports = kwargs['ports']
        self.urls = kwargs['urls']
        self.qtypes = kwargs['dns_types']
        self.note = kwargs['note']
        #self._ping_result = None
        self._packet_loss = None
        self._rtt = None
        self._socket_result = None
        self._url_result = None
        self._dns_result = None
        self._data = []
        try:
            assert type(self.name) is str,\
                'Validation error; expected a string for hostname, received {}.'\
                .format(type(self.name))

            assert type(self.element_kind) is str,\
                'Validation error; expected a str for element kind, received {}.'\
                .format(type(self.element_kind))

            assert type(self.note) is str or self.note is None,\
                'Validation error; expected a string for note, received {}.'\
                .format(type(self.note))

            assert type(self.qtypes) is tuple or self.qtypes is None,\
                'Validation error; expected a tuple for qtypes, received {}.'\
                .format(type(self.qtypes))

            assert type(self.nservers) is tuple or self.nservers is None,\
                'Validation error; expected a tuple for URLs, received {}.'\
                .format(type(self.nservers))

            assert type(self.nservers) == type(self.qtypes),\
                'Validation error; both nservers & qtypes should be set or None,'\
                'received {} {}.'.format(type(self.nservers), type(self.qtypes))

            assert type(self.ports) is tuple or self.ports is None,\
                'Validation error; expected a tuple for ports; received {}'\
                    .format(type(self.ports))

            assert type(self.urls) is tuple or self.urls is None,\
                'Validation error; expected a tuple for URLs, received {}.'\
                .format(type(self.urls))
        except AssertionError as e:
            print(e)
            exit()

    def reset_attributes(self):
        self._packet_loss = None
        self._rtt = None
        self._socket_result = None
        self._url_result = None
        self._dns_result = None
        self._data = []

    def __str__(self):
        self.load_data()
        _results = '\n\t'.join(self._data)
        #self._data.clear()
        self.reset_attributes()
        return _results

    def get_dns(self):
        self._dns_result =['DNS {} record: {}'.format(qtype.upper(), self.Toolkit.check_dns(
            self.name, self.nservers, qtype)) for qtype in self.qtypes]
        return self._dns_result

    def get_ping(self):
        _output = self.Toolkit.check_ping(self.name)
        try:
            self._packet_loss = 'Packet loss: {}'.format(_output.split(',')[0])
            self._rtt = _output.split(',')[1]
        except IndexError:
            return 'connection error'
        return self._packet_loss

    def get_rtt(self):
        return 'Latency (RTTms): {}'.format(self._rtt)

    def get_socket(self):
        self._socket_result = ['Port {}: {}'.format(port, self.Toolkit.check_socket(
            self.name, port)) for port in self.ports]
        return self._socket_result

    def get_url(self):
        self._url_result = ['URL {}: {}'.format(url, self.Toolkit.check_http_code(
            url)) for url in self.urls]
        return self._url_result

    def load_data(self):
        self._data.append('\nElement: '+self.name)

        self._data.append('Type: '+self.element_kind)

        if self.nservers is not None and self.qtypes is not None:
            self._data.append('\n\t'.join(self.get_dns()))

        self._data.append(self.get_ping())

        self._data.append(self.get_rtt())

        if self.ports is not None:
            self._data.append('\n\t'.join(self.get_socket()))

        if self.urls is not None:
            self._data.append('\n\t'.join(self.get_url()))

        if self.note is not None:
            self._data.append('Notes: '+self.note)


def main():

    google = NetElement('google.com',
                        'Web server',
                        dns_types=('a',),
                        dns_servers=('8.8.8.8',),
                        ports=('t80', 't443'),
                        urls=('http://www.google.com', 'https://google.com'),
                        note=None)

    print(google)


if __name__ == '__main__':
    main()
