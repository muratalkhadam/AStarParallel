import nbformat


def reformat_jupyter(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)

    for cell in notebook.cells:
        if cell.cell_type == 'code' and 'execution_count' not in cell:
            cell['execution_count'] = None

    with open(f'fixed-{filepath}', 'w', encoding='utf-8') as f:
        nbformat.write(notebook, f)


# Replace 'your_notebook.ipynb' with the path to your notebook
reformat_jupyter('AStarTest.ipynb')
