import os
import sys
from pathlib import Path

# Weird issue: If you run the Python version, you need to use vtk.util
# If you run a compiled exe using PyInstaller, you need vtkmodules
try:
    from vtk.util.colors import light_grey
except ImportError:
    from vtkmodules.util.colors import light_grey

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkIOGeometry import vtkSTLReader
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
from vtkmodules.vtkRenderingCore import vtkPolyDataMapper, vtkActor
from vtkmodules.vtkRenderingLOD import vtkLODActor

# For PyInstaller paths
bundle_dir = Path(getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__))))


def load_STL(filename):
    path = str(bundle_dir / filename)
    reader = vtkSTLReader()
    reader.SetFileName(path)
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    actor = vtkLODActor()
    actor.SetMapper(mapper)
    return actor


def create_coordinates():
    axes = vtkAxesActor()
    axes.SetTotalLength(100, 100, 100)
    axes.SetShaftType(0)
    axes.SetCylinderRadius(0.02)
    axes.GetXAxisCaptionActor2D().SetWidth(0.03)
    axes.GetYAxisCaptionActor2D().SetWidth(0.03)
    axes.GetZAxisCaptionActor2D().SetWidth(0.03)
    return axes


def create_ground():
    # create plane source
    plane = vtkPlaneSource()
    plane.SetXResolution(5)
    plane.SetYResolution(5)
    plane.SetCenter(0.30, 0, 0.02)
    plane.SetNormal(0, 0, 1)
    # mapper
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(plane.GetOutputPort())

    # actor
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetRepresentationToWireframe()

    actor.GetProperty().SetColor(light_grey)
    transform = vtkTransform()
    transform.Scale(500, 500, 1)
    actor.SetUserTransform(transform)
    return actor
