import lxml.etree


_xslt_trees = [lxml.etree.parse('lower-%i.xslt' % i) for i in (1, 2)]
xslt_transforms = list(map(lxml.etree.XSLT, _xslt_trees))


_ld_url = _xslt_trees[0].getroot().nsmap['ld']
def ld_name(name):
    return lxml.etree.QName(_ld_url, name)


class XMLError(Exception):
    def __init__(self, message, *, file=None, line=None):
        self.message = message
        self.file = file
        self.line = line

    def __str__(self):
        return ': '.join(map(str, filter(bool, [self.file, self.line, self.message])))
