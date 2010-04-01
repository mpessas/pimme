#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author Apostolos Mpessas <mpessas@gmail.com>
@license GPL v3 or later
"""

import unittest
import test_info
import test_cmd

def suite():
    suite_info = unittest.TestLoader().loadTestsFromModule(test_info)
    suite_cmd = unittest.TestLoader().loadTestsFromModule(test_cmd)
    suites = [suite_info, suite_cmd]
    return unittest.TestSuite(suites)

if __name__ == '__main__':
    tests = suite()
    res = unittest.TestResult()
    tests.run(res)

    print res.testsRun, ' tests were run.'
    if res.wasSuccessful():
        print 'Success'
    else:
        if res.errors:
            print 'Errors:'
            print '=' * 20
            for err in res.errors:
                print err[0], err[1], '-' * 20
        if  res.failures:
            print 'Failures:'
            print '=' * 10
            for failure in res.failures:
                print failure[0], failure[1], '-' * 20
