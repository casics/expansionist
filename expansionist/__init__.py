'''Expansionist: expand identifier tokens

Natural language processing (NLP) methods are increasingly being applied to
source code analysis for various purposes.  The methods rely on terms
(identifiers and other textual strings) extracted from program source code
and comments.  The methods often work better if, instead of raw identifiers,
real words are used as features; that is, "get" and "integer" are often better
features for NLP tools than the string "getInteger".  This leads to the
need for automated methods for splitting identifiers of classes, functions,
variables, and other entities into word-like constituents.  A number of
methods have been proposed an implemented to perform identifier splitting.

Expansionist is a package that can be applied to short tokens to produce
candidate expansions based on contextual information.  The context can be,
e.g., text extracted from comments, strings and file headers of source code
files where the tokens are found.

Authors
-------

Michael Hucka <mhucka@caltech.edu>

Copyright
---------

Copyright (c) 2017 by the California Institute of Technology.  This software
was developed as part of the CASICS project, the Comprehensive and Automated
Software Inventory Creation System.  For more, visit http://casics.org.

'''

from .__version__ import __version__, __title__, __description__, __url__
from .__version__ import __author__, __email__
from .__version__ import __license__, __copyright__

from .constants import common_computing_acronyms
