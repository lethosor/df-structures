from codegen.util import ld_name, XMLError

class BaseType:
    def __init__(self, *, type_name, source_file):
        self.type_name = type_name
        self.source_file = source_file

    @classmethod
    def from_node(cls, node, *, source_file):
        meta = node.attrib[ld_name('meta')]
        try:
            type_name = node.attrib['type-name']
        except KeyError:
            import pdb; pdb.set_trace()
            raise XMLError('Unnamed type', file=source_file)
        return BaseType(
            type_name=type_name,
            source_file=source_file,
        )
