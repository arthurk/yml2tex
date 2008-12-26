from yaml.reader import *
from yaml.scanner import *
from yaml.parser import *
from composer import *
from yaml.constructor import *
from yaml.resolver import *

class PairLoader(Reader, Scanner, Parser, PairComposer, Constructor, Resolver):

    def __init__(self, stream):
        Constructor.add_constructor(u'!omap', self.omap_constructor)
        
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        PairComposer.__init__(self)
        Constructor.__init__(self)
        Resolver.__init__(self)
    
    def omap_constructor(self, loader, node):
        return loader.construct_pairs(node)