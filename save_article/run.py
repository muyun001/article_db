# -*- coding: utf8 -*-
import os
import sys
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_PATH)
from save_article.save.save_articles import SaveArticle


if __name__ == '__main__':
    save_article = SaveArticle()
    save_article.save_article()
