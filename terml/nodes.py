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
        if isinstance(tag, QFunctor):
            #XXX QTerm just has a property that delegates for 'data'
            data = tag.data
        return _Term.__new__(cls, tag, data, args, span)

    def __iter__(self):
        #and now I feel a bit silly subclassing namedtuple
        raise NotImplementedError()

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
            if len(self.args) == 0:
                if isinstance(self.tag, _Hole):
                    return "%s()" % (self.tag._unparse(indentLevel),)
                else:
                    return self.tag._unparse(indentLevel)
            return "%s(%s)" % (self.tag._unparse(indentLevel), args)

    def withSpan(self, span):
        return Term(self.tag, self.data, self.args, span)


    def build(self, builder):
        if self.data is None:
            f = builder.leafTag(self.tag, self.span)
        else:
            f = builder.leafData(self.data, self.span)

        return builder.term(f, [arg.build(builder) for arg in self.args])


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

    def withoutArgs(self):
        return Term(self.tag, self.data, (), self.span)

    def _substitute(self, map):
        candidate = self.tag._substitute(map)[0]
        args = tuple(itertools.chain.from_iterable(a._substitute(map) for a in self.args))
        term = Term(candidate.tag, candidate.data, args, self.span)
        return [term]

    def substitute(self, map):
        return self._substitute(map)[0]


    def _match(self, args, specimens, bindings, index, max):
        if not specimens:
            return -1
        spec = self._coerce(specimens[0])
        if spec is None:
            return -1
        matches = self.tag._match(args, [spec.withoutArgs()], bindings, index, 1)
        if not matches:
            return -1
        if matches > 1:
            raise TypeError("Functor may only match 0 or 1 specimen")
        num = matchArgs(self.args, spec.args, args, bindings, index, len(spec.args))
        if len(spec.args) == num:
            if max >= 1:
                return 1
        return -1

    def _coerce(self, spec):
        if isinstance(spec, Term):
            newf = coerceToQuasiMatch(spec.withoutArgs(), self.tag.isFunctorHole, self.tag.tag)
            if newf is None:
                return None
            return Term(newf.asFunctor(), None, spec.args, None)
        else:
            return coerceToQuasiMatch(spec, self.tag.isFunctorHole, self.tag.tag)

    def match(self, specimen, substitutionArgs=()):
        bindings = {}
        if self._match(substitutionArgs, [specimen], bindings, (), 1) == 1:
            return bindings
        raise TypeError("%r doesn't match %r" % (self, specimen))

    def _reserve(self):
        return 1

    def asFunctor(self):
        if self.args:
            raise ValueError("Terms with args can't be used as functors")
        else:
            return self.tag


def matchArgs(quasiArglist, specimenArglist, args, bindings, index, max):
    specs = specimenArglist
    reserves = [q._reserve() for q in quasiArglist]
    numConsumed = 0
    for i, qarg in enumerate(quasiArglist):
        num = qarg._match(args, specs, bindings, index, max - sum(reserves[i + 1:]))
        if num == -1:
            return -1
        specs = specs[num:]
        max -= num
        numConsumed += num
    return numConsumed


class Tag(object):
    def __init__(self, name):
        if name[0] == '':
            import pdb; pdb.set_trace()
        self.name = name

    def __eq__(self, other):
        return other.__class__ == self.__class__ and self.name == other.name

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return "Tag(%r)" % (self.name,)

    def _unparse(self, indentLevel=0):
        return self.name


class QFunctor(namedtuple("QFunctor", "tag data span")):
    isFunctorHole = False
    def _reserve(self):
        return 1

    @property
    def name(self):
        return self.tag.name

    def _unparse(self, indentLevel=0):
        return self.tag._unparse(indentLevel)

    def _substitute(self, map):
        return [Term(self.tag, self.data, None, self.span)]

    def _match(self, args, specimens, bindings, index, max):
        if not specimens:
            return -1
        spec = coerceToQuasiMatch(specimens[0], False, self.tag)
        if spec is None:
            return -1
        if self.data is not None and self.data != spec.data:
            return -1
        if max >= 1:
            return 1
        return -1

    def asFunctor(self):
        return self

def coerceToQuasiMatch(val, isFunctorHole, tag):
    from terml.twine import TwineText, TwineBytes
    if isFunctorHole:
        if val is None:
            result = Term(Tag("null"), None, None, None)
        elif isinstance(val, Term):
            if len(val.args) != 0:
                return None
            else:
                result = val
        elif isinstance(val, (TwineText, TwineBytes)):
            result = Term(Tag(val), val, None, val.span)
        elif isinstance(val, basestring):
            result = Term(Tag(val), None, None, None)
        elif isinstance(val, bool):
            result = Term(Tag(["false", "true"][val]), None, None, None)
        else:
            return None
    else:
        result = coerceToTerm(val)
    if tag is not None and result.tag != tag:
        return None
    return result

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

class _Hole(namedtuple("_Hole", "tag name isFunctorHole")):
    def _reserve(self):
        return 1

    def __repr__(self):
        return "term('%s')" % (self._unparse(4).replace("'", "\\'"))

    def match(self, specimen, substitutionArgs=()):
        bindings = {}
        if self._match(substitutionArgs, [specimen], bindings, (), 1) != -1:
            return bindings
        raise TypeError("%r doesn't match %r" % (self, specimen))


def _multiget(args, holenum, index, repeat):
    result = args[holenum]
    for i in index:
        if not isinstance(result, list):
            return result
        result = result[i]
    return result

def _multiput(bindings, holenum, index, newval):
    bits = bindings
    dest = holenum
    for it in index:
        next = bits[dest]
        if next is None:
            next = {}
            bits[dest] = next
        bits = next
        dest = it
    result = None
    if dest in bits:
        result = bits[dest]
    bits[dest] = newval
    return result

class ValueHole(_Hole):
    def _unparse(self, indentLevel=0):
        return "${%s}" % (self.name,)

    def _substitute(self, map):
        termoid = map[self.name]
        val = coerceToQuasiMatch(termoid, self.isFunctorHole, self.tag)
        if val is None:
            raise TypeError("%r doesn't match %r" % (termoid, self))
        return [val]

    def asFunctor(self):
        if self.isFunctorHole:
            return self
        else:
            return ValueHole(self.tag, self.name, True)


class PatternHole(_Hole):

    def _unparse(self, indentLevel=0):
        if self.tag:
            return "%s@{%s}" % (self.tag.name, self.name)
        else:
            return "@{%s}" % (self.name,)

    def _match(self, args, specimens, bindings, index, max):
        if not specimens:
            return -1
        spec = coerceToQuasiMatch(specimens[0], self.isFunctorHole, self.tag)
        if spec is None:
            return -1
        oldval = _multiput(bindings, self.name, index, spec)
        if oldval is None or oldval != spec:
            if max >= 1:
                return 1
        return -1


    def asFunctor(self):
        if self.isFunctorHole:
            return self
        else:
            return PatternHole(self.tag, self.name, True)

class QSome(namedtuple("_QSome", "value quant")):
    def _reserve(self):
        if self.quant == "+":
            return 1
        else:
            return 0
