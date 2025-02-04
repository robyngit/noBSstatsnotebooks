"""
This file contains helper functions for plotting the probability distributions.
(c) 2022 Minireferece Co. - MIT License

TODOs:
 - change x to xs (to signal it's a array-like)
 - rename all r.v. generation functions to use `gen_` prefix.
"""
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.integrate import quad
import seaborn as sns

from scipy.stats import randint    # special handling beta+1=beta
from scipy.stats import nbinom     # display parameter n as r
from scipy.stats import hypergeom  # special handling M=a+b, n=a, N=n
from scipy.stats import expon      # hide loc=0 parameter
from scipy.stats import gamma      # hide loc=0 parameter
from scipy.stats import norm



# Figure settings
# sns.set(color_codes=True)                               # turn on Seaborn styles
# plt.rc('text', usetex=True)                             # enable latex for labels
# plt.rc('font', family='serif', serif=['Palatino'])      # set font to Minireference style guide
rcparams = {
    'figure.figsize': (7,4),
    #     'figure.dpi': 300,
    'font.serif': ['Palatino', 'DejaVu Serif', 'Bitstream Vera Serif',
                   'Computer Modern Roman', 'New Century Schoolbook',
                   'Century Schoolbook L', 'Utopia', 'ITC Bookman',
                   'Bookman', 'Nimbus Roman No9 L', 'Times New Roman',
                   'Times', 'Charter', 'serif'],
    'font.family': 'serif',    
    #     'font.size': 20,
    #     'figure.titlesize': 16,
    #     'axes.titlesize':22,
    #     'axes.labelsize':20,
    #     'xtick.labelsize': 12,
    #     'ytick.labelsize': 12,
    #     'legend.fontsize': 16,
    #     'legend.title_fontsize': 18,
}
sns.set_theme(
    context="paper",
    style="whitegrid",
    palette="colorblind",  # ALT sns.color_palette('Blues', 4)
    rc=rcparams,
)



DEFAULT_PARAMS_TO_LATEX = {
    'mu': '\\mu',
    'sigma': '\\sigma',
    'lambda': '\\lambda',
    'beta': '\\beta',
    'a': 'a',
    'b': 'b',
    'N': 'N',
    'K': 'K',
    'k': 'k',
    'n': 'n',
    'p': 'p',
    'r': 'r',
}



# Utils
################################################################################

def default_labeler(params, params_to_latex):
    """
    Returns string appropriate for probability distribution label used in plot.
    """
    params_to_latex = dict(DEFAULT_PARAMS_TO_LATEX, **params_to_latex)
    label_parts = []
    for param, value in params.items():
        if param in params_to_latex:
            label_part = '$' + params_to_latex[param] + '=' + str(value) + '$'
        else:
            label_part = str(param) + '=' + str(value)
        label_parts.append(label_part)
    label = ', '.join(label_parts)
    return label

def ensure_containing_dir_exists(filepath):
    parent = os.path.join(filepath, os.pardir)
    absparent = os.path.abspath(parent)
    if not os.path.exists(absparent):
        os.makedirs(absparent)


# Continuous random variables
################################################################################

def plot_pdf(rv, xlims=None, ylims=None, rv_name="X", ax=None, title=None, label=None, linestyle='solid'):
    """
    Plot the pdf of the continuous random variable `rv` over the `xlims`.
    """
    # Setup figure and axes
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure

    # Compute limits of plot
    if xlims:
        xmin, xmax = xlims
    else:
        xmin, xmax = rv.ppf(0.000000001), rv.ppf(0.99999)
    xs = np.linspace(xmin, xmax, 1000)

    # Compute the probability mass function and plot it
    fXs = rv.pdf(xs)
    sns.lineplot(x=xs, y=fXs, ax=ax, label=label, linestyle=linestyle)
    ax.set_xlabel(rv_name.lower())
    ax.set_ylabel(f"$f_{{{rv_name}}}$")
    if ylims:
        ax.set_ylim(*ylims)

    if title and title.lower() == "auto":
        title = "Probability density function of the random variable " + rv.dist.name + str(rv.args)
    if title:
        ax.set_title(title, y=0, pad=-30)

    # return the axes
    return ax




