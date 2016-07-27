import drake
import drake.git
import os

class Packager(drake.Builder):

  """
  Only the name of the folder containing the licenses needs to be passed.
  The builder will automatically populate the list of source nodes by traversing
  the folder.
  """

  def __init__(self, license_folder, out_file):
    self.__license_folder = license_folder
    self.__target = out_file
    self.__context = drake.Drake.current.prefix
    licenses = list()
    def traverse(folder, in_dir):
      git = drake.git.Git(folder)
      for f in git.ls_files():
        path = str(drake.path_source() / in_dir / folder / f)
        if os.path.isdir(path):
          traverse('%s/%s' % (folder, f), '%s/%s' % (in_dir, folder))
        else:
          licenses.append(drake.node('%s/%s' % (folder, f)))
    traverse(license_folder, self.__context)
    super().__init__(licenses, [out_file])
    self.__sorted_sources = \
      list(map(lambda s: str(s), self.sources().values()))
    self.__sorted_sources.sort(key = lambda s: s.lower())

  def execute(self):
    print('Generating aggregated license file: %s' % self.__target)
    with open(str(self.__target), 'w') as out:
      for license in self.__sorted_sources:
        l_name = license.replace(
          '%s/%s/' % (self.__context, self.__license_folder), '')
        out.write('# Begin: %s\n(*%s\n' % (l_name, 78 * '-'))
        with open(str(drake.path_source() / license), 'r') as f:
          out.write(f.read())
        out.write('\n%s*)\n# End: %s\n\n' % (78 * '-', l_name))
    return True
