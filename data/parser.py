import sys, json

fileName = sys.argv[1]

f = open(fileName, "r")
out = open(fileName[0:len(fileName) - 5] + "_parsed.txt", "w")
dictionaryOut = open(fileName[0:len(fileName) - 5] + "_count.json", "w")

data = json.load(f)

notFoundChar = "-1"

#Reference:
#IP.SRC (IP), IP.DST (IP), IP.FLAGS (hex), IP.PROTOCOL (int), TCP.SRCPORT (int), TCP.DSTPORT (int), TCP.FLAGS (hex), UDP.SRCPORT (int), UDP.DSTPORT (int)

dictionary = {}

for i in data:

    packet = []

    #IP.SRC
    try:
        IPSrc = i['_source']['layers']['ip']['ip.src']
    except:
        IPSrc = notFoundChar
    #packet.append(IPSrc)
    
    #IP.DST
    try:
        IPDst = i['_source']['layers']['ip']['ip.src']
    except:
        IPDst = notFoundChar    
    #packet.append(IPDst)

    #IP.FLAGS
    try:
        IPFlags = i['_source']['layers']['ip']['ip.flags']
    except:
        IPFlags = notFoundChar
    packet.append(IPFlags)

    #IP.PROTOCOL
    try:
        IPProtocol = i['_source']['layers']['ip']['ip.proto']
    except:
        IPProtocol = notFoundChar
    packet.append(IPProtocol)

    #TCP.SRCPORT
    try:
        TCPSrcPort = i['_source']['layers']['tcp']['tcp.srcport']
    except:
        TCPSrcPort = notFoundChar
    packet.append(TCPSrcPort)

    #TCP.DSTPORT
    try:
        TCPDstPort = i['_source']['layers']['tcp']['tcp.dstport']
    except:
        TCPDstPort = notFoundChar
    packet.append(TCPDstPort)

    #TCP.FLAGS
    try:
        TCPFlags = i['_source']['layers']['tcp']['tcp.flags']
    except:
        TCPFlags = notFoundChar
    packet.append(TCPFlags)

    #UDP.SRCPORT
    try:
        UDPSrcPort = i['_source']['layers']['udp']['udp.srcport']
    except:
        UDPSrcPort = notFoundChar
    packet.append(UDPSrcPort)

    #UDP.DSTPORT
    try:
        UDPDstPort = i['_source']['layers']['udp']['udp.dstport']
    except:
        UDPDstPort = notFoundChar
    packet.append(UDPDstPort)

    #print(packet)

    out.write(" ".join(packet))
    out.write("\n")

    try:
        dictionary[str(packet)] = dictionary[str(packet)] + 1
    except:
        dictionary[str(packet)] = 1

dictionary = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse = True))
json.dump(dictionary, dictionaryOut, indent = 4)
f.close
out.close()
dictionaryOut.close()