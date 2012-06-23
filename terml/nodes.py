import itertools
from collections import namedtuple

_Term = namedtuple("Term", "tag data args span")
class Term(_Term):
    def __new__(cls, tag, data, args, span):
        #XXX AstroTag tracks (name, tag_code) and source span
        if data and not isinstance(data, (str, unicode, int, long, float)):
            raise ValueError("Term data can't be of type %r" % (type(data),))

        if data and args:
            raise ValueError("Term %s can't have both data and children" % (tag,))

        if args is None:
            args = ()
        return _Term.__new__(cls, tag, data, args, span)


    def __eq__(self, other):
        return (     self.tag, self.data, self.args
               ) == (other.tag, other.data, other.args)


    def __repr__(self):
        return "term('%s')" % (self._unparse(4).replace("'", "\\'"))


    def _unparse(self, indentLevel=0):
        newlineAndIndent = '\n' + (' ' * indentLevel)
        if self.data:
            if self.tag.name == '.String.':
                return '"%s"' % self.data
            elif self.tag.name == '.char.':
                return "'%s'" % self.data
            else:
                return str(self.data)
        if len(self.args) == 0:
            return self.tag._unparse(indentLevel)
        args = ', '.join([a._unparse() for a in self.args])
        if self.tag.name == '.tuple.':
            return "[%s]" % (args,)
        elif self.tag.name == '.attr.':
            return "%s: %s" % (self.args[0]._unparse(indentLevel),
                               self.args[1]._unparse(indentLevel))
        elif self.tag.name == '.bag.':
            return "{%s}" % (args,)
        elif len(self.args) == 1 and self.args[0].tag.name == '.bag.':
            return "%s%s" % (self.tag._unparse(indentLevel), args)
        else:
            return "%s(%s)" % (self.tag._unparse(indentLevel), args)

    def withSpan(self, span):
        return Term(self.tag, self.data, self.args, span)


    def build(self, builder):
        if self.data is None:
            f = builder.leafTag(self.tag, self.span)
        else:
            f = builder.leafData(self.data, self.span)

        args = builder.empty()
        for arg in self.args:
            val = arg.build(builder)
            args = builder.seq(args, val)
        return builder.term(f, args)


    def __cmp__(self, other):
        tagc = cmp(self.tag, other.tag)
        if tagc:
            return tagc
        datac = cmp(self.data, other.data)
        if datac:
            return datac
        return cmp(self.args, other.args)

    def __int__(self):
        return int(self.data)

    def __float__(self):
        return float(self.data)

    def _substitute(self, map):
        (f, data) = _asTag(self.tag._substitute(map)[0])
        args = tuple(itertools.chain.from_iterable(a._substitute(map) for a in self.args))
        term = Term(f, data or self.data, args, self.span)
        return [term]

    def substitute(self, map):
        return self._substitute(map)[0]


class Tag(object):
    def __init__(self, name):
        if name[0] == '':
            import pdb; pdb.set_trace()
        self.name = name

    def __eq__(self, other):
        return other.__class__ == self.__class__ and self.name == other.name

    def __repr__(self):
        return "Tag(%r)" % (self.name,)

    def _unparse(self, indentLevel=0):
        return self.name

    def _substitute(self, map):
        return [self]



def coerceToTerm(val):
    from ometa.runtime import character, unicodeCharacter
    from terml.twine import TwineText, TwineBytes
    if isinstance(val, Term):
        return val
    if val is None:
        return Term(Tag("null"), None, None, None)
    if val is True:
        return Term(Tag("true"), None, None, None)
    if val is False:
        return Term(Tag("false"), None, None, None)
    if isinstance(val, (int, long)):
        return Term(Tag(".int."), val, None, None)
    if isinstance(val, float):
        return Term(Tag(".float64."), val, None, None)
    if isinstance(val, (character, unicodeCharacter)):
        return Term(Tag(".char."), val, None, None)
    if isinstance(val, (TwineText, TwineBytes)):
        return Term(Tag(".String."), val, None, val.span)
    if isinstance(val, basestring):
        return Term(Tag(".String."), val, None, None)
    if isinstance(val, (list, tuple)):
        return Term(Tag(".tuple."), None, tuple(coerceToTerm(item) for item in val), None)
    if isinstance(val, set):
        return Term(Tag('.bag.'), None, tuple(coerceToTerm(item) for item in val), None)
    if isinstance(val, dict):
        return Term(Tag('.bag.'), None, tuple(Term(Tag('.attr.'), None,
                                                   (coerceToTerm(k), coerceToTerm(v)), None)
                                         for (k, v) in val.iteritems()),
                    None)
    def _substitute(self, map):
        return [self]

_Hole = namedtuple("_Hole", "tag name")

def _asTag(candidate):
    if isinstance(candidate, Term):
        if candidate.args:
            raise TypeError("Term with args can't be used as tag")
        else:
            return candidate.tag, candidate.data
    elif isinstance(candidate, Tag):
        return candidate, None
    else:
        raise TypeError("%r isn't a tag" % (candidate,))

def _multiget(args, holenum, index, repeat):
    result = args[holenum]
    for i in index:
        if not isinstance(result, list):
            return result
        result = result[i]
    return result

class ValueHole(_Hole):
    def _unparse(self, indentLevel=0):
        return "${%s}" % (self.name,)

    def _substitute(self, map):
        return [coerceToTerm(map[self.name])]


class PatternHole(_Hole):
    pass
