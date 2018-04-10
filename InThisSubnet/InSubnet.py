import socket
import binascii
import optparse


def ip_in_subnetwork(ip_address, subnetwork):
    ip_lower, ip_upper = subnetwork_to_ip_range(subnetwork)
    return ip_lower <= ip_address <= ip_upper


def subnetwork_to_ip_range(subnetwork):
    CIDRSubnet = subnetwork.split('/')
    network_prefix = CIDRSubnet[0]
    netmask_len = int(CIDRSubnet[1])
    ip_len = 32

    # generate binary mask for the suffix and the prefix (netmask)
    suffix_mask = (1 << (ip_len - netmask_len)) - 1
    netmask = ((1 << ip_len) - 1) - suffix_mask

    # find the hex value of the IPV4 address
    ip_hex = socket.inet_pton(socket.AF_INET, network_prefix)

    # find the integer value of the min ip
    ip_lower = int(binascii.hexlify(ip_hex), 16) & netmask

    # find the integer value of the max ip
    ip_upper = ip_lower + suffix_mask

    return ip_lower, ip_upper


def read_command_line_flags():
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


def read_input_file_for_subnet_ip_pairs(options):
    if options.output:
        output = open(options.output, "w")
    else:
        output = open("output", "w")
    with open(options.input) as f:
        for line in f:
            try:
                ipSubnetPair = line.split(" ")
                hexVal = int(ipSubnetPair[0], 16)
                if ip_in_subnetwork(hexVal, ipSubnetPair[1]):
                    output.write(
                        "The hexadecimal representation of the ip, " + ipSubnetPair[0] + ", is in the subnet " +
                        ipSubnetPair[1])
                else:
                    output.write(
                        "The hexadecimal representation of the ip, " + ipSubnetPair[0] + ", is NOT in the subnet " +
                        ipSubnetPair[1])
            except:
                output.write(
                    "encountered an error while determining if ip in subnet: " + ipSubnetPair[0] +", " +ipSubnetPair[1])


def ip_in_subnetwork_for_command_line_args(options):
    if ip_in_subnetwork(options.ip, options.subnet):
        print("The hexadecimal representation of the ip,", options.ip, "is in the subnet", options.subnet)
    else:
        print("The hexadecimal representation of the ip,", options.ip, "is NOT in the subnet", options.subnet)


def main():
    options, args = read_command_line_flags()
    if options.ip and options.subnet:
        ip_in_subnetwork_for_command_line_args(options)
    elif options.input:
        read_input_file_for_subnet_ip_pairs(options)
    else:
        print("Pass either a subnet and an ip or an input file with the subnet ip pairs")


if __name__ == "__main__":
    main()
