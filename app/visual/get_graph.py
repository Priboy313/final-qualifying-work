
import pandasflow as pdf
import pandas as pd

import matplotlib.pyplot as plt
import mplfinance as mpf
plt.style.use("dark_background")




def get_graph(data:pd.DataFrame) -> mpf.plot:

    add_plot = [
        mpf.make_addplot(data['ind_up'],
                        type='scatter', color='blue',
                        marker='^', markersize=50,
                        panel=0,
                        ),

        mpf.make_addplot(data['ind_down'],
                        type='scatter', color='blue',
                        marker='v', markersize=50,
                        panel=0
                        )
    ]

    mc = mpf.make_marketcolors(
        up='green', down='red',
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
                    volume=False,
                    figsize=(15, 6),
                    # title=my_title,
                    ylabel='Index Level',
                    xlabel='Time',
                    style=s,
                    addplot=add_plot
                )
