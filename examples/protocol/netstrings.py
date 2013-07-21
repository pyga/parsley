grammar = """

nonzeroDigit = digit:x ?(x != '0')
digits = <'0' | nonzeroDigit digit*>:i -> int(i)

netstring = digits:length ':' <anything{length}>:string ',' -> string

receiveNetstring = netstring:string -> receiver.netstringReceived(string)

"""

class NetstringSender(object):
    def __init__(self, transport):
        self.transport = transport

    def sendNetstring(self, string):
        self.transport.write('%d:%s,' % (len(string), string))
