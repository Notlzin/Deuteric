# test_vgpu.py
from src.vGPU import vGPU

gpu = vGPU(20, 5)
gpu.hookStdout()  # initialize internal GPUStdout

# send strings directly through receive (which now uses GPUStdout internally)
gpu._gpuStdout.vgpu.drawChar("Hello Deuteric!\n")
gpu._gpuStdout.write("vGPU STDOUT only 😎")