def calc_prob_and_plot(rv, a, b, xlims=None, ax=None, title=None):
    """
    Calculate the probability random variable `rv` falls between a and b,
    and plot the area-under-the-curve visualization ofr this calculation.
    """

    # 1. calculate Pr(a<X<b) == integral of rv.pdf between x=a and x=b
    p = quad(rv.pdf, a, b)[0]

    # 2. plot the probability density function (pdf)
    if xlims:
        xmin, xmax = xlims
    else:
        xmin, xmax = rv.ppf(0.001), rv.ppf(0.999)
    x = np.linspace(xmin, xmax, 10000)
    pX = rv.pdf(x)
    ax = sns.lineplot(x=x, y=pX, ax=ax)
    if title is None:
        title = "Probability density for the random variable " + rv.dist.name + str(rv.args) \
                 + " between " + str(a) + " and " + str(b)
    ax.set_title(title, y=0, pad=-30)

    # 3. highlight the area under pX between x=a and x=b
    mask = (x > a) & (x < b)
    ax.fill_between(x[mask], y1=pX[mask], alpha=0.2, facecolor="blue")
    ax.vlines([a], ymin=0, ymax=rv.pdf(a), linestyle="-", alpha=0.5, color="blue")
    ax.vlines([b], ymin=0, ymax=rv.pdf(b), linestyle="-", alpha=0.5, color="blue")
    
    # return prob and figure axes
    return p, ax



def calc_prob_and_plot_tails(rv, x_l, x_r, xlims=None, ax=None, title=None):
    """
    Plot the area-under-the-curve visualization for the distribution's tails and
    calculate their combined probability mass: Pr({X < x_l}) + Pr({X > x_r}).
    """
    # 1. compute the probability in the left (-∞,x_l] and right [x_r,∞) tails
    p_l = quad(rv.pdf, rv.ppf(0.0000000000001), x_l)[0]
    p_r = quad(rv.pdf, x_r, rv.ppf(0.9999999999999))[0]
    p_tails = p_l + p_r

    # 2. plot the probability density function (pdf)
    if xlims:
        xmin, xmax = xlims
    else:
        xmin, xmax = rv.ppf(0.001), rv.ppf(0.999)
    x = np.linspace(xmin, xmax, 10000)
    pX = rv.pdf(x)
    ax = sns.lineplot(x=x, y=pX, ax=ax)
    if title is None:
        title = "Tails of the random variable " + rv.dist.name + str(rv.args)
    ax.set_title(title, y=0, pad=-30)

    # 3. highlight the area under pX for the tails
    mask_l = x < x_l   # left tail
    mask_u = x > x_r   # right tail
    ax.fill_between(x[mask_l], y1=pX[mask_l], alpha=0.3, facecolor="red")
    ax.fill_between(x[mask_u], y1=pX[mask_u], alpha=0.3, facecolor="red")
    ax.vlines([x_l], ymin=0, ymax=rv.pdf(x_l), linestyle="-", alpha=0.5, color="red")
    ax.vlines([x_r], ymin=0, ymax=rv.pdf(x_r), linestyle="-", alpha=0.5, color="red")

    # return prob and figure axes
    return p_tails, ax



