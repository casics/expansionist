#!/usr/bin/env python3
'''Expansionist: split and expand identifiers

This module takes a program identifier, splits it, expands the individual
tokens, and returns the result as a short phrase.  For example, the input
'readf' might yield the result ['read', 'file'].
'''

import bisect
from   collections import defaultdict
import math
import os
import re
import sys

try:
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
except:
    sys.path.append("..")

import spiral
from spiral import ronin
from spiral.constants import suffixes, special_computing_terms

from nltk.corpus import words as nltk_words
from nltk.corpus import wordnet as nltk_wordnet


# Globals
# .............................................................................

dictionary = set(nltk_words.words())
dictionary.update(nltk_wordnet.all_lemma_names())


# Expand
# .............................................................................

def expressions(token):
    return r'.*'.join(c for c in token) + r'.*'

# Contexts currently being considered, in order of narrower to wider:
# - comments & doc strings of function where token is found
# - comments & doc strings of class where token is found
# - comments & file header where token is found
# - comments, file headers, & text of directory where token is found
# - comments, file headers, & text of whole code base

# FIXME: better hand it the whole original identifier bc that might
# add more context too

def expansion_candidates(token, context_list):
    # 'context_list' should be a list of lists, where each sublist consists
    # of words that are found in contexts for the expansion of the 'token'.
    # Expand() will use each of the sublists in turn as a source of context.
    # The contexts should go from narrower to wider.

    # Procedure:
    # 1. if token is a recognized special case, return predefined expansion
    # 2. if token is a full dictionary word, return it as-is
    # 3. for context c in context_list:
    #    a) if token is exact start of a word found in the context, return word
    #    b) if token ends in 's', remove it and try (a) again
    #    c) if token wildcard matches a word in the context, return word
    # The "return word" steps may return multiple candidates, for example if
    # the context includes multiple words that match..  It's up to the caller
    # to rank and select from the results.

    if len(token) > 2 and token in dictionary:
        return [token]
    candidates = []
    for context in context_list:
        candidates = [x for x in context if x.startswith(token)]
        if candidates:
            return candidates
        candidates = [x for x in context if re.match(expressions(token), x)]
        if candidates:
            return [x for x in candidates if x in dictionary]
    return candidates if candidates else [token]


# FIXME ranking is not implemented yet.  Here's an idea for an approach:
# If there is more than one alternative expansion, use the one
# with the highest frequency in the context.  If all frequencies
# are equal, take the one that is recognized in our dictionaries,
# and if there's more than one, take the shortest among them.

def expand(identifier, context_list, as_list = True):
    '''Takes the 'identifier', splits it into constituent tokens, and expands
    the tokens into full words if possible.  Uses 'context_list' as a source
    of candidate words for the expansion.  'context_list' should be a list of
    lists, where each sublist represents a context, and the order of the
    lists is narrower to wider contexts.  Example contexts: function
    definition, class definition, whole file, directory, whole project.
    Optional argument 'as_list' indicates whether the result should be
    returned as a list of words or as a string.  If True, the result will be
    of the form ['read', 'file', 'input']; if False, it will be a single
    string, such as 'read file input'.
    '''
    if context_list:
        if not isinstance(context_list[0], list):
            raise ValueError('context_list must be a list of lists')
    results = []
    for token in ronin.split(identifier):
        # FIXME doesn't find best, just uses 1st one on the list
        candidates = expansion_candidates(token, context_list)
        if candidates:
            results.append(candidates[0])
    return results if as_list else ' '.join(results)


# print(expand('str', [['string', 'software']]))
