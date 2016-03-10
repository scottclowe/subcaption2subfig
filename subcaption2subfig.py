#!/usr/bin/python

import re
import argparse


# Search parameters
ENV_NAME = 'subfigure'
ENV_START_RE = '\\\\begin{\s*' + ENV_NAME + '\s*}'
ENV_END_RE = '\\\\end{\s*' + ENV_NAME + '\s*}'

COMMENT_RE = '(^|[^\\\])%'

LOF_CAPTION_AUTO = 'auto'
LOF_CAPTION_MIRROR = 'mirror'
LOF_CAPTION_NONE = 'none'
lof_caption = LOF_CAPTION_AUTO


def input_handler():
    parser = argparse.ArgumentParser(
        description='Transform subcaption subfigure floats into subfigure '
                    'subfloats')
    parser.add_argument(
        'source',
        help='name of source file.',
    )
    parser.add_argument(
        'destination',
        help='filename for output destination.',
    )
    parser.add_argument(
        '-v', '--verbose', action='count',
        help='increase verbosity',
    )
    args = parser.parse_args()
    return args


def handle_block(content, verbose=0):

    if verbose:
        print('>>>>>')
        print(content)
        print('-----')

    # Remove position argument
    content = re.sub('^\[[^\]]*\]', '', content)
    # Remove width argument
    result = re.match('^\{([^\}]*)\}', content)
    if result:
        box_width = result.groups()[0]
        content = content[result.end():]
    else:
        box_width = ''

    # Find all the labels
    prog = re.compile('\\\\label\{[^\}]*\}')
    labels = prog.findall(content)
    content = prog.sub('', content)

    # Find all the captions
    caption = ''
    prog = re.compile('\\\\caption\{([^\}]*)\}')
    result = prog.search(content)
    while result:
        caption += result.groups()[0]
        content = content[:result.start()] + content[result.end():]
        result = prog.search(content)

    # Remove any completely blank lines
    content = re.sub('\n\s+\n', '\n', content)

    # Fix widths, if relative width given
    result = re.search('\[width=([\d\.]*)\\\linewidth\]', content)
    if result:
        result2 = re.match('[\d\.]+', box_width)
        if result2:
            box_width_frac = float(result2.group())
            box_width_measure = box_width[result2.end():]
        else:
            box_width_frac = 1
            box_width_measure = box_width

        if result.groups()[0]:
            box_width_frac *= float(result.groups()[0])

        replacement_width = box_width_measure
        if box_width_frac is not 1:
            replacement_width = str(box_width_frac) + replacement_width
        replacement_width = '[width=' + replacement_width + ']'

        content = content[:result.start()] + replacement_width +\
                  content[result.end():]

    # Work out what arguments to give to subfloat, for caption and
    # labels to work correctly
    subcaption = caption + ''.join(labels)
    pre = '\subfloat'
    if lof_caption == LOF_CAPTION_AUTO:
        pre += '[][' + subcaption + ']'
    else:
        raise NotImplementedError()
    post = ''
    content = pre + '{' + content + post + '}'

    if verbose:
        print('-----')
        print(content)
        print('<<<<<')

    return content


def main(source, destination, verbose=0):
    # Setup loop parameters
    buffer_text = ''
    is_in_subfigure = False

    with open(source, 'r') as f_in:
        with open(destination, 'w') as f_out:
            for line_num, line in enumerate(f_in):
                if verbose > 1:
                    print('{:>4}:'.format(line_num), line, end='')
                while True:
                    comment_status = re.search(COMMENT_RE, line)
                    if is_in_subfigure:
                        result = re.search(ENV_END_RE, line)
                        if result and \
                                (not comment_status or
                                result.start() < comment_status.start()):
                            buffer_text += line[:result.start()]
                            f_out.write(handle_block(buffer_text, verbose))
                            is_in_subfigure = False
                            buffer_text = ''
                            line = line[result.end():]
                            continue
                        else:
                            buffer_text += line
                            break

                    else:
                        result = re.search(ENV_START_RE, line)
                        if result and \
                                (not comment_status or
                                result.start() < comment_status.start()):
                            f_out.write(line[:result.start()])
                            is_in_subfigure = True
                            line = line[result.end():]
                            continue
                        else:
                            f_out.write(line)
                            break

            if is_in_subfigure:
                f_out.write(handle_block(buffer_text, verbose))
                raise EnvironmentError(
                    'Final subfigure environment was not terminated.'
                    )


if __name__ == '__main__':
    args = input_handler()
    main(**vars(args))
