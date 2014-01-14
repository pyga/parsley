"""Parses the output of "free -c 10 -s 1" """

import parsley
import subprocess


def parse_memory_file(payload):
    """Create a grammar that can parse the output of 'free' when called
    with the -c option.
    Return the results as a list of dictionaries of dictionaries """

    memory_grammar = r"""
        memory_reports = memory_report*

        memory_report = headers_line mem_line:m buffers_line:b swap_line:s '\n'
                        -> dict(zip(['memory', 'buffers', 'swap'], [m, b, s]))

        headers_line = ws 'total' ws 'used' ws 'free' ws 'shared' ws
                       'buffers' ws 'cached' '\n'

        mem_line = 'Mem:' ws total:t ws used:u ws free:f ws shared:s ws
                   buffers:b ws cached:c '\n' -> dict([t, u, f, s, b, c])

        buffers_line = '-/+ buffers/cache:' ws used:u ws free:f '\n'
                       -> dict([u, f])

        swap_line = 'Swap:' ws total:t ws used:u ws free:f '\n'
                       -> dict([t, u, f])

        num = <digit+>
        total = num:n -> ('total', n)
        used = num:n -> ('used', n)
        free = num:n -> ('free', n)
        shared = num:n -> ('shared', n)
        buffers = num:n -> ('buffers', n)
        cached = num:n -> ('cached', n)
        """

    memory_parser = parsley.makeGrammar(memory_grammar, {})
    memory_reports = memory_parser(payload).memory_reports()
    return memory_reports


def get_memory_usage():
    """ Call free and save the output to a file"""
    with open('memory_usage.txt', 'w') as memory_file:
        p = subprocess.Popen(['free', '-c', '5', '-s', '1'],
                             stdin=subprocess.PIPE,
                             stdout=memory_file,
                             stderr=memory_file)
        p.communicate()

if __name__ == '__main__':
    get_memory_usage()
    with open('memory_usage.txt', 'r') as memory_file:
        memory_reports = parse_memory_file(memory_file.read())

    for memory_report in memory_reports:
        print memory_report['memory']['free']
        print memory_report['memory']['used']
        print memory_report['swap']['used']
