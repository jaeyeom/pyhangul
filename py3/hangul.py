#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2012 by Jaehyun Yeom

import functools
import operator

JAMO_ROMANIZATIONS = (
  # 19 Jamos
  ('g', 'gg', 'n', 'd', 'dd', 'r', 'm', 'b', 'bb', 's',
   'ss', '', 'j', 'jj', 'c', 'k', 't', 'p', 'h'),
  # 21 Jamos
  ('a', 'ae', 'ya', 'yae', 'eo', 'e', 'yeo', 'ye', 'o', 'wa',
   'wae', 'oe', 'yo', 'u', 'weo', 'we', 'wi', 'yu', 'eu', 'yi',
   'i'),
  # 28 Jamos
  ('', 'g', 'gg', 'gs', 'n', 'nj', 'nh', 'd', 'l', 'lg',
   'lm', 'lb', 'ls', 'lt', 'lp', 'lh', 'm', 'b', 'bs', 's',
   'ss', 'ng', 'j', 'c', 'k', 't', 'p', 'h'))

INITIAL_JAMOS = (
  'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ',
  'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ')

FIRST_HANGUL_CHARACTER = '\uac00'


def OrdHangul(hangul_character):
  """Return the integer index of hangul character, starting from 0 for [ga]."""
  return ord(hangul_character) - ord(FIRST_HANGUL_CHARACTER)


def ChrHangul(hangul_index):
  """Return a hangul character with given index starting from 0 for [ga]."""
  return chr(ord(FIRST_HANGUL_CHARACTER) + hangul_index)


def DecomposeHangulIndex(hangul_index, num_jamos):
  """Decompose hangul index to jamo indexes.

  This is a reverse function of ComposeHangulIndex().

  Args:
    hangul_index: Hangul index starting from 0 for [ga].
    num_jamos: Number of each CVC jamo family which is (19, 21, 28)
        for unicode character.

  Returns:
    Tuple of jamo indexes like (x, y, z).
  """
  jamo_indexes = []
  for num_jamo in reversed(num_jamos):
    jamo_indexes.append(hangul_index % num_jamo)
    hangul_index //= num_jamo
  return tuple(reversed(jamo_indexes))


def ComposeHangulIndex(jamo_indexes, num_jamos):
  """Compose jamo indexes to hangul index.

  This is a reverse function of DecomposeHangulIndex().

  Args:
    jamo_indexes: Tuple of jamo indexes like (x, y, z).
    num_jamos: Number of each CVC jamo family which is (19, 21, 28)
        for unicode character.

  Returns:
    Hangul index starting from 0 for [ga].
  """
  hangul_index = 0
  for num_jamo, jamo_index in zip(num_jamos, jamo_indexes):
    hangul_index *= num_jamo
    hangul_index += jamo_index
  return hangul_index


def DecomposeHangul(hangul_character, jamo_romanizations):
  """Decompose a hangul character to jamo indexes.

  This is a reverse function of ComposeHangul().

  Args:
    hangul_character: Hangul index starting from 0 for [ga].

  Returns:
    Tuple of jamo indexes like (x, y, z) if hangul_character is
    hangul, None otherwise.
  """
  num_jamos = tuple(len(jamos) for jamos in jamo_romanizations)
  num_characters = functools.reduce(operator.mul, num_jamos, 1)
  end_character = chr(ord(FIRST_HANGUL_CHARACTER) + num_characters)
  if (hangul_character >= FIRST_HANGUL_CHARACTER and
      hangul_character < end_character):
    hangul_index = OrdHangul(hangul_character)
    return DecomposeHangulIndex(hangul_index, num_jamos)
  return None


def ComposeHangul(jamo_indexes, jamo_romanizations):
  """Compose jamo indexes to a hangul character.

  This is a reverse function of DecomposeHangul().

  Args:
    jamo_indexes: Tuple of jamo indexes like (x, y, z).

  Returns:
    A hangul character.
  """
  num_jamos = tuple(len(jamos) for jamos in jamo_romanizations)
  hangul_index = ComposeHangulIndex(jamo_indexes, num_jamos)
  return ChrHangul(hangul_index)


