grammar = """

digit = anything:x ?(x.isdigit())
nonzeroDigit = anything:x ?(x != '0' and x.isdigit())
digits = <'0' | nonzeroDigit digit*>:i -> int(i)

netstring = digits:length ':' <anything{length}>:string ',' -> string

initial = netstring:string -> state.netstringReceived(string)

"""

class NetstringSender(object):
    def __init__(self, transport):
        self.transport = transport

    def sendNetstring(self, string):
        self.transport.write('%d:%s,' % (len(string), string))
