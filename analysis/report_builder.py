def build_html_report(insights, strategy, report_text):

    html_content = f"""
    <html>
    <head>
        <title>F1 Race Report</title>
        <style>
            body {{ font-family: Arial; padding: 20px; }}
            h1 {{ color: #d90429; }}
            .section {{ margin-bottom: 30px; }}
            img {{ width: 500px; border-radius: 10px; }}
        </style>
    </head>

    <body>

    <h1>🏁 F1 Race Report</h1>

    <div class="section">
        <h2>📊 Insights</h2>
        <ul>
            <li>Avg Lap Time: {insights['avg_lap_time']}</li>
            <li>Max Degradation: {insights['max_degradation']}</li>
            <li>Trend: {insights['trend']}</li>
            <li>Critical Lap: {insights['critical_lap']}</li>
        </ul>
    </div>

    <div class="section">
        <h2>🏁 Strategy</h2>
        <p>Action: {strategy['action']}</p>
        <p>Confidence: {round(strategy['confidence']*100)}%</p>
        <p>{strategy['reasoning']}</p>
    </div>

    <div class="section">
        <h2>📈 Visual Analysis</h2>
        <img src="lap_time.png"><br><br>
        <img src="degradation.png">
    </div>

    <div class="section">
        <h2>📝 AI Report</h2>
        <p>{report_text}</p>
    </div>

    </body>
    </html>
    """

    with open("analysis/report.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("\n✅ HTML Report Generated: analysis/report.html")