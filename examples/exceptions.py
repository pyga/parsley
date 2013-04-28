"""
A grammar for parsing a tiny HTML-like language, plus a transformer for it.
"""
from parsley import makeGrammar, term, termMaker as t, unwrapGrammar
from itertools import chain

tinyHTMLGrammar = r"""

name = <letterOrDigit+>

tag = ((('<' spaces name:n spaces attribute*:attrs '>')
         html:c
         ('<' '/' token(n) spaces '>')
             -> t.Element(n.lower(), dict(attrs), c))) ^ (valid tag)

html = (text | tag)*

text = <(~('<') anything)+>

attribute = spaces name:k token('=') quotedString:v -> (k, v)

quotedString = ((('"' | '\''):q <(~exactly(q) anything)*>:xs exactly(q))
                     -> xs)

"""
TinyHTML = makeGrammar(tinyHTMLGrammar, globals(), name="TinyHTML")

testSource = "<html<title>Yes</title><body><h1>Man, HTML is <i>great</i>.</h1><p>How could you even <b>think</b> otherwise?</p><img src='HIPPO.JPG'></img><a href='http://twistedmatrix.com'>A Good Website</a></body></html>"

print unwrapGrammar(TinyHTML)(testSource).apply('tag')

# The "tag" rule uses the custom label construct "^ (valid tag)".
# When this rule fails, the exception raised will say
# "expected a valid tag".
#
# <html<title>Yes</title><body><h1>Man, HTML is <i>great</i>.</h1><p>How could you even <b>think</b> otherwise?</p><img src='HIPPO.JPG'></img><a href='http://twistedmatrix.com'>A Good Website</a></body></html>
# ^
# Parse error at line 1, column 5: expected a valid tag. trail: [name attribute tag]
