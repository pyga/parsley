"""
A grammar for parsing a tiny HTML-like language, plus a transformer for it.
"""
from pymeta.grammar import OMeta
from itertools import chain

tinyHTMLGrammar = """

name ::= <letterOrDigit>+:ls => ''.join(ls)

tag ::= ('<' <spaces> <name>:n <spaces> <attribute>*:attrs '>'
         <html>:c
         '<' '/' <token n> <spaces> '>'
             => [n.lower(), dict(attrs), c])

html ::= (<text> | <tag>)*

text ::= (~('<') <anything>)+:t => ''.join(t)

attribute ::= <spaces> <name>:k <token '='> <quotedString>:v => (k, v)

quotedString ::= (('"' | '\''):q (~<exactly q> <anything>)*:xs <exactly q>
                     => ''.join(xs))

"""
TinyHTML = OMeta.makeGrammar(tinyHTMLGrammar, globals(), name="TinyHTML")

def formatAttrs(attrs):
    """
    Format a dictionary as HTML-ish attributes.
    """
    return ''.join([" %s='%s'" % (k, v) for (k, v) in attrs.iteritems()])


unparserGrammar = """
contents ::= [<tag>*:t] => ''.join(t)
tag ::= ([:name :attrs <contents>:t]
            => "<%s%s>%s</%s>" % (name, formatAttrs(attrs), t, name)
         | <anything>)
"""

TinyHTMLUnparser = OMeta.makeGrammar(unparserGrammar, globals(), name="TinyHTMLUnparser")

linkExtractorGrammar = """
contents ::= [<tag>*:t] => list(chain(*t))
tag ::= ( ["a" :attrs ?('href' in attrs) <contents>:t] => ([attrs['href']] + t)
        | ["img" :attrs ?('src' in attrs) <contents>:t] => ([attrs['src']] + t)
        | [:name :attrs <contents>:t] => t
        | :text => [])
"""

LinkExtractor = OMeta.makeGrammar(linkExtractorGrammar, globals(), name="LinkExtractor")

boringifierGrammar = """
contents ::= [<tag>*:t] => list(chain(*t))
tag ::= ( ["b" <anything> <contents>:t] => t
        | ["i" <anything> <contents>:t] => t
        | [:name :attrs <contents>:t] => [[name, attrs, t]]
        | :text => [text])
"""

Boringifier = OMeta.makeGrammar(boringifierGrammar, globals(), name="Boringifier")

testSource = "<html><title>Yes</title><body><h1>Man, HTML is <i>great</i>.</h1><p>How could you even <b>think</b> otherwise?</p><img src='HIPPO.JPG'></img><a href='http://twistedmatrix.com'>A Good Website</a></body></html>"
