# trace generated using paraview version 5.8.1
#
# To ensure correct image size when batch processing, please search
# for and uncomment the line `# renderView*.ViewSize = [*,*]`

#### import the simple module from the paraview
from paraview.simple import *
import numpy as np

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'PVD Reader'
#shear_pf_pcs_1pvd = PVDReader(FileName='/Users/mollaali/Opening/PhaseField/DiagonalPulling/full_center_fixed/Masonry/3033530/shear_pf_pcs_1.pvd')
shear_pf_pcs_1pvd = PVDReader(FileName='/Users/mollaali/Opening/PhaseField/DiagonalPulling/half_unfixed_a_eff/results/shear_pf.pvd')

#shear_pf_pcs_1pvd = PVDReader(FileName='/Users/mollaali/Opening/PhaseField/shear/half/results/shear_pf.pvd')

shear_pf_pcs_1pvd.CellArrays = ['cum_grad_d', 'damage', 'grad_damage', 'u_dot_grad_d', 'width']
shear_pf_pcs_1pvd.PointArrays = ['NodalForces', 'displacement', 'epsilon', 'pf-ic', 'phasefield', 'sigma']


################
# get animation scene
animationScene1 = GetAnimationScene()

# get the time-keeper
timeKeeper1 = GetTimeKeeper()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [628, 301]

# get layout
layout1 = GetLayout()

# show data in view
shear_pf_pcs_1pvdDisplay = Show(shear_pf_pcs_1pvd, renderView1, 'UnstructuredGridRepresentation')


# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(shear_pf_pcs_1pvdDisplay, ('POINTS', 'phasefield'))

# rescale color and/or opacity maps used to include current data range
shear_pf_pcs_1pvdDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
shear_pf_pcs_1pvdDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'phasefield'
phasefieldLUT = GetColorTransferFunction('phasefield')

# get opacity transfer function/opacity map for 'phasefield'
phasefieldPWF = GetOpacityTransferFunction('phasefield')

animationScene1.GoToLast()
##################

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [628, 305]

# show data in view
#shear_pf_pcs_1pvdDisplay = Show(shear_pf_pcs_1pvd, renderView1, 'UnstructuredGridRepresentation')


# create a new 'Gradient Of Unstructured DataSet'
gradientOfUnstructuredDataSet1 = GradientOfUnstructuredDataSet(Input=shear_pf_pcs_1pvd)
gradientOfUnstructuredDataSet1.ScalarArray = ['POINTS', 'NodalForces']

# Properties modified on gradientOfUnstructuredDataSet1
gradientOfUnstructuredDataSet1.ScalarArray = ['POINTS', 'phasefield']
gradientOfUnstructuredDataSet1.ResultArrayName = 'Grad_d'

# show data in view
#gradientOfUnstructuredDataSet1Display = Show(gradientOfUnstructuredDataSet1, renderView1, 'UnstructuredGridRepresentation')


programmableFilter1 = ProgrammableFilter(Input=gradientOfUnstructuredDataSet1)
# Properties modified on programmableFilter1
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

num_nodes, num_comp = coord.shape
print(num_comp)
print(num_nodes)

Wnode = np.zeros(num_nodes)
mm=0
nn=0
for i, x in enumerate(coord):

    u_x = u[i][0]
    u_y = u[i][1]

    coord_x = coord[i][0]
    coord_y = coord[i][1]



    gd_x = grad_d[i][0]
    gd_y = grad_d[i][1]
    Wnode[i] = (u_x*gd_y-u_y*gd_x)


print("mm",mm)
print("nn",nn)

Wnode_vtk = numpy_to_vtk(Wnode, 1)
Wnode_vtk.SetName("W_node")
output.GetPointData().AddArray(Wnode_vtk)
 """

# show data in view
programmableFilter1Display = Show(programmableFilter1, renderView1, 'UnstructuredGridRepresentation')

# find source
#shear_pf_pcs_1pvd = FindSource('shear_pf_pcs_1.pvd')
output = open('/Users/mollaali/Opening/PhaseField/DiagonalPulling/half_unfixed_a_eff/results/Shearopening_l0p005.csv','w+')
#output = open('/Users/mollaali/Opening/PhaseField/shear/half/results/Shearopening_l0p01.csv','w+')
#
#
h = '0.0025'#argv[3]
if h == '0.0025':
	x = np.linspace(-0.12,0.12,240)
#
for i in range(len(x)):
     slice1 = Slice(Input=programmableFilter1)
     slice1.SliceType = 'Plane'
     slice1.SliceOffsetValues = [0.0]
     slice1.SliceType.Origin = [x[i], 0., 0.]
     slice1.SliceType.Normal = [1.0, 0.0, 0.0]

     integrateVariables1 = IntegrateVariables(Input=slice1)
     DataSliceFile = paraview.servermanager.Fetch(integrateVariables1)
     print(x[i], DataSliceFile.GetPointData().GetArray('W_node').GetValue(0))
     output.write("%s\t%s\n"%(x[i], DataSliceFile.GetPointData().GetArray('W_node').GetValue(0)))


output.close()
#     #print(x[i], DataSliceFile.GetCellData().GetArray('u_dot_grad_d').GetValue(0))
#     #output2.write("%s\t  %s \n" %(x[i],DataSliceFile.GetCellData().GetArray('u_dot_grad_d').GetValue(0)))
