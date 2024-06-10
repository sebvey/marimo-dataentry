import marimo

__generated_with = "0.6.16"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    import polars as pl
    return pl, mo


@app.cell
def __(duckdb):
    print("Hello DataEntry")

if __name__ == "__main__":
    app.run()
