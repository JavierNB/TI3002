import pandas as pd
import yfinance as yf
from datetime import datetime
from bokeh.models.sources import ColumnDataSource
from bokeh.io import curdoc # returns the current document for a Bokeh application
from bokeh.models import ColumnDataSource, Select, DataTable, TableColumn, DatePicker, Div
from bokeh.layouts import column, row, layout
from bokeh.plotting import figure, show

DEFAULT_TICKERS = ['AAPL', 'GOOG', 'MSFT', 'NFLX', 'TSLA']
START, END = '2018-01-02', '2024-01-02'

def load_ticker(tickers):
    """
    Load closing prices for selected tickers within the specified date range
    """
    df = yf.download(tickers, start=date_picker_start.value, end=date_picker_end.value)
    df = df['Close'].dropna()
    #print(df.head())
    #print(df.info())
    return df

# static_data = load_ticker(DEFAULT_TICKERS)

def get_data(t1, t2, start=START, end=END):
    d = load_ticker(DEFAULT_TICKERS)
    df = d[[t1, t2]].loc[start: end]
    returns = df.pct_change().add_suffix('_returns') # Percentage change between the current and a prior element.
    df = pd.concat([df, returns], axis=1)
    return df.dropna()

def nix(val, lst):
    return [x for x in lst if x!= val]

header_div = Div(
    text="""
<h1>A simple Bokeh Dashboard</h1>
<p>Data: Financial and market data fetched from Yahoo finance <a href="https://pypi.org/project/yfinance/" target="_blank">yfinance</a></p target="_blank">
""",
    sizing_mode="stretch_width",
)

ticker1 = Select(value='AAPL', options = nix('GOOG', DEFAULT_TICKERS))
ticker2 = Select(value='GOOG', options = nix('AAPL', DEFAULT_TICKERS))

# Create two DatePicker widgets
date_picker_start = DatePicker(title="Start Date", value=START, min_date="2000-01-01", max_date=datetime.today().strftime('%Y-%m-%d'))
date_picker_end = DatePicker(title="End Date", value=END, min_date="2000-01-01", max_date=datetime.today().strftime('%Y-%m-%d'))

# Source data
data = get_data(ticker1.value, ticker2.value)
source = ColumnDataSource(data=data)
#print(data.head())

# Descriptive statistics
stats = round(data.describe().reset_index(), 2)
stats_source = ColumnDataSource(data=stats)
stat_columns = [TableColumn(field=col, title=col) for col in stats.columns]
data_table = DataTable(source=stats_source, columns=stat_columns, width = 450, height=350, index_position=None)

# Plots
corr_tools = 'pan, wheel_zoom, box_select, reset'
tools = 'pan, wheel_zoom, xbox_select, reset'

corr = figure(width=350, height=350, tools=corr_tools)
corr.scatter(ticker1.value+'_returns', ticker2.value+'_returns', size=2, source=source,
            selection_color='firebrick', alpha=0.6, nonselection_alpha=0.1, selection_alpha=0.4)

# show(corr)
ts1 = figure(width=800, height=250, tools=tools, x_axis_type='datetime', active_drag='xbox_select')
ts1.line('Date', ticker1.value, source=source)
ts1.scatter('Date', ticker1.value, size=1, source=source, color=None, selection_color='firebrick')

ts2 = figure(width=800, height=250, tools=tools, x_axis_type='datetime', active_drag='xbox_select')
ts2.x_range = ts1.x_range
ts2.line('Date', ticker2.value, source=source)
ts2.scatter('Date', ticker2.value, size=1, source=source, color=None, selection_color='firebrick')

# show(column(ts1, ts2))

# Callbacks
def ticker1_change(attrname, old, new):
    ticker2.options = nix(new, DEFAULT_TICKERS)
    update()

def ticker2_change(attrname, old, new):
    ticker1.options = nix(new, DEFAULT_TICKERS)
    update()

def update():
    t1, t2 = ticker1.value, ticker2.value
    df = get_data(t1, t2, start=date_picker_start.value, end=date_picker_end.value)
    source.data = df #print(round(df.describe().reset_index(), 2))
    stats = round(df.describe().reset_index(), 2)
    stat_columns = [TableColumn(field=col, title=col) for col in stats.columns]
    #data_table = DataTable(source=stats_source, columns=stat_columns, width = 450, height=350, index_position=None)
    
    stats_source.data = stats
    data_table.columns = stat_columns
    
    ts1.line('Date', ticker1.value, source=source)
    ts1.scatter('Date', ticker1.value, size=1, source=source, color=None, selection_color='firebrick')
    
    ts2.line('Date', ticker2.value, source=source)
    ts2.scatter('Date', ticker2.value, size=1, source=source, color=None, selection_color='firebrick')
    
    corr.scatter(ticker1.value+'_returns', ticker2.value+'_returns', size=2, source=source,
            selection_color='firebrick', alpha=0.6, nonselection_alpha=0.1, selection_alpha=0.4)
    
    corr.title.text = '%s returns vs. %s returns' % (t1, t2)
    ts1.title.text, ts2.title.text = t1, t2


# Attach callback to action tickers
ticker1.on_change('value', ticker1_change)
ticker2.on_change('value', ticker2_change)
# Attach callback to date pickers
date_picker_start.on_change('value', lambda attr, old, new: update())
date_picker_end.on_change('value', lambda attr, old, new: update())

# Layouts
widgets = column(row(ticker1, ticker2, sizing_mode='stretch_width'), data_table, sizing_mode='stretch_both')#column(ticker1, ticker2, data_table)
main_row = row(widgets, corr)
series = row(ts1, ts2)
#layout = column(main_row, series)

layout = layout(
    [
        [header_div],
        [date_picker_start, date_picker_end],
        [main_row],
        [series]
    ],
    sizing_mode='stretch_width'
)
#show(layout)

# Bokeh server
curdoc().add_root(layout)
curdoc().title = 'Stock Dashboard'
# Run: bokeh serve --show Bokeh_dashboard.py