# mdpy
### tools for working with python in markdown

## installation

    pip install mdpy

## usage

`mdpy` expects that python code blocks are demarcated like so:

    ```python
    # some python code
    ```

to compile the markdown file into an iPython notebook:

    # creates markdown_with_python.ipynb
    mdpy compile markdown_with_python.md

by default, this does not execute the code blocks. you can specify to do so with the `-x` or `--execute` flag:

    mdpy compile -x markdown_with_python.md

you can also execute the python code blocks and drop into `ipython`:

    mdpy run markdown_with_python.md

## example

an example markdown file:

    # This is a test notebook

    this is some test, $x = y$

    ```python
    import numpy as np
    a = np.array([1,2,3])
    print(a)
    ```

    this is a little interlude

    ```python
    import numpy as np
    a + np.array([5,6,7])
    ```

    ok!