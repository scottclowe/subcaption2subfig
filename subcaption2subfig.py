#!/usr/bin/python

import re


DEBUG = True

input_file = 'rw_tst/foo.tex'
output_file = 'rw_tst/foo_out.tex'

# Search parameters
ENV_NAME = 'subfigure'
ENV_START_RE = '\\\\begin{\s*' + ENV_NAME + '\s*}'
ENV_END_RE = '\\\\end{\s*' + ENV_NAME + '\s*}'

LOF_CAPTION_AUTO = 'auto'
LOF_CAPTION_MIRROR = 'mirror'
LOF_CAPTION_NONE = 'none'
lof_caption = LOF_CAPTION_AUTO


def handle_block(content):

    if DEBUG:
        print('---')
        print(content)
        print('---')

    # Remove position argument
    content = re.sub('^\[[^\]]*\]', '', content)
    # Remove width argument
    result = re.match('^\{([^\}]*)\}', content)
    if result:
        width = result.groups()[0]
        content = content[result.end():]
    else:
        width = ''

    # Find and remove all the labels
    prog = re.compile('\\\\label\{[^\}]*\}')
    labels = prog.findall(content)
    content = prog.sub('', content)

    caption = ''
    prog = re.compile('^(.*)\\\\caption\{([^\}]*)\}(.*)$')
    result = prog.match(content)
    print(result)
    while result:
        caption += result.groups()[1]
        content = result.groups()[0] + result.groups()[2]
        result = prog.match(content)

    subcaption = caption + ''.join(labels)
    pre = '\subfloat'
    if lof_caption == LOF_CAPTION_AUTO:
        pre += '[][' + subcaption + ']'
    else:
        raise NotImplementedError()
    post = ''
    return pre + '{' + content + post + '}'


def main():
    # Setup loop parameters
    buffer_text = ''
    is_in_subfigure = False

    with open(input_file, 'r') as f_in:
        with open(output_file, 'w') as f_out:
            for line_num, line in enumerate(f_in):
                #print(line_num)
                #print(line)
                while True:
                    comment_status = re.search(COMMENT_RE, line)
                    if is_in_subfigure:
                        result = re.search(ENV_END_RE, line)
                        if result:
                            buffer_text += line[:result.start()]
                            f_out.write(handle_block(buffer_text))
                            is_in_subfigure = False
                            buffer_text = ''
                            line = line[result.end():]
                            continue
                        else:
                            buffer_text += line
                            break

                    else:
                        result = re.search(ENV_START_RE, line)
                        if result:
                            f_out.write(line[:result.start()])
                            is_in_subfigure = True
                            line = line[result.end():]
                            continue
                        else:
                            f_out.write(line)
                            break

if __name__ == '__main__':
    main()
