import schemdraw
from schemdraw import flow
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np


def visualize_ops(signal):

    ops = signal.get_ops()    
    with schemdraw.Drawing() as d:        
        d.config(fontsize=8)
        op = ops[0]
        d += flow.Terminal().label(op.name + '\n' + str(op.parameters))
        d += flow.Arrow().length(d.unit/2)
        for op in ops[1:-1]:
            d += flow.Process().label(op.name + '\n' + str(op.parameters))
            d += flow.Arrow().length(d.unit/2)        
        op = ops[-1]
        d += flow.Terminal().label(op.name + '\n' + str(op.parameters))

def plot_signal(signal):
    a = signal.amplitude
    fig = make_subplots(rows=1, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.01)

    if len(a.shape) > 1:
        fig.add_trace(go.Heatmap(
                        z=a))
    else:
        fig.add_trace(go.Scatter(x=np.arange(a.shape[0]), y=a,mode='lines',))

    fig.update_layout(height=600, width=1600,
                    title_text="Acoustic plots")
    fig.show()