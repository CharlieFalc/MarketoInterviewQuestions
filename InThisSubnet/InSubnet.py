import socket
import binascii
import optparse


def ip_in_subnetwork(ip_address, subnetwork):
    ip_lower, ip_upper = subnetwork_to_ip_range(subnetwork)
    return ip_lower <= ip_address <= ip_upper


def subnetwork_to_ip_range(subnetwork):
    fragments = subnetwork.split('/')
    network_prefix = fragments[0]
    netmask_len = int(fragments[1])
    ip_len = 32

    suffix_mask = (1 << (ip_len - netmask_len)) - 1
    netmask = ((1 << ip_len) - 1) - suffix_mask
    ip_hex = socket.inet_pton(socket.AF_INET, network_prefix)
    ip_lower = int(binascii.hexlify(ip_hex), 16) & netmask
    ip_upper = ip_lower + suffix_mask

    return ip_lower, ip_upper


def readCommandLineFlags():
    parser = optparse.OptionParser()
    parser.add_option("-f", "--file", dest="input",
                      help="read IPs and subnet pairs from FILE", metavar="FILE")
    parser.add_option("-o", "--output", dest="output",
                      help="write output to FILE", metavar="FILE")
    parser.add_option("-i", type="int", dest="ip",
                      help="specify the hexadecimal representation of the IP address")
    parser.add_option("-s", dest="subnet",
                      help="specify the subnet e.g. '98.210.237.192/26'")
    return parser.parse_args()


def main():
    options, args = readCommandLineFlags()
    # inputs = open("inputs.txt", "r")
    if options.ip and options.subnet:
        if ip_in_subnetwork(options.ip, options.subnet):
            print("The hexadecimal representation of the ip,", options.ip, "is in the subnet", options.subnet)
        else:
            print("The hexadecimal representation of the ip,", options.ip, "is NOT in the subnet", options.subnet)
    elif options.input:
        file = open(options.input, "r")
    else:
        print("Pass either a subnet and an ip or an input file with the subnet ip pairs")

    ip_lower, ip_upper = subnetwork_to_ip_range("98.210.237.192/26")
    print(ip_lower <= 0x62d2edff <= ip_upper)


if __name__ == "__main__":
    main()
