import plotly.graph_objects as go
import streamlit as st


def _hex_to_rgba(hex_color, alpha):
    hex_color = hex_color.lstrip("#")
    rgb = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {alpha})"


class Plotly:
    @staticmethod
    # def time_series(df, legend, st_wrapper, line_color="rgb(0,180,250)"):
    def time_series(df, ylabel, color, st_wrapper):
        x, min_val, max_val, avg_val = df["datetime"], df["min"], df["max"], df["avg"]
        x_axis, y_axis = "datetime", ylabel
        fill_color = _hex_to_rgba(color, 0.2)
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=x,
                y=avg_val,
                showlegend=False,
                line_color=color,
                name="avgVal",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=x,
                y=max_val,
                line_color="rgba(255,255,255,0)",
                name="maxVal",
                showlegend=False,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=x,
                y=min_val,
                fill="tonexty",
                fillcolor=fill_color,
                line_color="rgba(255,255,255,0)",
                name="minVal",
                showlegend=False,
            )
        )

        fig.update_traces(mode="lines")
        fig.update_layout(
            xaxis_title=x_axis,
            yaxis_title=y_axis,
            margin=dict(l=20, r=20, t=20, b=20),
        )
        if st_wrapper:
            return st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        else:
            return fig
