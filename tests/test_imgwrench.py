#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `imgwrench` package."""


import os
import unittest
from pathlib import Path

from PIL import Image
from click.testing import CliRunner

from imgwrench import cli_imgwrench

from .images import pixel1x1, png1x1


class TestImgwrenchMainCli(unittest.TestCase):
    '''Tests for `imgwrench` main cli.'''

    def setUp(self):
        '''Set up test fixtures, if any.'''
        self.runner = CliRunner()
        self.images_path = Path(__file__).resolve().parent / 'images'

    def tearDown(self):
        '''Tear down test fixtures, if any.'''

    def test_command_line_interface(self):
        '''Test help invocation.'''
        help_msg = 'Show this message and exit'
        help_result = self.runner.invoke(cli_imgwrench, ['--help'])
        self.assertEqual(0, help_result.exit_code)
        self.assertIn(help_msg, help_result.output)
        # executing imgwrench without subcommands should have the same effect
        help_result = self.runner.invoke(cli_imgwrench)
        self.assertEqual(0, help_result.exit_code)
        self.assertIn(help_msg, help_result.output)

    def test_subcommand_availability(self):
        '''Test availability of subcommands'''
        self.assertGreaterEqual(len(cli_imgwrench.commands), 3)
        help_result = self.runner.invoke(cli_imgwrench, ['--help'])
        for subcommand in cli_imgwrench.commands:
            self.assertIn(subcommand, help_result.output)

    def test_pipeline(self):
        '''Test pipeline functionality'''
        self.assertTrue(cli_imgwrench.chain)
        pipelinetest = 'pipelinetest'

        n_invocations = [0]
        n_image_invocations = [0]

        @cli_imgwrench.command(pipelinetest)
        def _pipelintest():
            n_invocations[0] += 1

            def _process(images):
                for orgfname, image in images:
                    n_image_invocations[0] += 1
                    yield orgfname, image

            return _process

        with self.runner.isolated_filesystem():
            with open('pixel1x1.jpg', 'wb') as f:
                f.write(pixel1x1)
            with open('images.txt', 'w') as f:
                for i in range(10):
                    f.write('pixel1x1.jpg\n')
            result = self.runner.invoke(cli_imgwrench,
                                        ['-i', 'images.txt', pipelinetest,
                                         pipelinetest, pipelinetest])
            self.assertEqual(0, result.exit_code)
            self.assertEqual(3, n_invocations[0], 'expecting 3 processors')
            self.assertEqual(30, n_image_invocations[0], 'expecting 30 calls')
        del cli_imgwrench.commands[pipelinetest]

    def test_increment(self):
        '''Test increment of output files'''
        increment = 3
        prefix = 'img_'
        with self.runner.isolated_filesystem():
            with open('pixel1x1.jpg', 'wb') as f:
                f.write(pixel1x1)
            with open('images.txt', 'w') as f:
                for i in range(10):
                    f.write('pixel1x1.jpg\n')
            result = self.runner.invoke(cli_imgwrench,
                                        ['-c', increment, '-p', prefix,
                                         '-d', 4,
                                         '-i', 'images.txt', 'save'])
            self.assertEqual(0, result.exit_code)
            for i in range(10):
                fname = '{}{:04d}.jpg'.format(prefix, i*increment)
                self.assertTrue(os.path.exists(fname), fname + ' missing')

    def test_digits(self):
        '''Test number of digits of output files'''
        prefix = 'img_'
        with self.runner.isolated_filesystem():
            with open('pixel1x1.jpg', 'wb') as f:
                f.write(pixel1x1)
            with open('images.txt', 'w') as f:
                for i in range(20):
                    f.write('pixel1x1.jpg\n')
            result = self.runner.invoke(cli_imgwrench,
                                        ['-p', prefix,
                                         '-d', 7,
                                         '-i', 'images.txt', 'save'])
            self.assertEqual(0, result.exit_code)
            for i in range(20):
                fname = '{}{:07d}.jpg'.format(prefix, i)
                self.assertTrue(os.path.exists(fname), fname + ' missing')

    def test_output_folder_creation(self):
        '''Test creation of non-existing output folder'''
        prefix = 'img_'
        output_folder = 'my/out/dir'
        n = 5
        with self.runner.isolated_filesystem():
            with open('pixel1x1.jpg', 'wb') as f:
                f.write(pixel1x1)
            with open('images.txt', 'w') as f:
                for i in range(n):
                    f.write('pixel1x1.jpg\n')
            result = self.runner.invoke(cli_imgwrench,
                                        ['-o', output_folder,
                                         '-p', prefix,
                                         '-d', 1,
                                         '-i', 'images.txt', 'save'])
            self.assertEqual(0, result.exit_code)
            for i in range(n):
                fname = '{}/{}{:01d}.jpg'.format(output_folder, prefix, i)
                self.assertTrue(os.path.exists(fname), fname + ' missing')

    def test_png_loading(self):
        '''Test loading of PNG input images'''
        prefix = 'img_'
        with self.runner.isolated_filesystem():
            with open('png1x1.png', 'wb') as f:
                f.write(png1x1)
            with open('images.txt', 'w') as f:
                f.write('png1x1.png\n')
            result = self.runner.invoke(cli_imgwrench,
                                        ['-p', prefix,
                                         '-d', 4,
                                         '-i', 'images.txt', 'save'])
            self.assertEqual(0, result.exit_code)
            fname = '{}{:04d}.jpg'.format(prefix, 0)
            self.assertTrue(os.path.exists(fname), fname + ' missing')

    def test_saving_of_exif_metadata(self):
        '''Test saving of exif metadata'''
        img_path = str(self.images_path / 'town.jpg')
        img = Image.open(img_path)
        self.assertTrue(hasattr(img, '_getexif'))
        org_exif = img._getexif()
        # need to copy image to isolated filesystem
        with open(img_path, 'rb') as f:
            img_data = f.read()
        with self.runner.isolated_filesystem():
            with open('town.jpg', 'wb') as f:
                f.write(img_data)
            with open('images.txt', 'w') as f:
                f.write('town.jpg\n')
            # save with exif
            result = self.runner.invoke(cli_imgwrench,
                                        ['-p', 'exif_',
                                         '-d', 4,
                                         '-e',
                                         '-i', 'images.txt',
                                         'resize', '-m', 100])
            self.assertEqual(0, result.exit_code)
            fname = '{}{:04d}.jpg'.format('exif_', 0)
            self.assertTrue(os.path.exists(fname), fname + ' missing')
            img = Image.open(fname)
            self.assertTrue(hasattr(img, '_getexif'))
            exif = img._getexif()
            self.assertEqual(org_exif, exif)
            # save without exif
            result = self.runner.invoke(cli_imgwrench,
                                        ['-p', 'no_exif_',
                                         '-d', 4,
                                         '-i', 'images.txt', 'save'])
            fname = '{}{:04d}.jpg'.format('no_exif_', 0)
            self.assertTrue(os.path.exists(fname), fname + ' missing')
            img = Image.open(fname)
            self.assertFalse(hasattr(img, '_getexif') and img._getexif())

    def test_image_rotation(self):
        '''Test rotation if images depending on exif preservation'''
        img_path = str(self.images_path / 'town.jpg')
        img = Image.open(img_path)
        self.assertTrue(hasattr(img, '_getexif'))
        # note: this is a portrait image by exif rotation,
        # but a landscaoe image by storage format
        self.assertEqual(img.size[0], 300)
        self.assertEqual(img.size[1], 200)
        # need to copy image to isolated filesystem
        with open(img_path, 'rb') as f:
            img_data = f.read()
        with self.runner.isolated_filesystem():
            with open('town.jpg', 'wb') as f:
                f.write(img_data)
            with open('images.txt', 'w') as f:
                f.write('town.jpg\n')
            # save with exif
            result = self.runner.invoke(cli_imgwrench,
                                        ['-p', 'exif_',
                                         '-d', 4,
                                         '-e',
                                         '-i', 'images.txt',
                                         'save'])
            self.assertEqual(0, result.exit_code)
            fname = '{}{:04d}.jpg'.format('exif_', 0)
            self.assertTrue(os.path.exists(fname), fname + ' missing')
            img = Image.open(fname)
            # stored with exif -> should still be landscape by storage
            self.assertEqual(img.size[0], 300)
            self.assertEqual(img.size[1], 200)
            # save without exif
            result = self.runner.invoke(cli_imgwrench,
                                        ['-p', 'no_exif_',
                                         '-d', 4,
                                         '-i', 'images.txt',
                                         'save'])
            self.assertEqual(0, result.exit_code)
            fname = '{}{:04d}.jpg'.format('no_exif_', 0)
            self.assertTrue(os.path.exists(fname), fname + ' missing')
            img = Image.open(fname)
            # stored without exif -> should now be portrait by storage
            self.assertEqual(img.size[0], 200)
            self.assertEqual(img.size[1], 300)

    def test_keep_names(self):
        '''Test keeping names of images.'''
        fname = 'pixel1x1.jpg'
        outdir = Path('out')
        with self.runner.isolated_filesystem():
            with open(fname, 'wb') as f:
                f.write(pixel1x1)
            with open('images.txt', 'w') as f:
                f.write(fname + '\n')
            result = self.runner.invoke(cli_imgwrench,
                                        ['-k',
                                         '-i', 'images.txt',
                                         '-o', str(outdir),
                                         'save'])
            self.assertEqual(0, result.exit_code)
            outfile = outdir / fname
            self.assertTrue(outfile.exists(), '{0} missing'.format(outfile))
