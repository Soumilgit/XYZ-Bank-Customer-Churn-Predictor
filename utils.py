import plotly.graph_objects as go

def create_gauge_chart(probability):
    # Color scheme based on churn probability
    if probability < 0.3:
        color = "#2ecc71"  # Green
        bg_colors = ["#92ef99", "#61de65", "#237626"]
    elif probability < 0.6:
        color = "#f39c12"  # Orange
        bg_colors = ["#fff8e1", "#dfc67b", "#a0842e"]
    else:
        color = "#e74c3c"  # Red
        bg_colors = ["#c88e97", "#bc6c74", "#8a3636"]

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=probability * 100,
            domain={"x": [0, 1], "y": [0, 1]},
            title={
                "text": "Churn Probability",
                "font": {"size": 24, "color": "white", "family": "Arial"}
            },
            number={
                "font": {"size": 40, "color": "white", "family": "Arial"},
                "suffix": "%"
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                    "tickcolor": "white",
                    "tickfont": {"color": "white", "size": 12}
                },
                "bar": {"color": color, "thickness": 0.3},
                "bgcolor": "rgba(255,255,255,0.8)",
                "borderwidth": 2,
                "bordercolor": "#bdc3c7",
                "steps": [
                    {"range": [0, 30], "color": bg_colors[0]},
                    {"range": [30, 60], "color": bg_colors[1]},
                    {"range": [60, 100], "color": bg_colors[2]}
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
    # Modern color gradient for models
    colors = ["#3b82f6", "#6366f1", "#8b5cf6", "#a855f7", "#d946ef"]
    
    fig = go.Figure(data=[
        go.Bar(
            y=list(probabilities.keys()),
            x=list(probabilities.values()),
            orientation='h',
            text=[f'{p:.1%}' for p in probabilities.values()],
            textposition='auto',
            textfont={"color": "white"},
            marker_color=colors[:len(probabilities)],
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