def plot_pdf_and_cdf(rv, b=None, a=-np.inf, xlims=None, rv_name="X", title=None):
    """
    Plot side-by-side figure that shows pdf and CDF of random variable `rv`.
    If `b` is specified, the left plot will shows the area-under-the-curve
    visualization until x=b and tight plot higlights point at (b, F_X(b)).
    """
    fig, axs = plt.subplots(1, 2)
    ax0, ax1 = axs

    # figure title
    if title and title.lower() == "auto":
        title = "Probability distributions of the random variable " \
            + "$" + rv_name + "$" + " ~ " \
            + rv.dist.name + str(rv.args).replace(" ", "")
        fig.suptitle(title)
    if title:
        fig.suptitle(title)

    # 1. plot the probability density function (pdf)
    if xlims:
        xmin, xmax = xlims
    else:
        xmin, xmax = rv.ppf(0.001), rv.ppf(0.999)
    x = np.linspace(xmin, xmax, 1000)
    pX = rv.pdf(x)
    sns.lineplot(x=x, y=pX, ax=ax0)
    ax0.set_title("Probability density function")

    if b:
        # highlight the area under pX between x=a and x=b
        mask = (x > a) & (x < b)
        ax0.fill_between(x[mask], y1=pX[mask], alpha=0.2, facecolor="blue")
        ax0.vlines([b], ymin=0, ymax=rv.pdf(b), linestyle="-", alpha=0.5, color="blue")
        ax0.text(b, 0, "$b$", horizontalalignment="center", verticalalignment="top")
        ax0.text(b, rv.pdf(b)/2.5, r"Pr$(\{" + rv_name + r" \leq b \})$    ",
                 horizontalalignment="right", verticalalignment="center")

    # 2. plot the CDF
    FX = rv.cdf(x)
    sns.lineplot(x=x, y=FX, ax=ax1)
    ax1.set_title("Cumulative distribution function")

    if b:
        # highlight the point x=b
        ax1.vlines([b], ymin=0, ymax=rv.cdf(b), linestyle="-", color="blue")
        ax1.text(b, 0, "$b$", horizontalalignment="center", verticalalignment="top")
        ax1.text(b, rv.cdf(b), "$(b, F_{" + rv_name + "}(b))$",
                 horizontalalignment="right", verticalalignment="bottom")

    # return figure and axes
    return fig, axs



def generate_pdf_panel(fname, xs, model, params_matrix,
                       params_to_latex={},
                       xticks=None, ylims=None,
                       fontsize=10,
                       labeler=default_labeler):
    """
    Generate PDF and PNG figures with panel of probability density function of
    `model` over the sample space `xs` for all RV parameters specified in the
    list-of-lists `params_matrix`.
    """
    # We're drawing a figure with MxN subplots
    M = len(params_matrix)
    N = max( [len(row) for row in params_matrix] )

    # RV generation
    fXs_matrix = np.zeros( (M,N,len(xs)) )
    for i in range(0,M):
        for j in range(0,N):
            params = params_matrix[i][j]
            rv = model(**params)
            fXs_matrix[i][j] = rv.pdf(xs)

    # Generate the MxN panel of subplots
    fig, axarr = plt.subplots(M, N, sharey=True)
    # We neeed to ensure `axarr` is an MxN matrix even if M or N are 1
    if M == 1 and N == 1:
        ax = axarr
        axarr = np.ndarray((1,1), object)
        axarr[0,0] = ax
    elif M == 1:
        axarr = axarr[np.newaxis,:]
    elif N == 1:
        axarr = axarr[:, np.newaxis]

    # Construct the panel of plots
    for i in range(0,M):
        for j in range(0,N):
            ax = axarr[i][j]
            fXs = fXs_matrix[i][j]
            params = params_matrix[i][j]
            if model == expon:
                display_params = {"scale":params["scale"]}
            elif model == gamma:
                lam = 1/params["scale"]
                if lam >= 1:
                    lam = int(lam)
                display_params = {"a": params["a"], "lam":lam}
            else:
                display_params = params
            label = labeler(display_params, params_to_latex)
            sns.lineplot(x=xs, y=fXs, ax=ax)
            if ylims:
                ax.set_ylim(*ylims)
            if xticks is not None:
                ax.xaxis.set_ticks(xticks)
            ax.text(0.93, 0.86, label,
                    horizontalalignment='right',
                    transform=ax.transAxes,
                    size=fontsize)

    # Save as PDF and PNG
    ensure_containing_dir_exists(fname)
    basename = fname.replace('.pdf','').replace('.png','')
    fig.tight_layout()
    fig.savefig(basename + '.pdf', dpi=300, bbox_inches="tight", pad_inches=0.02)
    fig.savefig(basename + '.png', dpi=300, bbox_inches="tight", pad_inches=0.02)

    return fig



# Discrete random variables
################################################################################

