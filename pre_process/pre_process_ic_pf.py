# trace generated using paraview version 5.5.2

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'XML Unstructured Grid Reader'
surfing_UniformQudMesh_Hansen_OGSNRvtu = XMLUnstructuredGridReader(FileName=["/Users/mollaali/Downloads/SemiCircularBend/quad2x1.vtu"])

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1296, 821]

# show data in view
surfing_UniformQudMesh_Hansen_OGSNRvtuDisplay = Show(surfing_UniformQudMesh_Hansen_OGSNRvtu, renderView1)

# trace defaults for the display properties.
surfing_UniformQudMesh_Hansen_OGSNRvtuDisplay.Representation = 'Surface'

# reset view to fit data
renderView1.ResetCamera()

#changing interaction mode based on data extents
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [1.0, 0.0, 10000.0]
renderView1.CameraFocalPoint = [1.0, 0.0, 0.0]

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Calculator'
calculator1 = Calculator(Input=surfing_UniformQudMesh_Hansen_OGSNRvtu)

# Properties modified on calculator1
calculator1.ResultArrayName = 'coordinates'
calculator1.Function = 'coords'

# show data in view
calculator1Display = Show(calculator1, renderView1)

# trace defaults for the display properties.
calculator1Display.Representation = 'Surface'

# hide data in view
Hide(surfing_UniformQudMesh_Hansen_OGSNRvtu, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Point Data to Cell Data'
pointDatatoCellData1 = PointDatatoCellData(Input=calculator1)

# show data in view
pointDatatoCellData1Display = Show(pointDatatoCellData1, renderView1)

# trace defaults for the display properties.
pointDatatoCellData1Display.Representation = 'Surface'

# hide data in view
Hide(calculator1, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Programmable Filter'
programmableFilter1 = ProgrammableFilter(Input=pointDatatoCellData1)

# Properties modified on programmableFilter1
programmableFilter1.Script = 'import numpy as np\nimport math\nfrom vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk\n\nin_data = self.GetInputDataObject(0, 0)\noutput = self.GetOutputDataObject(0)\n\nin_point_data = in_data.GetPointData()\nin_cell_data = in_data.GetCellData()\n\n# get the point coordinates:\ncoord_vtk = in_data.GetPoints().GetData()\ncoord = vtk_to_numpy(coord_vtk)\n\n# get the cell coordinates\ncell_coord_vtk = in_cell_data.GetAbstractArray("coordinates")\ncell_coord = vtk_to_numpy(cell_coord_vtk)\n\n# initialize phase_field (point data)\nnum_nodes, num_comp = coord.shape\nphase_field = np.ones(num_nodes)\n\nh=6.25e-3\na0=0.5\nfor node_id, x in enumerate(coord):\n    if x[0]< a0+1e-3  and x[1] < h and x[1] > -h:\n        phase_field[node_id] = 0.0\n\n# initialize Gc (cell data)\nnum_cell, num_comp = cell_coord.shape\nGc = np.ones(num_cell)\nYoung = np.zeros(num_cell)\n\nx1 = 0.\ny1 = 0.\nx2 = 2.\ny2 = 0.\n\nlc=15.e-3\nb = 2*lc\n\nseg_len = math.sqrt((x1-x2)**2 + (y1-y2)**2)\n\nfor i, x in enumerate(cell_coord):\n    # distance from (x1, y1) to the interception point\n    d1 = ((x2-x1)*(x[0]-x1) + (y2-y1)*(x[1]-y1))/seg_len\n\n    # distance from a point to the line segment\n    if(d1 < 0):\n        dist = math.sqrt((x1-x[0])**2 + (y1-x[1])**2)\n    elif(d1 > seg_len):\n        dist = math.sqrt((x2-x[0])**2 + (y2-x[1])**2)\n    else:\n        dist = abs( (y2-y1)*x[0] - (x2-x1)*x[1] + x2*y1 - y2*x1 )/seg_len\n\n    Gc[i] = 5.4\n    if (dist < b):\n        Gc[i] = 2.7\n\n    Young[i] = 210e9\n    if x[0] < 0.0:\n        Young[i] = 210e9 \n\nphase_field_vtk = numpy_to_vtk(phase_field, 1)\nphase_field_vtk.SetName("pf-ic")\nGc_vtk = numpy_to_vtk(Gc, 1)\nGc_vtk.SetName("Gc")\nYoung_vtk = numpy_to_vtk(Young, 1)\nYoung_vtk.SetName("Young")\n\noutput.GetPointData().AddArray(phase_field_vtk)\noutput.GetCellData().AddArray(Gc_vtk)\noutput.GetCellData().AddArray(Young_vtk)'

# show data in view
programmableFilter1Display = Show(programmableFilter1, renderView1)

# trace defaults for the display properties.
programmableFilter1Display.Representation = 'Surface'

# hide data in view
Hide(pointDatatoCellData1, renderView1)

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

# set scalar coloring
ColorBy(programmableFilter1Display, ('CELLS', 'Gc'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(pficLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
programmableFilter1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
programmableFilter1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'Gc'
gcLUT = GetColorTransferFunction('Gc')

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [1.0, 0.0, 10000.0]
renderView1.CameraFocalPoint = [1.0, 0.0, 0.0]
renderView1.CameraParallelScale = 1.118033988749895

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
