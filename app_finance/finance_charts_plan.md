# Plan to Modify financecharts.py

This plan outlines the steps to modify the `financecharts.py` file to fetch GC=F candle data, detect harmonic patterns using `pyharmonics`, and visualize the results.

**Objective:**

Modify `financecharts.py` to:
1. Fetch the last 50 candles of GC=F at a 5-minute interval from Yahoo Finance.
2. Use the `pyharmonics` library to detect and display all completed and forming harmonic patterns on this data.
3. Generate a chart visualizing the candles and the detected patterns.

**Steps:**

1.  **Import necessary libraries:** Import `YahooCandleData`, `Technicals`, `HarmonicSearch`, and `Plotter` from the `pyharmonics` library.
2.  **Fetch market data:**
    *   Create an instance of `YahooCandleData`.
    *   Use the `get_candles` method to fetch the last 50 candles for the symbol 'GC=F' at a 5-minute interval (`MIN_5`).
3.  **Create Technicals object:** Instantiate the `Technicals` class with the fetched candle data, symbol, and interval.
4.  **Search for harmonic patterns:**
    *   Create an instance of `HarmonicSearch` with the `Technicals` object.
    *   Call the `search()` method to find completed harmonic patterns.
    *   Call the `forming()` method to find forming harmonic patterns.
    *   Retrieve all detected patterns (completed and forming) using `get_patterns()`.
5.  **Visualize the results:**
    *   Create a `Plotter` object using the `Technicals` object, symbol, and interval.
    *   Add the detected harmonic patterns to the plotter using `add_harmonic_plots()`.
    *   Display the chart using the `show()` method.
6.  **Save the code:** Write the complete Python code to the `app_finance/finance_charts.py` file.

```mermaid
graph TD
    A[Start] --> B{Read pyharmonics docs.txt};
    B --> C{Understand pyharmonics usage};
    C --> D[Plan: Import libraries];
    D --> E[Plan: Fetch data (GC=F, 50 candles, 5m)];
    E --> F[Plan: Create Technicals object];
    F --> G[Plan: Search for patterns (completed & forming)];
    G --> H[Plan: Create Plotter object];
    H --> I[Plan: Add patterns to plotter];
    I --> J[Plan: Show plot];
    J --> K[Plan: Write code to financecharts.py];
    K --> L{Ask user for plan approval};
    L --> M[End];