def plot_pmf(rv, xlims=None, ylims=None, rv_name="X", ax=None, title=None, label=None):
    """
    Plot the pmf of the discrete random variable `rv` over the `xlims`.
    """
    # Setup figure and axes
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure

    # Compute limits of plot
    if xlims:
        xmin, xmax = xlims
    else:
        xmin, xmax = rv.ppf(0.000000001), rv.ppf(0.99999)
    xs = np.arange(xmin, xmax)

    # Compute the probability mass function and plot it
    fXs = rv.pmf(xs)
    fXs = np.where(fXs == 0, np.nan, fXs)  # set zero fXs to np.nan
    ax.stem(fXs, basefmt=" ", label=label)
    ax.set_xticks(xs)
    ax.set_xlabel(rv_name.lower())
    ax.set_ylabel(f"$f_{{{rv_name}}}$")
    if ylims:
        ax.set_ylim(*ylims)
    if label:
        ax.legend()

    if title and title.lower() == "auto":
        title = "Probability mass function of the random variable " + rv.dist.name + str(rv.args)
    if title:
        ax.set_title(title, y=0, pad=-30)

    # return the axes
    return ax


def plot_cdf(rv, xlims=None, ylims=None, rv_name="X", ax=None, title=None, label=None):
    """
    Plot the CDF of the random variable `rv` (discrete or continuous) over the `xlims`.
    """
    # Setup figure and axes
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure

    # Compute limits of plot
    if xlims:
        xmin, xmax = xlims
    else:
        xmin, xmax = rv.ppf(0.000000001), rv.ppf(0.99999)
    xs = np.linspace(xmin, xmax, 1000)

    # Compute the CDF and plot it
    FXs = rv.cdf(xs)
    sns.lineplot(x=xs, y=FXs, ax=ax)

    # Set plot attributes
    ax.set_xlabel(rv_name.lower())
    ax.set_ylabel(f"$F_{{{rv_name}}}$")
    if ylims:
        ax.set_ylim(*ylims)
    if label:
        ax.legend()
    if title and title.lower() == "auto":
        title = "Cumulative distribution function of the random variable " + rv.dist.name + str(rv.args)
    if title:
        ax.set_title(title, y=0, pad=-30)

    # return the axes
    return ax


def generate_pmf_panel(fname, xs, model, params_matrix,
                       params_to_latex={},
                       xticks=None,
                       fontsize=10,
                       labeler=default_labeler):
    """
    Generate PDF and PNG figures with panel of probability mass function of
    `model` over the sample space `xs` for all RV parameters specified in the
    list-of-lists `params_matrix`.
    """
    # We're drawing a figure with MxN subplots
    M = len(params_matrix)
    N = max( [len(row) for row in params_matrix] )

    # prepare x-axis ticks at aevery multiple of `kticks`
    xmax = np.max(xs) + 1

    # RV generation
    fX_matrix = np.zeros( (M,N,xmax) )
    for i in range(0,M):
        for j in range(0,N):
            params = params_matrix[i][j]
            rv = model(**params)
            low, high = rv.support()
            if high == np.inf:
                high = 1000
            calX = range(low, high+1)
            fXs = []
            for x in xs:
                if x in calX:
                    fXs.append(rv.pmf(x))
                else:
                    fXs.append(np.nan)
            fX_matrix[i][j] = fXs

    # Generate the MxN panel of subplots
    fig, axarr = plt.subplots(M, N, sharex=True, sharey=True)
    # We neeed to ensure `axarr` is an MxN matrix even if M or N are 1
    if M == 1 and N == 1:
        ax = axarr
        axarr = np.ndarray((1,1), object)
        axarr[0,0] = ax
    elif M == 1:
        axarr = axarr[np.newaxis,:]
    elif N == 1:
        axarr = axarr[:, np.newaxis]

    # Construct the panel of plots
    for i in range(0,M):
        for j in range(0,N):
            ax = axarr[i][j]
            fX = fX_matrix[i][j]
            params = params_matrix[i][j]
            if model == randint:
                display_params = {"low":params["low"], "high":params["high"]-1}
            elif model == hypergeom:
                display_params = {"a":params["n"], "b":params["M"]-params["n"], "n":params["N"]}
            elif model == nbinom:
                display_params = {"r":params["n"], "p":params["p"]}
            else:
                display_params = params
            label = labeler(display_params, params_to_latex)
            markerline, _stemlines, _baseline = ax.stem(fX, basefmt=" ")
            plt.setp(markerline, markersize = 2)
            if xticks is not None:
                ax.xaxis.set_ticks(xticks)
            ax.text(0.95, 0.86, label,
                    horizontalalignment='right',
                    transform=ax.transAxes,
                    size=fontsize)

    # Save as PDF and PNG
    ensure_containing_dir_exists(fname)
    basename = fname.replace('.pdf','').replace('.png','')
    fig.tight_layout()
    fig.savefig(basename + '.pdf', dpi=300, bbox_inches="tight", pad_inches=0.02)
    fig.savefig(basename + '.png', dpi=300, bbox_inches="tight", pad_inches=0.02)
    
    return fig


