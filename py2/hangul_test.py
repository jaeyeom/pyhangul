#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (C) 2012 by Jaehyun Yeom

import unittest
import hangul


class TestHangul(unittest.TestCase):
  """Return value of each test is on the left side."""

  def testOrdHangul(self):
    self.assertEqual(0, hangul.OrdHangul(u'가'))
    self.assertEqual(1, hangul.OrdHangul(u'각'))
    self.assertEqual(4, hangul.OrdHangul(u'간'))
    self.assertEqual(6468, hangul.OrdHangul(u'아'))
    self.assertEqual(11171, hangul.OrdHangul(u'힣'))

    # OrdHangul accepts unicode. Normal str needs to be decoded.
    byte_str = '간'
    self.assertEqual(4, hangul.OrdHangul(byte_str.decode('utf-8')))


  def testChrHangul(self):
    self.assertEqual(u'가', hangul.ChrHangul(0))
    self.assertEqual(u'각', hangul.ChrHangul(1))
    self.assertEqual(u'간', hangul.ChrHangul(4))
    self.assertEqual(u'아', hangul.ChrHangul(6468))
    self.assertEqual(u'힣', hangul.ChrHangul(11171))

    # ChrHangul returns unicode. It can be encoded as byte str.
    self.assertEqual('아', hangul.ChrHangul(6468).encode('utf-8'))

  def testDecomposeHangul(self):
    jamo = hangul.JAMO_ROMANIZATIONS
    self.assertEqual((0, 0, 0), hangul.DecomposeHangul(u'가', jamo))
    self.assertEqual((0, 0, 1), hangul.DecomposeHangul(u'각', jamo))
    self.assertEqual((0, 1, 0), hangul.DecomposeHangul(u'개', jamo))
    self.assertEqual((0, 2, 0), hangul.DecomposeHangul(u'갸', jamo))
    self.assertEqual((1, 0, 0), hangul.DecomposeHangul(u'까', jamo))
    self.assertEqual((2, 8, 0), hangul.DecomposeHangul(u'노', jamo))
    self.assertEqual((6, 0, 6), hangul.DecomposeHangul(u'많', jamo))
    self.assertEqual((11, 0, 0), hangul.DecomposeHangul(u'아', jamo))
    self.assertEqual((18, 20, 27), hangul.DecomposeHangul(u'힣', jamo))
    self.assertEqual(None, hangul.DecomposeHangul(u'a', jamo))

  def testComposeHangul(self):
    jamo = hangul.JAMO_ROMANIZATIONS
    self.assertEqual(u'가', hangul.ComposeHangul((0, 0, 0), jamo))
    self.assertEqual(u'각', hangul.ComposeHangul((0, 0, 1), jamo))
    self.assertEqual(u'개', hangul.ComposeHangul((0, 1, 0), jamo))
    self.assertEqual(u'갸', hangul.ComposeHangul((0, 2, 0), jamo))
    self.assertEqual(u'까', hangul.ComposeHangul((1, 0, 0), jamo))
    self.assertEqual(u'노', hangul.ComposeHangul((2, 8, 0), jamo))
    self.assertEqual(u'많', hangul.ComposeHangul((6, 0, 6), jamo))
    self.assertEqual(u'아', hangul.ComposeHangul((11, 0, 0), jamo))
    self.assertEqual(u'힣', hangul.ComposeHangul((18, 20, 27), jamo))

  def testRomanizeHangul(self):
    jamo = hangul.JAMO_ROMANIZATIONS
    self.assertEqual('ga', hangul.RomanizeHangul(u'가', jamo))
    self.assertEqual('gag', hangul.RomanizeHangul(u'각', jamo))
    self.assertEqual('gae', hangul.RomanizeHangul(u'개', jamo))
    self.assertEqual('gya', hangul.RomanizeHangul(u'갸', jamo))
    self.assertEqual('gga', hangul.RomanizeHangul(u'까', jamo))
    self.assertEqual('no', hangul.RomanizeHangul(u'노', jamo))
    self.assertEqual('manh', hangul.RomanizeHangul(u'많', jamo))
    self.assertEqual('a', hangul.RomanizeHangul(u'아', jamo))
    self.assertEqual('hih', hangul.RomanizeHangul(u'힣', jamo))

  def testUnromanizeHangul(self):
    jamo = hangul.JAMO_ROMANIZATIONS
    self.assertEqual(u'가', hangul.UnromanizeHangul('ga', jamo))
    self.assertEqual(u'각', hangul.UnromanizeHangul('gag', jamo))
    self.assertEqual(u'개', hangul.UnromanizeHangul('gae', jamo))
    self.assertEqual(u'갸', hangul.UnromanizeHangul('gya', jamo))
    self.assertEqual(u'까', hangul.UnromanizeHangul('gga', jamo))
    self.assertEqual(u'노', hangul.UnromanizeHangul('no', jamo))
    self.assertEqual(u'많', hangul.UnromanizeHangul('manh', jamo))
    self.assertEqual(u'아', hangul.UnromanizeHangul('a', jamo))
    self.assertEqual(u'힣', hangul.UnromanizeHangul('hih', jamo))
    self.assertEqual(None, hangul.UnromanizeHangul('', jamo))
    self.assertEqual(None, hangul.UnromanizeHangul('g', jamo))
    self.assertEqual(None, hangul.UnromanizeHangul('hihh', jamo))

  def testRomanizeHangulString(self):
    self.assertEqual('[ga][na][da]', hangul.RomanizeHangulString(u'가나다'))
    self.assertEqual('[eobs][neun]', hangul.RomanizeHangulString(u'없는'))
    self.assertEqual(
      '(san)(do)',
      hangul.RomanizeHangulString(u'산도', prefix='(', postfix=')'))
    self.assertEqual(
      'sando', hangul.RomanizeHangulString(u'산도', prefix='', postfix=''))

  def testUnromanizeHangulString(self):
    self.assertEqual(u'가나다', hangul.UnromanizeHangulString('[ga][na][da]'))
    self.assertEqual(u'없는', hangul.UnromanizeHangulString('[eobs][neun]'))
    self.assertEqual(u'산도', hangul.UnromanizeHangulString('(san)(do)',
                                                           prefix='(',
                                                           postfix=')'))

  def testHasFinalConsonants(self):
    self.assertEqual(False, hangul.HasFinalConsonants(u'전략가'))
    self.assertEqual(True, hangul.HasFinalConsonants(u'수공'))
    self.assertEqual(True, hangul.HasFinalConsonants(u'앉'))
    self.assertEqual(None, hangul.HasFinalConsonants(u'a'))
    self.assertEqual(None, hangul.HasFinalConsonants(u''))
    self.assertEqual(None, hangul.HasFinalConsonants(u'1'))

  def testAppendHangulPostfix(self):
    self.assertEqual('전략가를', hangul.AppendHangulPostfix('전략가', '를', '을'))
    self.assertEqual('수공을', hangul.AppendHangulPostfix('수공', '를', '을'))
    self.assertEqual('전략가가', hangul.AppendHangulPostfix('전략가', '가', '이'))
    self.assertEqual('수공으로', hangul.AppendHangulPostfix('수공', '로', '으로'))
    self.assertEqual('밥이다', hangul.AppendHangulPostfix('밥', '다', '이다'))

    # Does not support non-hangul.
    self.assertEqual('m를', hangul.AppendHangulPostfix('m', '를', '을'))

  def testGetInitialCharacter(self):
    self.assertEqual(u'ㅇ', hangul.GetInitialCharacter(u'이순신'))
    self.assertEqual(u'M', hangul.GetInitialCharacter(u'Michael'))
    self.assertEqual(u'N', hangul.GetInitialCharacter(u'nelly'))
    self.assertEqual(u'2', hangul.GetInitialCharacter(u'2PM'))
    self.assertEqual(None, hangul.GetInitialCharacter(u''))
    self.assertEqual(u'ㄱ', hangul.GetInitialCharacter(u'김치국'))
    self.assertEqual(u'ㅎ', hangul.GetInitialCharacter(u'ㅎㅎㅎ'))
    self.assertEqual(u'ㅜ', hangul.GetInitialCharacter(u'ㅜㅜ'))

  def testGetInitialCharacterBytes(self):
    self.assertEqual('ㅇ', hangul.GetInitialCharacterBytes('이순신'))
    self.assertEqual('M', hangul.GetInitialCharacterBytes('Michael'))
    self.assertEqual('N', hangul.GetInitialCharacterBytes('nelly'))
    self.assertEqual('2', hangul.GetInitialCharacterBytes('2PM'))
    self.assertEqual(None, hangul.GetInitialCharacterBytes(''))
    self.assertEqual('ㄱ', hangul.GetInitialCharacterBytes('김치국'))
    self.assertEqual('ㅎ', hangul.GetInitialCharacterBytes('ㅎㅎㅎ'))
    self.assertEqual('ㅜ', hangul.GetInitialCharacterBytes('ㅜㅜ'))

if __name__ == '__main__':
  unittest.main()
