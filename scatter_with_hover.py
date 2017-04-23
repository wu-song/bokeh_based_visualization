from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool

_marker_types = [
    "circle",
    "square",
    "triangle",
    "diamond",
    "inverted_triangle",
    "asterisk",
    "cross",
    "x",
    "circle_cross",
    "circle_x",
    "square_x",
    "square_cross",
    "diamond_cross",
]

palette = [
'#7BC65F',
'#6698EC',
'#E6754C',
'#33BEB0',
'#D066F6',
'#F45665',
'#3CFF00',
'#0432FF',
'#C10000',
'#73FDD6',
'#8C00DB',
'#FF0000',
'#FDFF00',
'#EED1D1',
'#FFC000',
'#F938EB',
'#BF9000',
'#AAAAAA',
'#000000']

conversions = {
            "*": "asterisk",
            "+": "cross",
            "o": "circle",
            "ox": "circle_x",
            "o+": "circle_cross"
        }

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
    df_temp = df.copy()
    df_temp.insert(0, '__index__', df_temp.index)
    if cols is None:
        # Display *all* columns in the tooltips
        hover = HoverTool(tooltips = [(c, '@' + c) for c in df_temp.columns])
    else:
        # Display just the given columns in the tooltips
        hover = HoverTool(tooltips = [(c, '@' + c) for c in cols])

    if color is None: color = palette[5] #
    if marker is None:
        marker = 'circle'
    elif marker in conversions:
        marker = conversions[marker]

    if color in df_temp.columns:
        color_keys = list(set(df_temp[color]))
        color_dic = dict(zip(palette, color_keys)) # uesed for defining 'color_marker_legend'
        df_temp['__color'] = list(df_temp[color].map(dict(zip(color_keys, palette))))
        df_temp['__color'] = df_temp['__color'].fillna('#000000')
    else:
        df_temp['__color'] = color

    if marker in df_temp.columns:
        marker_keys = list(set(df_temp[marker]))
        marker_dic = dict(zip(_marker_types, marker_keys)) # uesed for defining 'color_marker_legend'
        df_temp['__marker'] = list(df_temp[marker].map(dict(zip(marker_keys, _marker_types))))
        df_temp['__marker'] = df_temp['__marker'].fillna('x')
    else:
        df_temp['__marker'] = marker
    # If we haven't been given a Figure obj then create it with default size.
    if fig is None:
        fig = figure(width=plot_width, height=plot_height, title=title, tools=tools)

    if xlabel is None: xlabel = x
    if ylabel is None: ylabel = y
    fig.xaxis.axis_label = xlabel
    fig.yaxis.axis_label = ylabel

    grouped_df = df_temp.groupby(['__color', '__marker'])
    for color_marker, df_marker in grouped_df:
        #print(marker, df_marker.shape)
        #print(df_marker)
        source = ColumnDataSource(data=df_marker)

        # define legend's format
        if 'color_dic' in dir():
            if 'marker_dic' in dir():
                color_marker_legend = (color_dic[color_marker[0]], marker_dic[color_marker[1]])
            else:
                color_marker_legend = color_dic[color_marker[0]] # 反推‘marker’列的值
        else:
            if 'marker_dic' in dir():
                color_marker_legend = marker_dic[color_marker[1]]
            else:
                color_marker_legend = None

        fig.scatter(x, y, source=source, line_color=line_color, fill_color=color_marker[0], marker=color_marker[1], \
                    size=size, legend=str(color_marker_legend), **kwargs)

    fig.legend.location = legend
    fig.add_tools(hover)
    return fig
