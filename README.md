# sleuth

Module toolkit, class Toolkit()

A collection of tools (methods) for testing network related attributes on IP elements. To this point, toolkit includes the tools for the following:

Packet loss.
Delay.
DNS queries including A records, C-Names, PTR records, and MX records.
Socket availability, both TCP and UDP.
HTTP information such as HTTP version, redirect information, and HTTP status code.
SSH client for authentication, shell command(s) execution, and command output capture on a remote IP element.

Module element, class NetElement():

An element factory, element is defined as an IP entity with a set of attributes and the status of such attributes; for instance:

Element: google.com
	Type: Web server
	DNS A record: 74.125.138.101, 74.125.138.102, 74.125.138.113
	Packet loss: 0%
	Latency (RTTms): 27.987
	Port t80: open
	Port t443: open
	URL http://www.google.com: HTTP/1.1 200 OK
	URL https://google.com: HTTP/1.1 301 Moved Permanently -> Location: https://www.google.com/ -> HTTP/1.1 200 OK
	Note: No notes for this node.
  
  
Sleuth leverages Linux, a series of standard and third party Python libraries such as socket, subprocess, urllib, and dnspython.
