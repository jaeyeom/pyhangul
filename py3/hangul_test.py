#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2012 by Jaehyun Yeom

import unittest
import hangul


class TestHangul(unittest.TestCase):
  """Return value of each test is on the left side."""

  def testOrdHangul(self):
    self.assertEqual(0, hangul.OrdHangul('가'))
    self.assertEqual(1, hangul.OrdHangul('각'))
    self.assertEqual(4, hangul.OrdHangul('간'))
    self.assertEqual(6468, hangul.OrdHangul('아'))
    self.assertEqual(11171, hangul.OrdHangul('힣'))

  def testChrHangul(self):
    self.assertEqual('가', hangul.ChrHangul(0))
    self.assertEqual('각', hangul.ChrHangul(1))
    self.assertEqual('간', hangul.ChrHangul(4))
    self.assertEqual('아', hangul.ChrHangul(6468))
    self.assertEqual('힣', hangul.ChrHangul(11171))

  def testDecomposeHangul(self):
    jamo = hangul.JAMO_ROMANIZATIONS
    self.assertEqual((0, 0, 0), hangul.DecomposeHangul('가', jamo))
    self.assertEqual((0, 0, 1), hangul.DecomposeHangul('각', jamo))
    self.assertEqual((0, 1, 0), hangul.DecomposeHangul('개', jamo))
    self.assertEqual((0, 2, 0), hangul.DecomposeHangul('갸', jamo))
    self.assertEqual((1, 0, 0), hangul.DecomposeHangul('까', jamo))
    self.assertEqual((2, 8, 0), hangul.DecomposeHangul('노', jamo))
    self.assertEqual((6, 0, 6), hangul.DecomposeHangul('많', jamo))
    self.assertEqual((11, 0, 0), hangul.DecomposeHangul('아', jamo))
    self.assertEqual((18, 20, 27), hangul.DecomposeHangul('힣', jamo))
    self.assertEqual(None, hangul.DecomposeHangul('a', jamo))

  def testComposeHangul(self):
    jamo = hangul.JAMO_ROMANIZATIONS
    self.assertEqual('가', hangul.ComposeHangul((0, 0, 0), jamo))
    self.assertEqual('각', hangul.ComposeHangul((0, 0, 1), jamo))
    self.assertEqual('개', hangul.ComposeHangul((0, 1, 0), jamo))
    self.assertEqual('갸', hangul.ComposeHangul((0, 2, 0), jamo))
    self.assertEqual('까', hangul.ComposeHangul((1, 0, 0), jamo))
    self.assertEqual('노', hangul.ComposeHangul((2, 8, 0), jamo))
    self.assertEqual('많', hangul.ComposeHangul((6, 0, 6), jamo))
    self.assertEqual('아', hangul.ComposeHangul((11, 0, 0), jamo))
    self.assertEqual('힣', hangul.ComposeHangul((18, 20, 27), jamo))

  def testRomanizeHangul(self):
    jamo = hangul.JAMO_ROMANIZATIONS
    self.assertEqual('ga', hangul.RomanizeHangul('가', jamo))
    self.assertEqual('gag', hangul.RomanizeHangul('각', jamo))
    self.assertEqual('gae', hangul.RomanizeHangul('개', jamo))
    self.assertEqual('gya', hangul.RomanizeHangul('갸', jamo))
    self.assertEqual('gga', hangul.RomanizeHangul('까', jamo))
    self.assertEqual('no', hangul.RomanizeHangul('노', jamo))
    self.assertEqual('manh', hangul.RomanizeHangul('많', jamo))
    self.assertEqual('a', hangul.RomanizeHangul('아', jamo))
    self.assertEqual('hih', hangul.RomanizeHangul('힣', jamo))

  def testUnromanizeHangul(self):
    jamo = hangul.JAMO_ROMANIZATIONS
    self.assertEqual('가', hangul.UnromanizeHangul('ga', jamo))
    self.assertEqual('각', hangul.UnromanizeHangul('gag', jamo))
    self.assertEqual('개', hangul.UnromanizeHangul('gae', jamo))
    self.assertEqual('갸', hangul.UnromanizeHangul('gya', jamo))
    self.assertEqual('까', hangul.UnromanizeHangul('gga', jamo))
    self.assertEqual('노', hangul.UnromanizeHangul('no', jamo))
    self.assertEqual('많', hangul.UnromanizeHangul('manh', jamo))
    self.assertEqual('아', hangul.UnromanizeHangul('a', jamo))
    self.assertEqual('힣', hangul.UnromanizeHangul('hih', jamo))
    self.assertEqual(None, hangul.UnromanizeHangul('', jamo))
    self.assertEqual(None, hangul.UnromanizeHangul('g', jamo))
    self.assertEqual(None, hangul.UnromanizeHangul('hihh', jamo))

  def testRomanizeHangulString(self):
    self.assertEqual('[ga][na][da]', hangul.RomanizeHangulString('가나다'))
    self.assertEqual('[eobs][neun]', hangul.RomanizeHangulString('없는'))
    self.assertEqual(
      '(san)(do)', hangul.RomanizeHangulString('산도', prefix='(', postfix=')'))
    self.assertEqual(
      'sando', hangul.RomanizeHangulString('산도', prefix='', postfix=''))

  def testUnromanizeHangulString(self):
    self.assertEqual('가나다', hangul.UnromanizeHangulString('[ga][na][da]'))
    self.assertEqual('없는', hangul.UnromanizeHangulString('[eobs][neun]'))
    self.assertEqual('산도', hangul.UnromanizeHangulString('(san)(do)',
                                                           prefix='(',
                                                           postfix=')'))

  def testHasFinalConsonants(self):
    self.assertEqual(False, hangul.HasFinalConsonants('전략가'))
    self.assertEqual(True, hangul.HasFinalConsonants('수공'))
    self.assertEqual(True, hangul.HasFinalConsonants('앉'))
    self.assertEqual(None, hangul.HasFinalConsonants('a'))
    self.assertEqual(None, hangul.HasFinalConsonants(''))
    self.assertEqual(None, hangul.HasFinalConsonants('1'))

  def testAppendHangulPostfix(self):
    self.assertEqual('전략가를', hangul.AppendHangulPostfix('전략가', '를', '을'))
    self.assertEqual('수공을', hangul.AppendHangulPostfix('수공', '를', '을'))
    self.assertEqual('전략가가', hangul.AppendHangulPostfix('전략가', '가', '이'))
    self.assertEqual('수공으로', hangul.AppendHangulPostfix('수공', '로', '으로'))
    self.assertEqual('밥이다', hangul.AppendHangulPostfix('밥', '다', '이다'))
    
    # Does not support non-hangul.
    self.assertEqual('m를', hangul.AppendHangulPostfix('m', '를', '을'))

  def testGetInitialCharacter(self):
    self.assertEqual('ㅇ', hangul.GetInitialCharacter('이순신'))
    self.assertEqual('M', hangul.GetInitialCharacter('Michael'))
    self.assertEqual('N', hangul.GetInitialCharacter('nelly'))
    self.assertEqual('2', hangul.GetInitialCharacter('2PM'))
    self.assertEqual(None, hangul.GetInitialCharacter(''))
    self.assertEqual('ㄱ', hangul.GetInitialCharacter('김치국'))
    self.assertEqual('ㅎ', hangul.GetInitialCharacter('ㅎㅎㅎ'))
    self.assertEqual('ㅜ', hangul.GetInitialCharacter('ㅜㅜ'))


if __name__ == '__main__':
  unittest.main()
