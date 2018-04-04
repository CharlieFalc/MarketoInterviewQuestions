import socket
import binascii


def ip_in_subnetwork(ip_address, subnetwork):

    ip_integer = ip_to_integer(ip_address)
    ip_lower, ip_upper = subnetwork_to_ip_range(subnetwork)

    return ip_lower <= ip_integer <= ip_upper


def ip_to_integer(ip_address):

    ip_hex = socket.inet_pton(socket.AF_INET, ip_address)
    ip_integer = int(binascii.hexlify(ip_hex), 16)

    return ip_integer

    raise ValueError("invalid IP address")


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

    return (ip_lower,
            ip_upper)



def main():
    print(ip_in_subnetwork("98.210.237.75", "98.210.237.192/26"))
    

if __name__ == "__main__":
    main()
