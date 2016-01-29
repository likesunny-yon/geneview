"""
Functions for plotting qq-plot.

Copytright (c) Shujia Huang
Date: 2016-01-28

"""
from itertools import cycle

import numpy as np
import matplotlib.pyplot as plt

from geneview.util import is_numeric, despine, offset_spines

def ppoints(n, a=0.5):
    """ 
    numpy analogue `R`'s `ppoints` function.

    ppoints() is used in qqplot and qqnorm to generate the set of 
    probabilities at which to evaluate the inverse distribution.

    see details at 
        http://stat.ethz.ch/R-manual/R-patched/library/stats/html/ppoints.html 

    Parameters
    ----------
    n : a number or array type
        If n is an array or list, ``n`` will re-assign to ``n=len(n)``
    
    a : float, optional, default: 0.5
        The offset fraction to be used; typically in (0, 1)
        Recommend to set: a = 3.0/8.0 if n <= 10 else 0.5 


    Returns
    -------
        A list of value calculates by this formular:
        (1:n - a)/(n + (1-2a)


    Notes
    -----
    * Becker, R. A., Chambers, J. M. and Wilks, A. R. (1988) The New S Language. Wadsworth & Brooks/Cole.
    * Blom, G. (1958) Statistical Estimates and Transformed Beta Variables. Wiley

    """
    if a < 0 or a > 1:
        msg = "`a` can just be any float value in 0 < a < 1."
        raise ValueError(msg) 

    try:
        n = np.float(len(n))
    except TypeError:
        n = np.float(n)

    # ``n`` is a float value
    return (np.arange(n) + 1 - a)/(n + 1 - 2*a)

def qqplot(pvalues, ax=None, color='k', ablinecolor='r', alpha=0.8, 
           mlog10=True, **kwargs):
    """
    Creat a Q-Q plot.

    Creates a quantile-quantile plot from p-values from a GWAS study.
    *CAUSION: The x-axis(expected) is created from uniform distribution 
              for GWAS*.

    Parameters
    ----------
    pvalues : float. list-like and just 1-D
        A numeric list or array of p-values.

    ax : matplotlib axis, optional
        Axis to plot on, otherwise uses current axis.

    color : matplotlib color, optional, default: 'k' (black) 
        The dots color in the plot

    ablinecolor: matplotlib color, optional, default: 'r' (red)
        Color for the abline in plot. ``ablinecolor=None`` means 
        do not plot the abline.

    mlog10 : bool, optional, default: True 
        If true, -log10 of the y_value(always be the p-value) is plotted. It
        isn't very useful to plot raw p-values in GWAS QQ plot.

    kwargs : key, value pairings
        Other keyword arguments are passed to ``plt.scatter()``
        (in matplotlib.pyplot).


    Returns
    -------
    ax : matplotlib Axes
        Axes object with the manhattanplot.


    Notes
    -----
    1. This plot function is not just suit for GWAS QQ plot, it could
       also be used for creating QQ plot for other data, which format 
       are list-like ::
        [value1, value2, ...] (all the values should between 0 and 1)

    -----
    """
    # Draw the plot and return the Axes
    if ax is None:
        ax = plt.gca()

    if not all(map(is_numeric, pvalues)):
        msg = 'Input must all be numeric.'
        raise ValueError(msg)

    pvalues = np.array(pvalues, dtype=float)
    # limit to (0, 1)
    pvalues = pvalues[pvalues>0.0]
    pvalues = pvalues[pvalues<1.0]
    
    # Observed and expected
    if mlog10:
        o = -np.log10(sorted(pvalues, reverse=True)) # increasing
        e = -np.log10(ppoints(len(pvalues)))[::-1]
    else:
        o = sorted(pvalues)
        e = ppoints(len(pvalues))

    # x is for expected; y is for observed value
    ax.scatter(e, o, c=color, alpha=alpha, edgecolors='none', **kwargs) 

    # Remove the 'top' and 'right' plot spines by default
    despine(ax=ax)

    ax.set_xlim(xmin=e.min())  
    ax.set_ylim(ymin=o.min())  

    if ablinecolor:
        # plot the y=x line by expected: uniform distribution data
        ax.plot([e.min(), e.max()], [e.min(), e.max()], color=ablinecolor, 
                linestyle='-')

    return ax





