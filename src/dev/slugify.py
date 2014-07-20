# -*- coding: utf-8 -*-

__version__ = '0.0.7'

__all__ = ['slugify']

import re
import unicodedata
import types
import sys
from htmlentitydefs import name2codepoint
from workflow.workflow import ASCII_REPLACEMENTS

# character entity reference
CHAR_ENTITY_REXP = re.compile('&(%s);' % '|'.join(name2codepoint))

# decimal character reference
DECIMAL_REXP = re.compile(r'&#(\d+);')

# hexadecimal character reference
HEX_REXP = re.compile(r'&#x([\da-fA-F]+);')

REPLACE1_REXP = re.compile(r'[\']+')
REPLACE2_REXP = re.compile(r'[^-a-z0-9]+')
REMOVE_REXP = re.compile('-{2,}')

def isascii(text):
    """Test if ``text`` contains only ASCII characters

    :param text: text to test for ASCII-ness
    :type text: ``unicode``
    :returns: ``True`` if ``text`` contains only ASCII characters
    :rtype: ``Boolean``
    """

    try:
        text.encode('ascii')
    except UnicodeEncodeError:
        return False
    return True

def fold_to_ascii(text):
    """
    Convert non-ASCII characters to closest ASCII equivalent.

    :param text: text to convert
    :type text: ``unicode``
    :returns: text containing only ASCII characters
    :rtype: ``unicode``
    """
    if isascii(text):
        return text
    text = ''.join([ASCII_REPLACEMENTS.get(c, c) for c in text])
    return unicode(unicodedata.normalize('NFKD',
                   text).encode('ascii', 'ignore'))



def smart_truncate(string, max_length=0, word_boundaries=False, separator=' '):
    """ Truncate a string """

    string = string.strip(separator)

    if not max_length:
        return string

    if len(string) < max_length:
        return string

    if not word_boundaries:
        return string[:max_length].strip(separator)

    if separator not in string:
        return string[:max_length]

    truncated = ''
    for word in string.split(separator):
        if word:
            next_len = len(truncated) + len(word) + len(separator)
            if next_len <= max_length:
                truncated += '{0}{1}'.format(word, separator)
    if not truncated:
        truncated = string[:max_length]
    return truncated.strip(separator)


def slugify(text, entities=True, decimal=True, hexadecimal=True,
            max_length=0, word_boundary=False, separator='_'):
    """ Make a slug from the given text """

    # text to unicode
    if type(text) != types.UnicodeType:
        text = unicode(text, 'utf-8', 'ignore')

    # decode unicode ( 影師嗎 = Ying Shi Ma)
    text = fold_to_ascii(text)

    # text back to unicode
    if type(text) != types.UnicodeType:
        text = unicode(text, 'utf-8', 'ignore')

    # character entity reference
    if entities:
        func = lambda m: unichr(name2codepoint[m.group(1)])
        text = CHAR_ENTITY_REXP.sub(func, text)

    # decimal character reference
    if decimal:
        try:
            text = DECIMAL_REXP.sub(lambda m: unichr(int(m.group(1))), text)
        except:
            pass

    # hexadecimal character reference
    if hexadecimal:
        try:
            text = HEX_REXP.sub(lambda m: unichr(int(m.group(1), 16)), text)
        except:
            pass

    # translate
    text = unicodedata.normalize('NFKD', text)
    if sys.version_info < (3,):
        text = text.encode('ascii', 'ignore')

    # replace unwanted characters
        # replace ' with nothing instead with -
    text = REPLACE1_REXP.sub('', text.lower())
    text = REPLACE2_REXP.sub('-', text.lower())

    # remove redundant -
    text = REMOVE_REXP.sub('-', text).strip('-')

    # smart truncate if requested
    if max_length > 0:
        text = smart_truncate(text, max_length, word_boundary, '-')

    if separator != '-':
        text = text.replace('-', separator)

    return text
