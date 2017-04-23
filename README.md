# bokeh_based_visualization
## Solving the problem of "Hover in charts not displaying data"
- For detail https://github.com/bokeh/bokeh/issues/4347
- There is a solution at http://blog.rtwilson.com/bokeh-plots-with-dataframe-based-tooltips/, but it is not perfect. It can accept static marker and color arguments, but can not accept the column to use for marker, color and size.
- So, I just improved the function of scatter_with_hover, which acts just like bokeh.charts.Scatter with a functional hover tooltip.
- "scatter_with_hover" was rewrited with the power of Basic Glyphs of bokeh.

def scatter_with_hover(df, x, y, color=None, marker=None, size=10, line_color=None,cols=None,
                       title=None, xlabel=None, ylabel=None, legend='top_right',
                       fig=None, plot_width=600, plot_height=600, tools="pan,wheel_zoom,box_zoom,save,reset", **kwargs):
        
     """
    Plots an interactive scatter plot of `x` vs `y` using bokeh, with automatic
    tooltips showing columns from `df`.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the data to be plotted
    x : str
        Name of the column to use for the x-axis values
    y : str
        Name of the column to use for the y-axis values
    color : str
        Name of the column to use for color
    marker : str
        Name of marker to use for scatter plot;
        Or, Name of the column to use for marker
    size : int or str
        Size of the marker;
        Or, name of the column to use for size of the marker
    fig : bokeh.plotting.Figure, optional
        Figure on which to plot (if not given then a new figure will be created)
    cols : list of str
        Columns to show in the hover tooltip (default is to show all)
    line_color, title, xlabel, ylabel, legend, tools, ...
        Normal arguments just like 'from bokeh.charts import Scatter'
    **kwargs
        Any further arguments to be passed to fig.scatter

    Returns
    -------
    bokeh.plotting.Figure
        Figure (the same as given, or the newly created figure)

    Example
    -------
    from scatter_with_hover import scatter_with_hover
    fig = scatter_with_hover(df, 'A', 'B')
    show(fig)

    fig = scatter_with_hover(df, 'A', 'B', cols=['C', 'D', 'E'], marker='x', color='red')
    show(fig)

    fig = scatter_with_hover(df, 'A', 'B', marker='C', color='D', size='E')
    show(fig)

    Author
    ------
    Sam Wu <wusong@live.cn>
    with thanks to Robin Wilson for original code example
    """
