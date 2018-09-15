# Description

A test harness written in Python using Scapy to test iptables firewall rules.

Note the `run-tests.sh` script is just an example script, which uses vagrant machines that apply the rules
and the host running the tests against them.

The file `usr_local_bin_firewall.tmpl` is a mustache template (originally used by CFEngine3) of a shell script
that creates the iptables rules that are to be tested.

# Requirements

## Host: For testing the firewall rules

* Python 2.x
* Python 2.x modules
  * xmlrunner
  * scapy
  * netfilterqueue
* libnetfilter

## Guest: For testing the firewall rules

* Python 2.x
* Python 2.x modules
  * xmlrunner
  * scapy
* tcpdump (required for scapy's sniff)

Note that things above are required on the system that will run the tests and
on which the firewall rules are applied.
