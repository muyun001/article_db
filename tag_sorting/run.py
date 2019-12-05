# coding: utf-8
import os
import sys
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_PATH)
from tag_sorting.tag_sort.tag_sort import TagSort
import threading


def start_tag_sort():
    """
    开始对文章进行tag分拣
    """
    tag_sort.tag_sort_article()


if __name__ == '__main__':
    tag_sort = TagSort()
    thread = threading.Thread(target=start_tag_sort)
    thread.start()
