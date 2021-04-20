import numpy as np
import galsim
import lsst.afw.image as afw_image
import lsst.geom as geom
from ..sim import FixedDMPSF, PowerSpectrumDMPSF, make_ps_psf
from ._wcs import make_sim_wcs


def test_fixed_dmpsf_smoke():
    dim = 20
    masked_image = afw_image.MaskedImageF(dim, dim)
    exp = afw_image.ExposureF(masked_image)

    gspsf = galsim.Gaussian(fwhm=0.9)
    psf_dim = 15
    wcs = make_sim_wcs(dim)

    fpsf = FixedDMPSF(gspsf=gspsf, psf_dim=psf_dim, wcs=wcs)
    exp.setPsf(fpsf)

    psf = exp.getPsf()

    x = 8.5
    y = 10.1
    pos = geom.Point2D(x=x, y=y)
    gs_pos = galsim.PositionD(x=x, y=y)

    # this one is always centered
    msim = psf.computeKernelImage(pos)
    assert msim.array.shape == (psf_dim, psf_dim)

    gsim = gspsf.drawImage(
        nx=psf_dim, ny=psf_dim,
        wcs=wcs.local(image_pos=gs_pos),
    )

    assert np.allclose(msim.array, gsim.array)


def test_fixed_dmpsf_offset_smoke():
    dim = 20
    masked_image = afw_image.MaskedImageF(dim, dim)
    exp = afw_image.ExposureF(masked_image)

    gspsf = galsim.Gaussian(fwhm=0.9)
    psf_dim = 15
    wcs = make_sim_wcs(dim)

    fpsf = FixedDMPSF(gspsf=gspsf, psf_dim=psf_dim, wcs=wcs)
    exp.setPsf(fpsf)

    psf = exp.getPsf()

    x = 8.5
    y = 10.1
    pos = geom.Point2D(x=x, y=y)
    gs_pos = galsim.PositionD(x=x, y=y)

    # this one is shifted
    msim = psf.computeImage(pos)
    assert msim.array.shape == (psf_dim, psf_dim)

    offset_x = x - int(x)
    offset_y = y - int(y)

    if offset_x > 0.5:
        offset_x = 1 - offset_x
    if offset_y > 0.5:
        offset_y = 1 - offset_y

    offset = (offset_x, offset_y)

    gsim = gspsf.drawImage(
        nx=psf_dim, ny=psf_dim,
        offset=offset,
        wcs=wcs.local(image_pos=gs_pos),
    )

    assert np.allclose(msim.array, gsim.array)


def test_ps_dmpsf_smoke():
    rng = np.random.RandomState(7812)
    dim = 20
    masked_image = afw_image.MaskedImageF(dim, dim)
    exp = afw_image.ExposureF(masked_image)

    psf_dim = 15
    wcs = make_sim_wcs(dim)

    pspsf = make_ps_psf(rng=rng, dim=dim)
    fpsf = PowerSpectrumDMPSF(pspsf=pspsf, psf_dim=psf_dim, wcs=wcs)
    exp.setPsf(fpsf)

    psf = exp.getPsf()

    x = 8.5
    y = 10.1
    pos = geom.Point2D(x=x, y=y)
    gs_pos = galsim.PositionD(x=x, y=y)

    # this one is always centered
    msim = psf.computeKernelImage(pos)
    assert msim.array.shape == (psf_dim, psf_dim)

    gspsf = pspsf.getPSF(gs_pos)
    gsim = gspsf.drawImage(
        nx=psf_dim, ny=psf_dim,
        wcs=wcs.local(image_pos=gs_pos),
    )

    assert np.allclose(msim.array, gsim.array)


def test_ps_dmpsf_offset_smoke():
    rng = np.random.RandomState(12)

    dim = 20
    masked_image = afw_image.MaskedImageF(dim, dim)
    exp = afw_image.ExposureF(masked_image)

    psf_dim = 15
    wcs = make_sim_wcs(dim)

    pspsf = make_ps_psf(rng=rng, dim=dim)
    fpsf = PowerSpectrumDMPSF(pspsf=pspsf, psf_dim=psf_dim, wcs=wcs)
    exp.setPsf(fpsf)

    psf = exp.getPsf()

    x = 8.5
    y = 10.1
    pos = geom.Point2D(x=x, y=y)
    gs_pos = galsim.PositionD(x=x, y=y)

    # this one is shifted
    msim = psf.computeImage(pos)
    assert msim.array.shape == (psf_dim, psf_dim)

    offset_x = x - int(x)
    offset_y = y - int(y)

    if offset_x > 0.5:
        offset_x = 1 - offset_x
    if offset_y > 0.5:
        offset_y = 1 - offset_y

    offset = (offset_x, offset_y)

    gspsf = pspsf.getPSF(gs_pos)
    gsim = gspsf.drawImage(
        nx=psf_dim, ny=psf_dim,
        offset=offset,
        wcs=wcs.local(image_pos=gs_pos),
    )

    assert np.allclose(msim.array, gsim.array)