# Diagnositic plots (used in Section 2.7 Random variable generation)
################################################################################
# The function qq_plot tries to imitate the behaviour of the function `qqplot`
# defined in `statsmodels.graphics.api`. Usage: `qqplot(data, dist=norm(0,1), line='q')`. See:
# https://github.com/statsmodels/statsmodels/blob/main/statsmodels/graphics/gofplots.py#L912-L919
#
# TODO: figure out how to plot all of data correctly: currenlty missing first and last data point

def qq_plot(data, dist, ax=None, xlims=None, filename=None):
    # Setup figure and axes
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure

    # Add the Q-Q scatter plot
    qs = np.linspace(0, 1, len(data)+1)
    xs = dist.ppf(qs)
    ys = np.quantile(data, qs)
    sns.scatterplot(x=xs, y=ys, ax=ax, alpha=0.2)

    # Compute the parameters m and b for the diagonal
    xq25, xq75 = dist.ppf([0.25, 0.75])
    yq25, yq75 = np.quantile(data, [0.25,0.75])
    m = (yq75-yq25)/(xq75-xq25)
    b = yq25 - m * xq25
    # add the line  y = m*x+b  to the plot
    linexs = np.linspace(min(xs[1:]),max(xs[:-1]))
    lineys = m*linexs + b
    sns.lineplot(x=linexs, y=lineys, ax=ax, color="r")

    # Handle keyword arguments
    if xlims:
        ax.set_xlim(xlims)
    if filename:
        basename = filename.replace('.pdf','').replace('.png','')
        fig.tight_layout()
        fig.savefig(basename + '.pdf', dpi=300, bbox_inches="tight", pad_inches=0.02)
        fig.savefig(basename + '.png', dpi=300, bbox_inches="tight", pad_inches=0.02)

    return ax





# Random samples
################################################################################

def gen_samples(rv, n=30, N=10):
    """
    Generate `N` samples of size `n` from the random variable `rv`.
    Returns a pd.DataFrame with `N` columns containing the samples.
    """
    samples = {}
    for i in range(0, N):
        column_name = "sample" + str(i)
        samples[column_name] = rv.rvs(n)
    samples_df = pd.DataFrame(samples)
    return samples_df


def plot_samples(samples_df, ax=None, xlims=None, filename=None):
    """
    Draw a strip plots for each of the columns in `samples_df`.
    Annotate each strip plot with the mean for each sample.
    """
    n, N = samples_df.shape  # sample size, number of samples

    # 1. Setup figure and axes
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure

    # 2. Plot the samples as strip plot
    pal = "dark:b"
    sns.stripplot(samples_df, orient="h", palette=pal, ax=ax)

    # 3. Add diamond-shaped marker to indicate mean in each sample
    for i in range(0, N):
        column_name = "sample" + str(i)
        xbar_i = samples_df[column_name].mean()
        ax.scatter(xbar_i, i, marker="D", s=75, color="r", zorder=10)

    # 4. Handle keyword arguments
    if xlims:
        ax.set_xlim(xlims)
    if filename:
        basename = filename.replace('.pdf','').replace('.png','')
        fig.tight_layout()
        fig.savefig(basename + '.pdf', dpi=300, bbox_inches="tight", pad_inches=0.02)
        fig.savefig(basename + '.png', dpi=300, bbox_inches="tight", pad_inches=0.02)




