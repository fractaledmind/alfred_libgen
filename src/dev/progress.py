from workflow import bundler
import time
import os



def formatConsole(string):
    """Prepare for console."""
    bannedChars = ['!', '?', '$', '%', '#', 
                   '&', '*', ';', '(', ')',
                   '@', '`', '|', "'", '"',
                   '~', '<', '>', ' ']
    for i in bannedChars:
        if i in string:
            string = string.replace(i, r'\{}'.format(i))
    return string


class ProgressBar():
    """
    .. py:class ProgressBar()
    Used to manage a progress bar spawned from cocoadialog.
    """

    def __init__(self, title='', text='', percent='0'):
        """
        .. py:function __init__(self, title='', text='', percent='0')
        Initialize and spawn the progress bar.

        :param str title: Title of progress bar
        :param str text: Subtitle of progress bar
        :param str percent: Current percent present of progress bar
        """
        self.cd = bundler.utility('CocoaDialog')
        self.title = title
        self.text = text
        self.percent = percent
        cmd = '{} progressbar --title "{}" --text "{}" --percent "{}"'.format(
                    formatConsole(self.cd),
                    self.title,
                    self.text,
                    self.percent)
        self.pipe = os.popen(cmd, 'w')

    def update(self, percent, text=False):
        """
        .. py:function update(self, percent, text=False)
        Update the spawned progress bar object.

        :param str percent: New percent of progress bar
        :param bool text: No change text if false, 
        else edit to new string passed through text
        """
        if text:
            self.text = text
        self.pipe.write('%f %s\n' % (percent, self.text))
        self.pipe.flush()

    def finish(self):
        """Stop bar.
        """
        self.pipe.close()
        


def main():
    bar = ProgressBar(title="TEST", text='Updating YouTube-DL...')

    for n in range(100):
        bar.update(float(n))
        time.sleep(0.2)
    bar.finish()


if __name__ == "__main__":
    main()
