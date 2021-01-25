# trace generated using paraview version 5.8.1
#
# To ensure correct image size when batch processing, please search
# for and uncomment the line `# renderView*.ViewSize = [*,*]`

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'XML Unstructured Grid Reader'
mesh_full_OGSNRvtu = XMLUnstructuredGridReader(FileName=['/Users/mollaali/Opening/PhaseField/shear/half/mesh_half_OGSNR.vtu'])
mesh_full_OGSNRvtu.CellArrayStatus = ['MaterialIDs']

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [882, 1122]

# get layout
layout1 = GetLayout()

# show data in view
mesh_full_OGSNRvtuDisplay = Show(mesh_full_OGSNRvtu, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
mesh_full_OGSNRvtuDisplay.Representation = 'Surface'
mesh_full_OGSNRvtuDisplay.ColorArrayName = [None, '']
mesh_full_OGSNRvtuDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
mesh_full_OGSNRvtuDisplay.SelectOrientationVectors = 'None'
mesh_full_OGSNRvtuDisplay.ScaleFactor = 0.4
mesh_full_OGSNRvtuDisplay.SelectScaleArray = 'None'
mesh_full_OGSNRvtuDisplay.GlyphType = 'Arrow'
mesh_full_OGSNRvtuDisplay.GlyphTableIndexArray = 'None'
mesh_full_OGSNRvtuDisplay.GaussianRadius = 0.02
mesh_full_OGSNRvtuDisplay.SetScaleArray = [None, '']
mesh_full_OGSNRvtuDisplay.ScaleTransferFunction = 'PiecewiseFunction'
mesh_full_OGSNRvtuDisplay.OpacityArray = [None, '']
mesh_full_OGSNRvtuDisplay.OpacityTransferFunction = 'PiecewiseFunction'
mesh_full_OGSNRvtuDisplay.DataAxesGrid = 'GridAxesRepresentation'
mesh_full_OGSNRvtuDisplay.PolarAxes = 'PolarAxesRepresentation'
mesh_full_OGSNRvtuDisplay.ScalarOpacityUnitDistance = 0.14687864221330904

# reset view to fit data
renderView1.ResetCamera()

#changing interaction mode based on data extents
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [0.0, 0.0, 10000.0]

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Programmable Filter'
programmableFilter1 = ProgrammableFilter(Input=mesh_full_OGSNRvtu)
programmableFilter1.Script = """import numpy as np
import math
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk
in_data = self.GetInputDataObject(0, 0)
output = self.GetOutputDataObject(0)
in_point_data = in_data.GetPointData()
in_cell_data = in_data.GetCellData()
# get the point coordinates:
coord_vtk = in_data.GetPoints().GetData()
coord = vtk_to_numpy(coord_vtk)

# Getting the ingredients
u_vtk = in_point_data.GetAbstractArray("displacement")
u = vtk_to_numpy(u_vtk)
grad_d_vtk = in_point_data.GetAbstractArray("Grad_d")
grad_d = vtk_to_numpy(grad_d_vtk)



# initialize Gc (cell data)
num_nodes, num_comp = coord.shape
G_theta = np.zeros(num_nodes)
for i, x in enumerate(coord):
    u_x = u[i][0]
    u_y = u[i][1]

    gd_x = grad_d[i][0]
    gd_y = grad_d[i][1]


    G_theta[i] = -u_x*gd_x+u_y*gd_y
G_theta_vtk = numpy_to_vtk(G_theta, 1)
G_theta_vtk.SetName("G_theta")\
\

output.GetPointData().AddArray(G_theta_vtk)"""
programmableFilter1.RequestInformationScript = ''
programmableFilter1.RequestUpdateExtentScript = ''
programmableFilter1.PythonPath = ''

# Properties modified on programmableFilter1
programmableFilter1.Script = """import numpy as np
import math
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk

in_data = self.GetInputDataObject(0, 0)
output = self.GetOutputDataObject(0)

in_point_data = in_data.GetPointData()

# get the point coordinates:
coord_vtk = in_data.GetPoints().GetData()
coord = vtk_to_numpy(coord_vtk)

# initialize phase_field (point data)
num_nodes, num_comp = coord.shape
phase_field = np.ones(num_nodes)

for node_id, x in enumerate(coord):

    if( x[0] >- 0.1005  and x[0] < 0.1005 and x[1] < 0.00251 and x[1] > -0.00251):
        phase_field[node_id] = 0.0



phase_field_vtk = numpy_to_vtk(phase_field, 1)
phase_field_vtk.SetName("pf-ic")

output.GetPointData().AddArray(phase_field_vtk)"""

# show data in view
programmableFilter1Display = Show(programmableFilter1, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
programmableFilter1Display.Representation = 'Surface'
programmableFilter1Display.ColorArrayName = [None, '']
programmableFilter1Display.OSPRayScaleArray = 'pf-ic'
programmableFilter1Display.OSPRayScaleFunction = 'PiecewiseFunction'
programmableFilter1Display.SelectOrientationVectors = 'None'
programmableFilter1Display.ScaleFactor = 0.4
programmableFilter1Display.SelectScaleArray = 'None'
programmableFilter1Display.GlyphType = 'Arrow'
programmableFilter1Display.GlyphTableIndexArray = 'None'
programmableFilter1Display.GaussianRadius = 0.02
programmableFilter1Display.SetScaleArray = ['POINTS', 'pf-ic']
programmableFilter1Display.ScaleTransferFunction = 'PiecewiseFunction'
programmableFilter1Display.OpacityArray = ['POINTS', 'pf-ic']
programmableFilter1Display.OpacityTransferFunction = 'PiecewiseFunction'
programmableFilter1Display.DataAxesGrid = 'GridAxesRepresentation'
programmableFilter1Display.PolarAxes = 'PolarAxesRepresentation'
programmableFilter1Display.ScalarOpacityUnitDistance = 0.14687864221330904

# hide data in view
Hide(mesh_full_OGSNRvtu, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(programmableFilter1Display, ('POINTS', 'pf-ic'))

# rescale color and/or opacity maps used to include current data range
programmableFilter1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
programmableFilter1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'pfic'
pficLUT = GetColorTransferFunction('pfic')

# get opacity transfer function/opacity map for 'pfic'
pficPWF = GetOpacityTransferFunction('pfic')

# change representation type
programmableFilter1Display.SetRepresentationType('Surface With Edges')

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [0.0, 0.0, 10000.0]
renderView1.CameraParallelScale = 0.1704132425991815

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
