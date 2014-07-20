#!/usr/bin/python
import sys
from workflow import Workflow, web
from progress import ProgressBar

def download_file(url, path):
    """Download the contents of `url` to `path`.
    """
    r = web.get(url)
    total_length = r.raw.info().getparam('content-length')

    with open(path, 'wb') as f:
        if total_length is None: # no content length header
            f.write(r.content)
        else:
            dl = 0
            total_length = int(total_length)
            for chunk in r.iter_content(chunk_size=1024, decode_unicode=True):
                dl += len(chunk)
                percent = float(dl / total_length)
                if chunk:
                    f.write(chunk)
                    print 'Downloaded {0:.2f}%'.format(percent)
                    f.flush()
    return path



def main(wf):

    url = 'http://gen.lib.rus.ec/get?md5=A4DC00DEA85E05FE862A4F02357A843D'
    file_name = '/Users/smargheim/Downloads/knowledge_and_demonstration_aristotles_posterior_analytics.pdf'
    download_file(url, file_name)

    #cd_bar = ProgressBar(title="TEST", text='Downloading PDF...')
    #cd_bar.update(float(percent))
    #cd_bar.finish()
    


if __name__ == '__main__':
    WF = Workflow()
    sys.exit(WF.run(main))
