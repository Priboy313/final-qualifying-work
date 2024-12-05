
import pandasflow as pdf
import pandas as pd

import matplotlib.pyplot as plt
import mplfinance as mpf
plt.style.use("dark_background")




def get_graph(data      :pd.DataFrame,
              
              ind_up    :str    = 'ind_up',
              ind_down  :str    = 'ind_down',

              col_up    :str    = 'green',
              col_down  :str    = 'red',
              col_mup   :str    = 'blue',
              col_mdn   :str    = 'blue',
              msize     :int    = 50,

              volume    :bool   = False) -> mpf.plot:

    add_plot = [
        mpf.make_addplot(data[ind_up],
                        type='scatter', color=col_mup,
                        marker='^', markersize=msize,
                        panel=0,
                        ),

        mpf.make_addplot(data[ind_down],
                        type='scatter', color=col_mdn,
                        marker='v', markersize=msize,
                        panel=0
                        )
    ]

    mc = mpf.make_marketcolors(
        up=col_up, down=col_down,
        edge='inherit',
        wick='black',
        volume='in',
        ohlc='i',
    )

    s = mpf.make_mpf_style(
        marketcolors=mc,
    )

    return mpf.plot(
                    data,
                    type='candle',
                    volume=volume,
                    figsize=(15, 6),
                    # title=my_title,
                    ylabel='Index Level',
                    xlabel='Time',
                    style=s,
                    addplot=add_plot
                )
