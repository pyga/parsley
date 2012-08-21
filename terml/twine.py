from collections import namedtuple

_SourceSpan = namedtuple("SourceSpan",
                         "uri isOneToOne startLine startCol endLine endCol")
class SourceSpan(_SourceSpan):
    """
    Information about the original location of a span of text.
    Twines use this to remember where they came from.

    uri: Name of document this text came from.

    isOneToOne: Whether each character in that Twine maps to the
    corresponding source character position.

    startLine, endLine: Line numbers for the beginning and end of the
    span. Line numbers start at 1.

    startCol, endCol: Column numbers for the beginning and end of the
    span. Column numbers start at 0.
    """
    def __new__(*args, **kwargs):
        ss = _SourceSpan.__new__(*args, **kwargs)
        if (ss.startLine != ss.endLine and ss.isOneToOne):
            raise ValueError("one-to-one spans must be on a line")
        return ss

    def notOneToOne(self):
        """
        Return a new SourceSpan for the same text that doesn't claim
        one-to-one correspondence.
        """
        return SourceSpan(self.uri, False, self.startLine, self.startCol,
                          self.endLine, self.endCol)

    def __repr__(self):
        return "<%s#:%s::%s>" % (self.uri,
                                 "span" if self.isOneToOne else "blob",
                                 ':'.join(str(x) for x in self[2:]))



def spanCover(a, b):
    """
    Create a new SourceSpan that covers spans `a` and `b`.
    """
    if a is None or b is None or a.uri != b.uri:
        return None
    if (a.isOneToOne and b.isOneToOne
        and a.endLine == b.startLine
        and a.endCol == b.startCol):
        # These spans are adjacent.
        return SourceSpan(a.uri, True,
                          a.startLine, a.startCol,
                          b.endLine, b.endCol)

    # find the earlier start point
    if a.startLine < b.startLine:
        startLine = a.startLine
        startCol = a.startCol
    elif a.startLine == b.startLine:
        startLine = a.startLine
        startCol = min(a.startCol, b.startCol)
    else:
        startLine = b.startLine
        startCol = b.startCol

    #find the later end point
    if b.endLine > a.endLine:
        endLine = b.endLine
        endCol = b.endCol
    elif a.endLine == b.endLine:
        endLine = a.endLine
        endCol = max(a.endCol, b.endCol)
    else:
        endLine = a.endLine
        endCol = a.endCol

    return SourceSpan(a.uri, False, startLine, startCol, endLine, endCol)


