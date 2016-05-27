import os
import click
import subprocess
from nbformat import v4 as nbf
from nbformat import write
from nbconvert.preprocessors import ExecutePreprocessor


def extract_blocks(lines):
    """yields markdown and code blocks from markdown"""
    py_block = False
    block = []
    for line in lines:
        line = line.strip()

        # start of py block
        if line.strip() == '```python':
            py_block = True
            if block:
                yield block, 'md'
                block = []

        # exiting py block
        elif py_block and line == '```':
            py_block = False
            if block:
                yield block, 'py'
                block = []

        else:
            block.append(line)


def interact(blocks):
    """run the python and drop into ipython"""
    blocks = ['\n'.join(block) for block, type in blocks if type == 'py']
    script = '\n'.join(blocks)

    # save to temporary script
    fname = '/tmp/mdpy.py'
    with open(fname, 'w') as f:
        f.write(script)

    # run and drop into script with ipython
    subprocess.call(['ipython', '-i', fname])


def compile_nb(blocks, execute=False):
    """compile markdown to an ipynb"""
    nb = nbf.new_notebook()
    cells = []
    for block, type in blocks:
        block = '\n'.join(block)
        if type == 'md':
            cells.append(nbf.new_markdown_cell(block))
        elif type == 'py':
            cells.append(nbf.new_code_cell(block))

    # create a worksheet with the cells,
    # add it to the notebook
    nb['cells'] = cells

    if execute:
        # execute code blocks (in-place)
        ExecutePreprocessor().preprocess(nb, {})

    return nb


@click.group()
def cli():
    pass


@cli.command()
@click.argument('md_file', type=click.Path(exists=True))
@click.option('-x', '--execute', is_flag=True, help="execute code blocks")
def compile(md_file, execute):
    """compile a markdown file to an ipynb"""
    lines = open(md_file, 'r').readlines()
    blocks = extract_blocks(lines)
    nb = compile_nb(blocks, execute=execute)
    fname = os.path.basename(md_file)
    title = os.path.splitext(fname)[0]
    with open('{}.ipynb'.format(title), 'w') as f:
        write(nb, f)


@cli.command()
@click.argument('md_file', type=click.Path(exists=True))
def run(md_file):
    """execute python in markdown file and drop into ipython"""
    lines = open(md_file, 'r').readlines()
    blocks = extract_blocks(lines)
    interact(blocks)
