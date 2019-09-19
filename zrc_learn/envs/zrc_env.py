import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import numpy.ctypeslib as npct
import ctypes
from ctypes import c_int
from ctypes import c_float
from ctypes import byref
from ctypes import c_void_p
import os

array_1d_float = npct.ndpointer(dtype=np.float32, ndim=1, flags='CONTIGUOUS')
array_2d_float = npct.ndpointer(dtype=np.float32, ndim=2, flags='CONTIGUOUS')
c_float_p = ctypes.POINTER(c_float)
c_int_p = ctypes.POINTER(c_int)

libzrcgympath = 'C:\\GitHub\\aumfer\\zrc-c\\build\\libzrcgym\\Release\\'
os.environ['PATH'] = libzrcgympath + os.pathsep + os.environ['PATH']

# OSX or linux
#from ctypes.util import find_library
#libm = ctypes.cdll.LoadLibrary(find_library('m'))

libzrcgym = ctypes.cdll.LoadLibrary('libzrcgym.dll')
libzrcgym.env_observation_length.restype = c_int
libzrcgym.env_observation_length.argtypes = None
libzrcgym.env_action_length.restype = c_int
libzrcgym.env_action_length.argtypes = None
libzrcgym.env_create.restype = c_void_p
libzrcgym.env_create.argtypes = None
libzrcgym.env_delete.restype = None
libzrcgym.env_delete.argtypes = [c_void_p]
libzrcgym.env_reset.restype = None
libzrcgym.env_reset.argtypes = [c_void_p, array_1d_float]
libzrcgym.env_step.restype = None
libzrcgym.env_step.argtypes = [c_void_p, array_1d_float, array_1d_float, c_float_p, c_int_p]
libzrcgym.env_render.restype = None
libzrcgym.env_render.argtypes = [c_void_p]

class ZrcEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
      #self.obs_shape = (64, int(libzrcgym.env_observation_length()/64),)
      self.obs_shape = (libzrcgym.env_observation_length(),)
      self.action_shape = (libzrcgym.env_action_length(),)
      self.action_space = spaces.Box(low=-1, high=+1, shape=self.action_shape, dtype=np.float32)
      self.observation_space = spaces.Box(low=-1, high=+1, shape=self.obs_shape, dtype=np.float32)
      self.env = libzrcgym.env_create()
      #self.seed()
      #self.reset()
  def __del__(self):
      libzrcgym.env_delete(self.env)
  def step(self, action):
      observation = np.empty(self.obs_shape, dtype=np.float32)
      reward = c_float()
      done = c_int()
      libzrcgym.env_step(self.env, action, observation, byref(reward), byref(done))
      return observation, reward.value, bool(done.value), {}
  def reset(self):
      observation = np.empty(self.obs_shape, dtype=np.float32)
      libzrcgym.env_reset(self.env, observation)
      return observation
  def render(self, mode='human'):
      libzrcgym.env_render(self.env)
  def close(self):
      print("close")