class TwineMixin(object):
    """
    Methods for strings that remembers where they came from.
    """

    def __init__(self, input, span=None):
        if (span and span.isOneToOne
            and len(input) != (span.endCol - span.startCol + 1)):
            raise ValueError("One-to-one spans must match the size of the string")
        self._span = span


    @classmethod
    def fromParts(cls, parts):
        """
        Return a Twine that contains, in sequence, all the Twines in
        the iterable `parts`.
        """
        if not parts:
            return cls._makeSimple(cls._empty)
        elif len(parts) == 1:
            return parts[0]
        else:
            ps = []
            for p in parts:
                if isinstance(p, CompositeTwineMixin):
                    ps.extend(p._parts)
                else:
                    ps.append(p)
            return cls._makeComposite(ps)


    def asFrom(self, sourceURI, startLine=1, startCol=0):
        """
        Return a Twine with source span info from the given URI and
        (optionally) start position.
        """
        parts = []
        s = unicode(self)
        ln = len(s)
        start = 0
        end = 0
        while start < ln:
            end = s.find('\n', start)
            if end == -1:
                end = ln - 1
            endCol = startCol + end - start
            ss = SourceSpan(sourceURI, True, startLine, startCol, startLine, endCol)
            parts.append(self.__class__._makeSimple(s[start:end+1], ss))
            startLine += 1
            startCol = 0
            start = end + 1

        return self.__class__.fromParts(parts)


    @property
    def span(self):
        return self._span


    @property
    def parts(self):
        return [self]


    @property
    def sourceMap(self):
        result = []
        offset = 0
        for p in self.parts:
            ss = p.span
            if ss:
                result.append(((offset, offset + len(p)), ss))
            offset += len(p)
        return tuple(result)


    def __getslice__(self, i, j):
        return self.__getitem__(slice(i, j))


    def __getitem__(self, idxOrSlice):
        """
        Return a new Twine sliced out of this one, with a matching
        SourceSpan.
        """
        if not isinstance(idxOrSlice, slice):
            if idxOrSlice >= len(self):
                raise IndexError(idxOrSlice)
            if idxOrSlice < 0:
                stop = None
            else:
                stop = idxOrSlice + 1
            idxOrSlice = slice(idxOrSlice, stop, 1)
        start, stop, step = idxOrSlice.indices(len(self))
        if start == stop:
            return self.__class__._makeSimple(self._empty)
        if start == 0 and stop == len(self):
            return self

        return self._slice(start, stop, step)

    def _slice(self, start, stop, step):
        """
        This twine is atomic, so a simple slice and updated SourceSpan
        will do.
        """
        s = super(TwineMixin, self).__getitem__(slice(start, stop, step))
        if self._span and self._span.isOneToOne:
            startCol = self._span.startCol + start
            endCol = startCol + (stop - start) - 1
            span = SourceSpan(self._span.uri, step == 1,
                              self._span.startLine,
                              startCol,
                              self._span.endLine,
                              endCol)
        else:
            span = self._span
        return self.__class__._makeSimple(s, span)


    def __add__(self, other):
        if not isinstance(other, TwineMixin):
            other = self.__class__._makeSimple(other)
        return self.__class__.fromParts([self, other])

    def __radd__(self, other):
        if not isinstance(other, TwineMixin):
            other = self.__class__._makeSimple(other)
        return self.__class__.fromParts([other, self])

    def split(self, sep, count=None):
        if sep == "":
            raise ValueError("Separator must not be empty")
        p1 = 0
        p2 = self.find(sep)
        result = []
        while p2 != -1:
            result.append(self[p1:p2])
            if count == 0:
                break
            if count is not None:
                count -= 1
            p1 = p2 + len(sep)
            p2 = self.find(sep, p1)
        result.append(self[p1:])
        return result


    def rsplit(self, sep, count=None):
        if sep == "":
            raise ValueError("Separator must not be empty")
        p1 = len(self)
        p2 = self.rfind(sep)
        result = []
        while p2 != -1:
            if count == 0:
                break
            if count is not None:
                count -= 1
            result.insert(0, self[p2 + len(sep):p1])
            p1 = p2
            p2 = self.rfind(sep, 0, p1)
        result.insert(0, self[:p1])
        return result


    def join(self, twines):
        if not twines:
            return self.__class__._makeSimple(u"")
        sep = self.__class__._makeSimple(self)
        parts = [twines[0]]
        for t in twines[1:]:
            parts.append(sep)
            parts.append(t)
        return self.__class__.fromParts(parts)

    def replace(self, specimen, replacement, count=None):
        oldLen = len(specimen)
        parts = []
        if oldLen == 0:
            raise ValueError("Can't replace the empty string")
        p1 = 0
        p2 = self.find(specimen)
        while p2 != -1:
            if count == 0:
                break
            left = self[p1:p2]
            old = self[p2:p2 + oldLen]
            parts.append(left)
            parts.append(old.infect(replacement))
            p1 = p2 + oldLen
            p2 = self.find(specimen, p1)
        parts.append(self[p1:])
        return self.__class__.fromParts(parts)


    def infect(self, target):
        if len(self) != len(target):
            span = self.span.notOneToOne()
        else:
            span = self.span
        return self.__class__._makeSimple(target, span)


