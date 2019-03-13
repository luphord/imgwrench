# -*- coding: utf-8 -*-

'''Test utils.'''

import os

from imgwrench import cli_imgwrench

from .images import pixel1x1


def execute_and_test_output_images(test, cli_runner, n_input, n_output,
                                   prefix, args):
    '''Execute subcommand and test output images'''
    with cli_runner.isolated_filesystem():
        with open('pixel1x1.jpg', 'wb') as f:
            f.write(pixel1x1)
        with open('images.txt', 'w') as f:
            for i in range(n_input):
                f.write('pixel1x1.jpg\n')
        result = cli_runner.invoke(cli_imgwrench,
                                   ['-p', prefix,
                                    '-d', 4,
                                    '-i', 'images.txt'] + args)
        test.assertEqual(0, result.exit_code)
        for i in range(n_output + 1):
            fname = '{}{:04d}.jpg'.format(prefix, i)
            exists = os.path.exists(fname)
            if i < n_output:
                test.assertTrue(exists, fname + ' missing')
            else:
                test.assertFalse(exists, fname + ' must not exist')
