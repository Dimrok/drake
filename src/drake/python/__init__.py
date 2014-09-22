# Copyright (C) 2014, Quentin "mefyl" Hocquet
#
# This software is provided "as is" without warranty of any kind,
# either expressed or implied, including but not limited to the
# implied warranties of fitness for a particular purpose.
#
# See the LICENSE file for more information.

import drake

class Package(drake.VirtualNode):

  def __init__(self, name, root, nodes):
    super().__init__(name)
    self.__root_source = drake.path_source(root)
    self.__root_build = drake.path_build(root)
    self.__nodes = nodes
    for node in nodes:
      self.dependency_add(node)

  @property
  def pythonpath(self):
    return [self.__root_source, self.__root_build]
