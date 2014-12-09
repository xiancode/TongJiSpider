
from cx_Freeze import setup,Executable

includefiles = []
includes = ['scrapy','pkg_resources','lxml.etree','lxml._elementpath']

build_options = {'compressed' : True,
                 'optimize'   :2,
                 'namespace_packages' : ['scrapy','pkg_resources'],
                 'include_files':includefiles,
                 'includes'    : includes,
                 'excludes'   :[]
                 }

executable = Executable(script="F:\\TongJiSpider\\StatisticDataScrapy.py",
                        copyDependentFiles=True,
                        includes = includes)

setup(name = 'TongJiSpider',
      version = '1.0',
      description = 'TongJiSpider',
      options = {'build_exe':build_options},
      executables=[executable])
