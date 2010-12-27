import os
import pyfits
import unittest
import numpy as np

import healpy
from healpy.fitsfunc import *
from healpy.sphtfunc import *

class TestFitsFunc(unittest.TestCase):
    
    def setUp(self):
        self.nside = 512
        self.m = np.arange(healpy.nside2npix(self.nside))
        self.filename = 'testmap.fits'

    def test_write_map_IDL(self):
        write_map(self.filename, self.m, fits_IDL=True)
        read_m = pyfits.open(self.filename)[1].data.field(0)
        self.assertEqual(read_m.ndim, 2)
        self.assertEqual(read_m.shape[1], 1024)
        self.assertTrue(np.all(self.m == read_m.flatten()))

    def test_write_map_C(self):
        write_map(self.filename, self.m, fits_IDL=False)
        read_m = pyfits.open(self.filename)[1].data.field(0)
        self.assertEqual(read_m.ndim, 1)
        self.assertTrue(np.all(self.m == read_m))

    def tearDown(self):
        os.remove(self.filename)

class TestReadWriteAlm(unittest.TestCase):

    def setUp(self):

        s=Alm.getsize(256)
        self.alms = np.arange(s, dtype=np.complex128)

    def test_write_alm(self):

        write_alm('toto128.fits',self.alms,lmax=128,mmax=128)
        a0 = read_alm('toto128.fits')
        self.assertEqual(Alm.getlmax(len(a0)),128)

    def test_write_alm_256_128(self):
        write_alm('toto256_128.fits',self.alms,lmax=256,mmax=128)
        a0 = read_alm('toto256_128.fits')
        l0,m0 = Alm.getlm(128)
        idx = Alm.getidx(256,l0,m0)
        np.testing.assert_array_almost_equal(self.alms[idx],a0)


if __name__ == '__main__':
    unittest.main()