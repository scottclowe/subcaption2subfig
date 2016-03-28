# subcaption2subfig

Converts TeX subfigures written for the [subcaption package][subcaption] into
subfigures formatted correctly for the [subfig package][subfig], using the
subfloat command.

While subcaption is the newer of the two packages, and should generally be
preferred over subfig, you may occassionally encounter a scenario when your
combination LaTeX packages is incompatible. This utility enables you to
downgrade subcaption-compatible code to subfig-compatible code if necessary
to resolve such situations.


## Usage

To use the tool, simply run
```shell
python subcaption2subfig.py INPUTFILE OUTPUTFILE
```
and the new file, `OUTPUTFILE`, is the processed version of `INPUTFILE`, with
subfigure environments replaced with subfloats.


## Requirements

Either Python 2.6+ or Python 3. No other dependencies.


## Example

*sample.tex*
```tex
This LaTeX shows an example figure.
\begin{figure}[htbp]
    \begin{subfigure}[b]{0.5\linewidth}
        \centering
        \caption{Caption for Figure 1.}
        \label{fig:first-file}
        \includegraphics[width=\linewidth]{file.png}
    \end{subfigure}
    \\
    \begin{subfigure}[b]{0.5\pagewidth}
        \centering
        \caption{Caption for Figure 2.}
        \label{fig:second-file}
        \includegraphics[width=0.8\linewidth]{file2.png}
    \end{subfigure}
    \caption{Caption for the whole figure.}
    \label{fig:myfigure}
\end{figure}
```

*Command*
```shell
python subcaption2subfig.py sample.tex output.tex
```

*output.tex*
```tex
This LaTeX shows an example figure.
\begin{figure}[htbp]
    \subfloat[][Caption for Figure 1.\label{fig:first-file}]{
        \centering
        \includegraphics[width=0.5\linewidth]{file.png}
    }
    \\
    \subfloat[][Caption for Figure 2.\label{fig:second-file}]{
        \centering
        \includegraphics[width=0.4\pagewidth]{file2.png}
    }
    \caption{Caption for the whole figure.}
    \label{fig:myfigure}
\end{figure}
```


## Features

- Finds subfigure environments and turns them into subfloats.
- Moves captions and labels into the appropriate argument to `subfloat`.
- Updates any `width=` values, for instance as used by includegraphics, which
  were relative to the size of the subfigure box so their widths will still be
  sized correctly.
- Preserves indentation of all lines of the subfigure, including start and end
  of the subfigure environment.
- Changes made to the file can be shown at the command line with the verbose
  `-v` flag.
- If verbosity is increased further (using `-vv`) the entire file contents are
  shown with the changes as shown with level-1 verbosity included inplace.


## Notes

This code was optimized for my needs, and works correctly for what I intended
it to do (and accordingly it passes all the unit tests). But this may not be
exactly what you need.

For instance, the code is configured to always generate a subfloat which will
show a letter for the subfigure regardless of whether there is caption text,
and to never add subfigures to the list of figures (LOF). This behaviour could
be changed so other subfloat arguments are output, but this was all I needed
so those options do not exist.


  [subcaption]: https://www.ctan.org/pkg/subcaption
  [subfig]: https://www.ctan.org/pkg/subfig