class CompositeTwineMixin(TwineMixin):

    def __init__(self, parts):
        self._parts = tuple(parts)
        self._len = None

    @property
    def parts(self):
        return self._parts


    @property
    def span(self):
        if not self._parts:
            return None
        ss = self._parts[0].span
        for part in self._parts[1:]:
            if ss is None:
                return None
            ss = spanCover(ss, part.span)
        return ss


    def __len__(self):
        if self._len is None:
            self._len = sum(len(p) for p in self._parts)
        return self._len

    def _getPartAt(self, pos):
        """
        Find the part that `pos` is an index into. For instance, if
        self._parts is ['abc', 'def', 'ghi'], 2 is an index into part
        0, and 4 is an index into part 1.
        """
        search = 0
        for i, p in enumerate(self._parts):
            if pos < search + len(p):
                return [i, pos - search]
            search += len(p)
        raise IndexError("%s bigger than %s" % (pos, search))


    def _slice(self, start, stop, step):
        """
        Build a slice by extracting the relevant parts from this
        twine, slicing them if necessary, and returning a new
        CompositeTwine made from them.
        """
        leftIdx, leftOffset = self._getPartAt(start)
        left = self._parts[leftIdx]

        rightIdx, rightOffset = self._getPartAt(stop - 1)

        if leftIdx == rightIdx:
            # slice start/end falls in the same part
            return left[leftOffset:rightOffset + 1]
        else:
            right = self._parts[rightIdx]
            leftScrap = left[leftOffset::step]
            middle = self._parts[leftIdx + 1:rightIdx]
            if step != 1:
                # gotta count leftovers on the end of each part after
                # slicing with steps
                newMiddle = []
                stepOffset = step - (len(leftScrap) % step)
                for part in middle:
                    newMiddle.append(part[stepOffset::step])
                    stepOffset = step - (len(part) % step)
                middle = tuple(newMiddle)
            else:
                stepOffset = 0
            rightScrap = right[stepOffset:rightOffset + 1:step]
            return self.__class__.fromParts((leftScrap,) + middle + (rightScrap,))


    def __add__(self, other):
        #XXX
        if not isinstance(other, TwineMixin):
            other = self.__class__._makeSimple(other)
        return self.__class__.fromParts(self._parts + (other,))


    def __repr__(self):
        return repr(self._empty.join(self._parts))


    def __eq__(self, other):
        return self._empty.join(self._parts) == other


    def find(self, *args):
        #XXX more efficientness
        return self._empty.join(self._parts).find(*args)

    def rfind(self, *args):
        #XXX more efficientness
        return self._empty.join(self._parts).rfind(*args)

    def __int__(self):
        return int(self._empty.join(self._parts))

    def __float__(self):
        return float(self._empty.join(self._parts))



    ## Maybe this is faster?
    # def __getitem__(self, idxOrSlice):
    #     if not isinstance(idxOrSlice, slice):
    #         if idxOrSlice < 0:
    #             idxOrSlice = len(self) + idxOrSlice
    #         partIdx, partOffset = self._getPartAt(idxOrSlice)
    #         return self._parts[partIdx][partOffset]
    #     else:
    #         return Twine.__getitem__(self, idxOrSlice)


class TwineTextBase(unicode):
    _empty = u''

    @classmethod
    def _makeComposite(cls, parts):
        return CompositeTwineText(parts)

    @classmethod
    def _makeSimple(cls, s, span=None):
        return TwineText(s, span)


class TwineText(TwineMixin, TwineTextBase):
    def __new__(self, input, span=None):
        return unicode.__new__(self, input)

class TwineBytesBase(str):
    _empty = ''

    @classmethod
    def _makeComposite(cls, parts):
        return CompositeTwineBytes(parts)

    @classmethod
    def _makeSimple(cls, s, span=None):
        return TwineBytes(s, span)


class TwineBytes(TwineMixin, TwineBytesBase):
    def __new__(self, input, span=None):
        return str.__new__(self, input)



class CompositeTwineText(CompositeTwineMixin, TwineTextBase):
    def __new__(self, parts):
        return unicode.__new__(self)

    def __unicode__(self):
        return self._empty.join(self._parts)



class CompositeTwineBytes(CompositeTwineMixin, TwineBytesBase):
    def __new__(self, parts):
        return str.__new__(self)

    def __str__(self):
        try:
            return self._empty.join(self._parts)
        except TypeError:
            print "!#", repr(self._parts)
            return "#!ERR"


def asTwineFrom(bytesOrText, uri):
    if isinstance(bytesOrText, str):
        return TwineBytes(bytesOrText).asFrom(uri)
    elif isinstance(bytesOrText, unicode):
        return TwineText(bytesOrText).asFrom(uri)
    else:
        raise TypeError("Can't make a twine from %r, since it isn't a string" % (bytesOrText,))
