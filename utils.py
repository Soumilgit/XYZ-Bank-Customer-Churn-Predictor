import plotly.graph_objects as go
def create_gauge_chart(probability):
    # Determine color based on churn probability - darker versions
    if probability < 0.15:
        color = "#3e9c42"  # darker green
    elif probability < 0.3:
        color = "#1a5a1d"  # darker dark green
    elif probability < 0.45:
        color = "#c9a84d"  # darker gold
    elif probability < 0.6:
        color = "#7a641f"  # darker mustard
    elif probability < 0.8:
        color = "#9c4a54"  # darker rose
    else:
        color = "#6a2828"  # darker red

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=probability * 100,
            domain={
                "x": [0, 1],
                "y": [0, 1]
            },
            title={
                "text": "Churn Probability",
                "font": {
                    "size": 24,
                    "color": "white"
                }
            },
            number={
                "font": {
                    "size": 40,
                    "color": "white"
                }
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                    "tickcolor": "white",
                },
                "bar": {
                    "color": color
                },
                "bgcolor": "rgba(255,255,255,0.8)",
                "borderwidth": 2,
                "bordercolor": "white",
                "steps": [
                    {
                        "range": [0, 15],
                        "color": "rgba(62,156,66,0.7)" 
                    },
                    {
                        "range": [15, 30],
                        "color": "rgba(26,90,29,0.7)"
                    },
                    {
                        "range": [30, 45],
                        "color": "rgba(201,168,77,0.7)"
                    },
                    {
                        "range": [45, 60],
                        "color": "rgba(122,100,31,0.7)"
                    },
                    {
                        "range": [60, 80],
                        "color": "rgba(156,74,84,0.7)"
                    },
                    {
                        "range": [80, 100],
                        "color": "rgba(106,40,40,0.7)"
                    }
                ],
                "threshold": {
                    "line": {"color": "#34495e", "width": 4},
                    "thickness": 0.75,
                    "value": probability * 100
                }
            }
        )
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "white", "family": "Arial, sans-serif"},
        width=400,
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

def create_model_probability_chart(probabilities):
    colors = ["#3b82f6", "#6366f1", "#8b5cf6", "#a855f7", "#d946ef", "#ec4899", "#f97316", "#10b981"]
    
    # Create a list of models sorted by probability (optional)
    sorted_models = sorted(probabilities.keys(), key=lambda x: probabilities[x], reverse=True)
    
    fig = go.Figure(data=[
        go.Bar(
            y=list(probabilities.keys()),
            x=list(probabilities.values()),
            orientation='h',
            text=[f'{p:.1%}' for p in probabilities.values()],
            textposition='auto',
            textfont={"color": "white"},
            marker_color=colors[:len(probabilities)],  # Use as many colors as needed
            marker_line_color='rgba(255,255,255,0.3)',
            marker_line_width=1
        )
    ])

    fig.update_layout(
        title={
            'text': 'Churn Probability by Model',
            'font': {'color': 'white', 'size': 20}
        },
        yaxis={
            'title': 'Models',
            'color': 'white',
            'gridcolor': 'rgba(255,255,255,0.1)'
        },
        xaxis={
            'title': 'Probability',
            'tickformat': '.0%',
            'range': [0,1],
            'color': 'white',
            'gridcolor': 'rgba(255,255,255,0.1)'
        },
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "white", "family": "Arial, sans-serif"}
    )
    return fig

def create_percentile_bar_chart(percentiles):
    # Color gradient from blue to purple based on percentile
    colors = [
        f"hsl({220 + (value/100)*80}, 70%, 60%)" 
        for value in percentiles.values()
    ]
    
    fig = go.Figure(
        go.Bar(
            x=list(percentiles.keys()),
            y=list(percentiles.values()),
            text=[f"{v:.1f}%" for v in percentiles.values()],
            textposition="auto",
            marker_color=colors,
            textfont={"color": "white", "size": 12},
            opacity=0.85
        )
    )
    
    fig.update_layout(
        title={
            "text": "Customer Feature Percentiles",
            "font": {"color": "white", "size": 20}
        },
        xaxis={
            "title": "Features",
            "color": "white",
            "tickangle": -45
        },
        yaxis={
            "title": "Percentile",
            "range": [0, 100],
            "color": "white",
            "gridcolor": "rgba(255,255,255,0.1)"
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "white", "family": "Arial, sans-serif"},
        margin=dict(l=20, r=20, t=60, b=100)  # Extra bottom margin for rotated labels
    )
    return fig
