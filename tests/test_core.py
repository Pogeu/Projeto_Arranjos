from __future__ import annotations

import unittest

import numpy as np

from src import beampattern, beamformer, generate_uca, generate_ucya, generate_ula, generate_upa
from src.steering_vector import steering_vector


class ArrayCoreTests(unittest.TestCase):
    def test_geometry_sizes(self) -> None:
        self.assertEqual(generate_ula(9, 0.5).shape, (9, 3))
        self.assertEqual(generate_uca(16, 1.0).shape, (16, 3))
        self.assertEqual(generate_upa(3, 4, 0.5, 0.5).shape, (12, 3))
        self.assertEqual(generate_ucya(9, 4, 1.0, 0.5).shape, (36, 3))

    def test_steering_vector_unit_modulus(self) -> None:
        positions = generate_ula(8, 0.5)
        a = steering_vector(positions, 0.0, np.deg2rad(20.0), 1.0)
        self.assertTrue(np.allclose(np.abs(a), 1.0))

    def test_beampattern_is_normalized(self) -> None:
        theta = np.deg2rad(np.linspace(-90.0, 90.0, 361))
        positions = generate_ula(8, 0.5)
        pattern = beampattern(positions, 0.0, theta, 1.0)
        self.assertAlmostEqual(float(np.max(pattern)), 0.0, places=10)

    def test_beamformer_keeps_steered_signal(self) -> None:
        positions = generate_ula(4, 0.5)
        wavelength = 1.0
        azimuth = 0.0
        elevation = np.deg2rad(10.0)
        samples = np.ones(32)
        a = steering_vector(positions, azimuth, elevation, wavelength)
        x = a[:, None] * samples[None, :]
        y = beamformer(x, positions, (azimuth, elevation), wavelength)
        self.assertTrue(np.allclose(y, samples))


if __name__ == "__main__":
    unittest.main()
