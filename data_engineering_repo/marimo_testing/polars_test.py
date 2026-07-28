import marimo

__generated_with = "0.19.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    # Create your Polars dataframe
    df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    # CORRECT: Use mo.ui.table
    table = mo.ui.table(df)

    # Render the table in the cell output
    table
    return


if __name__ == "__main__":
    app.run()
