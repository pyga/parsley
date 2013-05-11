from parsley import makeGrammar
from parsley_json import jsonGrammar


def traceparse(jsonData):
    trace = []
    def traceit(*a):
        trace.append(a)
    JSONParser = makeGrammar(jsonGrammar, {},
                             tracefunc=traceit)
    return JSONParser(jsonData).top(), trace
