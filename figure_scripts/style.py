import os
import matplotlib
matplotlib.use('pgf')
import matplotlib.pyplot as plt
TEXTW = 394.35522/72.27   # inches, MDPI \textwidth
FULLW = 525.23764/72.27   # inches, full width (adjustwidth -\extralength)
plt.rcParams.update({
 'pgf.texsystem':'pdflatex','pgf.rcfonts':False,
 'pgf.preamble':r'\usepackage[T1]{fontenc}\usepackage{mathpazo}\usepackage{textcomp}\renewcommand{\ttdefault}{lmtt}\pdfmapfile{+lm.map}',
 'text.usetex':True,'font.family':'serif',
 'font.size':9,'axes.labelsize':9.5,'axes.titlesize':9.5,
 'xtick.labelsize':9,'ytick.labelsize':9,'legend.fontsize':9,
 'axes.linewidth':0.6,'xtick.major.width':0.6,'ytick.major.width':0.6,
 'xtick.major.size':3,'ytick.major.size':3,'lines.linewidth':1.2,
 'axes.spines.top':False,'axes.spines.right':False,
 'legend.frameon':False,'savefig.dpi':600,
})

os.makedirs('out', exist_ok=True)
