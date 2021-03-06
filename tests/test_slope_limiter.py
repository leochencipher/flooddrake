""" test slope limiting """

from __future__ import division

import numpy as np

from firedrake import *
from flooddrake import *


def test_slope_limiter():

    n = 15
    mesh = PeriodicUnitSquareMesh(n, n)

    # mixed function space
    v_h = FunctionSpace(mesh, "DG", 1)
    v_mu = FunctionSpace(mesh, "DG", 1)
    v_mv = FunctionSpace(mesh, "DG", 1)
    V = v_h * v_mu * v_mv

    # setup initial condition
    w = Function(V)
    w.sub(0).assign(1)
    w.sub(1).assign(1)
    w.sub(2).assign(1)

    x = SpatialCoordinate(V.mesh())
    b = Function(V)
    b.sub(0).interpolate(2 * x[0])

    w.assign(w - b)

    b_, b1, b2 = split(b)

    # slope limiting
    SL = SlopeLimiter(b_, V)
    W = SL.Limiter(w)

    # check that it's invariant as all cell averages are same.
    assert np.max(np.abs(W.dat.data[0] - w.dat.data[0])) < 1e-10


def test_slope_limiter_p0():

    n = 15
    mesh = PeriodicUnitSquareMesh(n, n)

    # mixed function space
    v_h = FunctionSpace(mesh, "DG", 0)
    v_mu = FunctionSpace(mesh, "DG", 0)
    v_mv = FunctionSpace(mesh, "DG", 0)
    V = v_h * v_mu * v_mv

    # setup initial condition
    w = Function(V)
    w.sub(0).assign(1)
    w.sub(1).assign(1)
    w.sub(2).assign(1)

    x = SpatialCoordinate(V.mesh())
    b = Function(V)
    b.sub(0).interpolate(2 * x[0])

    w.assign(w - b)

    b_, b1, b2 = split(b)

    # slope limiting
    SL = SlopeLimiter(b_, V)
    W = SL.Limiter(w)

    # check that it's invariant as all cell averages are same.
    assert np.max(np.abs(W.dat.data[0] - w.dat.data[0])) < 1e-10


def test_slope_limiter_mean_preserving():

    n = 15
    mesh = PeriodicUnitSquareMesh(n, n)

    # mixed function space
    v_h = FunctionSpace(mesh, "DG", 1)
    v_mu = FunctionSpace(mesh, "DG", 1)
    v_mv = FunctionSpace(mesh, "DG", 1)
    V = v_h * v_mu * v_mv

    # mixed functionspace
    v_hav = FunctionSpace(mesh, "DG", 0)
    v_muav = FunctionSpace(mesh, "DG", 0)
    v_mvav = FunctionSpace(mesh, "DG", 0)
    VAV = v_hav * v_muav * v_mvav

    # setup initial condition
    w = Function(V)
    x = SpatialCoordinate(V.mesh())
    w.sub(0).interpolate(x[0] * x[1])

    b = Function(V)
    b.sub(0).interpolate(x[0])

    w.assign(w - b)

    cell_av = Function(VAV).project(w)

    b_, b1, b2 = split(b)

    # slope limiting
    SL = SlopeLimiter(b_, V)
    W = SL.Limiter(w)

    new_cell_av = Function(VAV).project(W)

    # check that it's mean preserving.
    assert np.max(
        np.abs(
            cell_av.dat.data[0] -
            new_cell_av.dat.data[0])) < 1e-10


if __name__ == "__main__":
    import os
    import pytest
    pytest.main(os.path.abspath(__file__))