def gen_sampling_dist(rv, statfunc=np.mean, n=30, N=1000):
    """
    Generate `N` samples of size `n` from the random variable `rv`
    and calculate the statistic `statfunc` from each sample.
    """
    stats = []
    for i in range(0, N):
        sample = rv.rvs(n)
        stat = statfunc(sample)
        stats.append(stat)
    return stats


def plot_sampling_dist(stats, label=None, xlims=None, binwidth=None, ax=None, filename=None):
    """
    Plot a combined histogram and strip plot of the values in `stats`.
    """
    # 1. Setup figure and axes
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure
    if binwidth is None:
        if xlims is None:
            xlims = min(stats), max(stats)
        binwidth = (xlims[1]-xlims[0]) / 30            
    
    # 2. Plot a histogram of the sampling distribution
    sns.histplot(stats, binwidth=binwidth, stat="density", color="r", ax=ax, label=label)

    # 3. add the scatter plot of `stats` below
    y_offset = 1/(100*binwidth)
    sns.scatterplot(x=stats, y=-y_offset, ax=ax, color="r", marker="D", s=30, alpha=0.1)

    # 4. Handle keyword arguments
    if xlims:
        ax.set_xlim(xlims)
    if filename:
        basename = filename.replace('.pdf','').replace('.png','')
        fig.tight_layout()
        fig.savefig(basename + '.pdf', dpi=300, bbox_inches="tight", pad_inches=0.02)
        fig.savefig(basename + '.png', dpi=300, bbox_inches="tight", pad_inches=0.02)


        


# Panels illustrating CLT
################################################################################

        
def plot_samples_panel(rv, xlims, N=10, ns=[10,30,100], filename=None):
    """
    Draw a panel of strip plots for `N` sample with sizes `ns`.
    Need to pass `xlims` because cannot be determined automatically.
    """
    fig, axs = plt.subplots(1, len(ns), sharey=True, figsize=(10,2.5))

    for n, ax in zip(ns, axs):
        samples_df = gen_samples(rv, n=n, N=N)
        plot_samples(samples_df, xlims=xlims, ax=ax)
        ax.set_title(f"Samples of size $n={n}$")

    if filename:
        basename = filename.replace('.pdf','').replace('.png','')
        fig.tight_layout()
        fig.savefig(basename + '.pdf', dpi=300, bbox_inches="tight", pad_inches=0.02)
        fig.savefig(basename + '.png', dpi=300, bbox_inches="tight", pad_inches=0.02)



def plot_sampling_dists_panel(rv, xlims, N=1000, ns=[10,30,100], binwidth=None, filename=None):
    """
    Draw a panel of combined histogram and strip plot of the sampling distibutions
    of random variable `rv` for sample sizes `ns`.
    Need to pass appropriate `xlims` and `binwidth` parameters depending on `rv`.
    """
    fig, axs = plt.subplots(1, len(ns), sharey=True, figsize=(10,2.5))

    # plot parameters
    xs = np.linspace(*xlims, 1000)

    xbarss = []
    for n, ax in zip([10,30,100], axs):
        # A. generate and plot sampling distributoin
        xbars = gen_sampling_dist(rv, statfunc=np.mean, n=n, N=N)
        plot_sampling_dist(xbars, ax=ax, xlims=xlims, binwidth=binwidth, label=f"$n={n}$")
        # B. plot the distribution predicted by the CLT
        rvXbar = norm(rv.mean(), rv.std()/np.sqrt(n))
        sns.lineplot(x=xs, y=rvXbar.pdf(xs), ax=ax, color="m")
        xbarss.append(xbars)

    if filename:
        basename = filename.replace('.pdf','').replace('.png','')
        fig.tight_layout()
        fig.savefig(basename + '.pdf', dpi=300, bbox_inches="tight", pad_inches=0.02)
        fig.savefig(basename + '.png', dpi=300, bbox_inches="tight", pad_inches=0.02)
    
    return xbarss
