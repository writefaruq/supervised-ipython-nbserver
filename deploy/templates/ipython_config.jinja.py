# IPydra
# Template for ipython notebook config

c = get_config()
c.NotebookApp.enable_mathjax = True
c.NotebookApp.open_browser = False
c.NotebookApp.ipython_dir = u'{{ ipython_dir }}'

c.IPKernelApp.pylab = 'inline'
c.NotebookManager.notebook_dir = u'{{ notebook_dir }}'
