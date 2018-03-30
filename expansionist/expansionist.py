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

try:
    from .constants import *
except:
    from constants import *


# Globals.
# .............................................................................

dictionary = set(nltk_words.words())
dictionary.update(nltk_wordnet.all_lemma_names())


# Substitutions
# .............................................................................

def translate(token, substitutions):
    if not substitutions:
        return token
    return substitutions[token] if token in substitutions else token


# Expander.
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

    if len(token) < 2:
        return [token]
    # If it's a dictionary word, return that word.
    if token in dictionary:
        return [token]
    candidates = []
    # Iterate over the contexts (assumed to be narrower to wider)
    for context in context_list:
        # If token is an exact start of a word in the context, return word.
        candidates += [x for x in context if x.startswith(token)]
        # If token ends in 's', remove it and try (a) again. (Eg. "buffs").
        if token.endswith('s'):
            candidates += [x for x in context if x.startswith(token[:-1])]
        # If token wildcard matches a word in the context, return word
        candidates += [x for x in context if re.match(expressions(token), x)]
    return candidates if candidates else [token]


# FIXME ranking is not implemented yet.  Here's an idea for an approach:
# If there is more than one alternative expansion, use the one
# with the highest frequency in the context.  If all frequencies
# are equal, take the one that is recognized in our dictionaries,
# and if there's more than one, take the shortest among them.

def expand(identifier, contexts, as_list = True,
           substitutions = common_computing_acronyms):
    '''Takes the 'identifier', splits it into constituent tokens, and expands
    the tokens into full words if possible.  The process uses 'contexts' as a
    source of candidate words for the expansion.  The value of 'contexts'
    should be a list of lists, where each sublist represents a context, and
    the order of the lists is narrower to wider contexts.  Example contexts:
    function definition, class definition, whole file, directory, whole
    project.  Optional argument 'as_list' indicates whether the result should
    be returned as a list of words or as a string.  If True, the result will
    be of the form ['read', 'file', 'input']; if False, it will be a single
    string, such as 'read file input'.

    This function will perform substitution of recognized terms such as
    acronyms and abbreviations; e.g., it will replace 'acl' with 'access
    control list'.  The optional argument 'substitutions', if supplied, will
    override Expansionist's default list of substitutions.  The value of
    'substitutions' should be a dictionary in which each key is a term in
    lower case (e.g., an acronym) and the value is the desired expansion.
    Set 'substitutions' to the empty list [] to prevent all expansions; in
    that case, this function will leave acronyms and abbreviations as-is in
    the output.
    '''
    if contexts:
        if not isinstance(contexts[0], list):
            raise ValueError('contexts must be a list of lists')
    results = []
    for token in ronin.split(identifier):
        # FIXME right now it doesn't find best, just uses 1st one on the list
        candidates = expansion_candidates(token, contexts)
        if candidates:
            words = [w for w in candidates if w in dictionary]
            if words:
                results.append(words[0])
            else:
                results.append(token)
    if substitutions:
        final = []
        for term in results:
            final += translate(term, substitutions).split()
    else:
        final = results
    return results if as_list else ' '.join(results)


print(expand('asn1_open', [['config', 'configuration']]))