def RomanizeHangul(hangul_character, jamo_romanizations):
  """Romanize a single hangul character."""
  hangul_indexes = DecomposeHangul(hangul_character, jamo_romanizations)
  if hangul_indexes:
    return ''.join(jamos[index]
                   for index, jamos in zip(hangul_indexes, jamo_romanizations))
  return None


def UnromanizeHangul(romanized_character, jamo_romanizations):
  """Unromanize a single hangul character."""
  jamo_indexes = []
  for jamo_romanization in jamo_romanizations:
    matched_jamo = ''
    matched_jamo_index = -1
    for jamo_index, jamo in enumerate(jamo_romanization):
      if (romanized_character.startswith(jamo) and
          len(jamo) >= len(matched_jamo)):
        matched_jamo = jamo
        matched_jamo_index = jamo_index
    if matched_jamo_index == -1:
      return None
    jamo_indexes.append(matched_jamo_index)
    romanized_character = romanized_character[len(matched_jamo):]
  if romanized_character:
    return None
  return ComposeHangul(jamo_indexes, jamo_romanizations)


def RomanizeHangulString(unicode_string,
                         jamo_romanizations=JAMO_ROMANIZATIONS,
                         prefix='[', postfix=']'):
  """Romanize a string with hangul characters."""
  romanized_string = ''
  for unicode_character in unicode_string:
    romanized_character = RomanizeHangul(unicode_character, jamo_romanizations)
    if romanized_character:
      romanized_string += prefix + romanized_character + postfix
    else:
      romanized_string += unicode_character
  return romanized_string


def UnromanizeHangulString(unicode_string,
                           jamo_romanizations=JAMO_ROMANIZATIONS,
                           prefix='[', postfix=']'):
  """Unrromanize a string with romanized hangul characters."""
  unromanized_hangul_string = ''
  open_index = -1
  commit_index = 0
  for index, unicode_character in enumerate(unicode_string):
    if unicode_character == prefix:
      unromanized_hangul_string += unicode_string[commit_index:index]
      commit_index = index
      open_index = index
    elif unicode_character == postfix:
      unromanized_hangul_character = UnromanizeHangul(
        unicode_string[open_index+1:index], jamo_romanizations)
      if unromanized_hangul_character:
        unromanized_hangul_string += unromanized_hangul_character
        commit_index = index + 1
      else:
        unromanized_hangul_string += unicode_string[commit_index:index]
        commit_index = index
      open_index = -1
  unromanized_hangul_string += unicode_string[commit_index:]
  return unromanized_hangul_string


def IsHangulJamos(unicode_string):
  """Returns True if every characters are hangul jamos like ㄱ or ㅑ."""
  for unicode_character in unicode_string:
    if ord(unicode_character) not in range(ord('ㄱ'), ord('ㅣ') + 1):
      return False
  return True


def HasFinalConsonants(unicode_string, jamo_romanizations=JAMO_ROMANIZATIONS):
  if unicode_string:
    jamo_index = DecomposeHangul(unicode_string[-1], jamo_romanizations)
    if jamo_index:
      return jamo_index[2] > 0


def AppendHangulPostfix(string, no_cons, cons):
  """Append proper hangul postfix.

  Args:
    string: Hangul string.
    no_cons: Postfix for no final consonants such as 는, 가, 로, 를, 다
    cons: Post for final consonants such as 은, 이, 으로, 을, 이다
  """
  if HasFinalConsonants(string):
    return string + cons
  else:
    return string + no_cons


def GetInitialCharacter(unicode_string,
                        jamo_romanizations=JAMO_ROMANIZATIONS,
                        initial_jamos=INITIAL_JAMOS):
  """Get initial character of the string.

  For hangul characters, the first jamo is returned. Please see test cases.
  """
  if unicode_string:
    first_character = unicode_string[0]
    decomposed = DecomposeHangul(first_character, jamo_romanizations)
    if decomposed:
      return initial_jamos[decomposed[0]]
    else:
      return first_character.upper()
  else:
    return None
