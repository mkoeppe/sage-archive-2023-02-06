import os
import sys
import glob
import shutil
import sysconfig
from pathlib import Path
import fnmatch

from setuptools import setup
from distutils.command.build_scripts import build_scripts as distutils_build_scripts
from setuptools.command.build_py import build_py as setuptools_build_py
from setuptools.command.egg_info import egg_info as setuptools_egg_info
from distutils.errors import (DistutilsSetupError, DistutilsModuleError,
                              DistutilsOptionError)

class build_py(setuptools_build_py):

    def initialize_options(self):
        setuptools_build_py.initialize_options(self)
        self.plat_name = None

    def finalize_options(self):
        setuptools_build_py.finalize_options(self)
        if self.plat_name is None:
            self.plat_name = self.get_finalized_command('bdist_wheel').plat_name

    def run(self):
        HERE = os.path.dirname(__file__)
        with open(os.path.join(HERE, 'VERSION.txt')) as f:
            sage_version = f.read().strip()
        SETENV = ':'
        # Until pynac is repackaged as a pip-installable package (#30534), SAGE_LOCAL still has to be specific to
        # the Python version.  Note that as of pynac-0.7.26.sage-2020-04-03, on Cygwin, pynac is linked through
        # to libpython; whereas on all other platforms, it is not linked through, so we only key it to the SOABI.
        soabi = sysconfig.get_config_var('SOABI')
        if sys.platform == 'cygwin':
            libdir_tag = sysconfig.get_config_var('LIBDIR').replace(' ', '-').replace('\\', '-').replace('/', '-')
            ldversion = sysconfig.get_config_var('LDVERSION')
            python_tag = f'{libdir_tag}-{ldversion}'
        else:
            python_tag = f'{soabi}-{self.plat_name}'

        # On macOS, /var -> /private/var; we work around the DESTDIR staging bug #31569.
        STICKY = '/var/tmp'
        STICKY = str(Path(STICKY).resolve())
        # SAGE_ROOT will be a symlink during Sage runtime, but has to be a physical directory during build.
        SAGE_ROOT = os.path.join(STICKY, f'sage-{sage_version}-{python_tag}')
        # After building, we move the directory out of the way to make room for the symlink.
        # We do the wheel packaging from here.
        SAGE_ROOT_BUILD = SAGE_ROOT + '-build'
        # This will resolve via SAGE_ROOT.
        SAGE_LOCAL = os.path.join(SAGE_ROOT, 'local')
        SAGE_LOCAL_BUILD = os.path.join(SAGE_ROOT_BUILD, 'local')
        # The tree containing the wheel-building venv.  Not shipped as part of the
        # The built wheels are to be shipped separately.
        venv_name = f'venv-{python_tag}'
        SAGE_VENV = os.path.join(SAGE_ROOT, venv_name)
        SAGE_VENV_BUILD = os.path.join(SAGE_ROOT_BUILD, venv_name)
        # Also logs
        SAGE_LOGS = os.path.join(SAGE_ROOT, 'logs')
        SAGE_LOGS_BUILD = os.path.join(SAGE_ROOT_BUILD, 'logs')

        if Path(SAGE_ROOT).is_symlink():
            # Remove symlink created by the sage_conf runtime
            os.remove(SAGE_ROOT)

        try:
            # Within this try...finally block, SAGE_ROOT is a physical directory.

            # config.status and other configure output has to be writable.
            # So (until the Sage distribution supports VPATH builds - #21469), we have to make a copy of sage_root_source.
            #
            # The file exclusions here duplicate what is done in MANIFEST.in
            def ignore(path, names):
                # exclude embedded src trees -- except for the one of sage_conf
                if any(fnmatch.fnmatch(path, spkg) for spkg in ('*/build/pkgs/sagelib',
                                                                '*/build/pkgs/sage_docbuild',
                                                                '*/build/pkgs/sage_sws2rst')):
                    return ['src']
                return []
            shutil.copytree(os.path.join(HERE, 'sage_root_source'), SAGE_ROOT,
                            ignore=ignore)  # will fail if already exists

            # Use our copy of the sage_conf template, which contains the relocation logic
            shutil.copyfile(os.path.join(HERE, 'sage_conf.py.in'),
                            os.path.join(SAGE_ROOT, 'build', 'pkgs', 'sage_conf', 'src', 'sage_conf.py.in'))

            if os.path.exists(SAGE_LOCAL_BUILD):
                # Previously built, start from there
                print(f"### Reusing {SAGE_LOCAL_BUILD}")
                os.rename(SAGE_LOCAL_BUILD, SAGE_LOCAL)

            if os.path.exists(SAGE_VENV_BUILD):
                print(f"### Reusing {SAGE_VENV_BUILD}")
                os.rename(SAGE_VENV_BUILD, SAGE_VENV)

            if os.path.exists(SAGE_LOGS_BUILD):
                print(f"### Reusing {SAGE_LOGS_BUILD}")
                os.rename(SAGE_LOGS_BUILD, SAGE_LOGS)

            cmd = f"cd {SAGE_ROOT} && {SETENV} && ./configure --prefix={SAGE_LOCAL} --with-sage-venv={SAGE_VENV} --with-python={sys.executable} --with-system-python3=force --with-mp=gmp --without-system-mpfr --without-system-readline --enable-download-from-upstream-url --enable-fat-binary --disable-notebook --disable-r --disable-sagelib"
            print(f"Running {cmd}")
            if os.system(cmd) != 0:
                raise DistutilsSetupError("configure failed")

            shutil.copyfile(os.path.join(SAGE_ROOT, 'src', 'bin', 'sage-env-config'),
                            os.path.join(SAGE_ROOT, 'build', 'pkgs', 'sage_conf', 'src', 'bin', 'sage-env-config'))

            SETMAKE = 'if [ -z "$MAKE" ]; then export MAKE="make -j$(PATH=build/bin:$PATH build/bin/sage-build-num-threads | cut -d" " -f 2)"; fi'
            TARGETS = 'build'
            cmd = f'cd {SAGE_ROOT} && {SETENV} && {SETMAKE} && $MAKE V=0 {TARGETS}'
            if os.system(cmd) != 0:
                raise DistutilsSetupError(f"make {TARGETS} failed")
        finally:
            # Delete old SAGE_ROOT_BUILD (if any), move new SAGE_ROOT there
            shutil.rmtree(SAGE_ROOT_BUILD, ignore_errors=True)
            os.rename(SAGE_ROOT, SAGE_ROOT_BUILD)

        # Install configuration
        shutil.copyfile(os.path.join(SAGE_ROOT_BUILD, 'build', 'pkgs', 'sage_conf', 'src', 'sage_conf.py'),
                        os.path.join(HERE, 'sage_conf.py'))
        if not self.distribution.py_modules:
            self.py_modules = self.distribution.py_modules = []
        self.distribution.py_modules.append('sage_conf')
        shutil.copyfile(os.path.join(SAGE_ROOT_BUILD, 'src', 'bin', 'sage-env-config'),
                        os.path.join(HERE, 'bin', 'sage-env-config'))
        # Install built SAGE_ROOT as package data
        if not self.packages:
            self.packages = self.distribution.packages = ['']
        if not self.distribution.package_data:
            self.package_data = self.distribution.package_data = {}

        # symlink into build dir
        HERE_SAGE_ROOT = os.path.join(HERE, 'sage_root')
        if os.path.islink(HERE_SAGE_ROOT):
            os.remove(HERE_SAGE_ROOT)
        os.symlink(SAGE_ROOT_BUILD, HERE_SAGE_ROOT)

        # We do not include lib64 (a symlink) because all symlinks are followed,
        # causing another copy to be installed.
        self.distribution.package_data[''] = (
            glob.glob('sage_root/*')
            + glob.glob('sage_root/config/*')
            + glob.glob('sage_root/m4/*')
            + glob.glob('sage_root/build/**', recursive=True)
            + glob.glob('sage_root/local/*')
            + glob.glob('sage_root/local/bin/**', recursive=True)
            + glob.glob('sage_root/local/include/**', recursive=True)
            + glob.glob('sage_root/local/lib/**', recursive=True)
            + glob.glob('sage_root/local/share/**', recursive=True)
            + glob.glob('sage_root/local/var/lib/**', recursive=True)  # omit /var/tmp
            )
        #
        setuptools_build_py.run(self)

class build_scripts(distutils_build_scripts):

    def run(self):
        self.distribution.scripts.append(os.path.join('bin', 'sage-env-config'))
        if not self.distribution.entry_points:
            self.entry_points = self.distribution.entry_points = dict()
        # if 'console_scripts' not in self.distribution.entry_points:
        #     self.distribution.entry_points['console_scripts'] = []
        # self.distribution.entry_points['console_scripts'].append('sage-config=sage_conf:_main')
        distutils_build_scripts.run(self)

class egg_info(setuptools_egg_info):

    def finalize_options(self):
        ## FIXME: Tried to make sure that egg_info is run _after_ build_py
        ## cmd_build_py = self.get_finalized_command('build_py')
        ## cmd_build_py.run()    # <-- runs it a second time, not what we want
        self.distribution.install_requires = [
           'numpy @ https://github.com/sagemath/sage-wheels/releases/download/9.3.rc1/numpy-1.19.5-cp38-cp38-macosx_10_15_x86_64.whl'
        ]
        setuptools_egg_info.finalize_options(self)

setup(
    cmdclass=dict(build_py=build_py, build_scripts=build_scripts, egg_info=egg_info),
    # Do not mark the wheel as pure
    has_ext_modules=lambda: True
)
