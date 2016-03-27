'''
This file provides unit tests for subcaption2subfig.
'''
import os
import sys
import tempfile
import filecmp

import subcaption2subfig

# For Python < 2.7, unittest2 is a backport of unittest
if sys.version_info[:2] <= (2, 6):
    import unittest2 as unittest
else:
    import unittest

TEST_DIR = 'test_resources'


def main_test(source_file, target_file=None):
    '''
    Test whether a subfigure2subcaption test file is processed
    correctly.
    '''
    # If no target is given, target is the same as the source
    if target_file is None:
        target_file = source_file
    # Make a tempory file to output into
    fd, filename = tempfile.mkstemp()
    try:
        subcaption2subfig.main(os.path.join(TEST_DIR, source_file), filename)
        assert filecmp.cmp(os.path.join(TEST_DIR, target_file), filename)
    finally:
        os.remove(filename)


class TestSubcaption2Subfig(unittest.TestCase):

    '''
    Tests for subcaption2subfig.
    '''

    def test_none(self):
        main_test('none_in.tex')

    def test_basic(self):
        main_test('basic_in.tex', 'basic_out.tex')

    def test_indented(self):
        main_test('indented_in.tex', 'indented_out.tex')

    def test_multi(self):
        main_test('multi_in.tex', 'multi_out.tex')

    def test_subfigureargs(self):
        main_test('subfigureargs_in.tex', 'subfigureargs_out.tex')

    def test_commentedout(self):
        main_test('commentedout_in.tex')

    def test_partialcomment(self):
        main_test('partialcomment_in.tex', 'partialcomment_out.tex')

    def test_labelled(self):
        main_test('labelled_in.tex', 'labelled_out.tex')

    def test_labelledtwice(self):
        main_test('labelledtwice_in.tex', 'labelledtwice_out.tex')

    def test_captioned(self):
        main_test('captioned_in.tex', 'captioned_out.tex')

    def test_captionlabel(self):
        main_test('captionlabel_in.tex', 'captionlabel_out.tex')

    def test_inheritwidth(self):
        main_test('inheritwidth_in.tex', 'inheritwidth_out.tex')
