# -*- coding: utf8 -*-
import os
import sys
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_PATH)
from pseudo_article.pseudo.pseudo_articles import PseudoArticle


if __name__ == '__main__':
    pseudo_article = PseudoArticle()
    pseudo_article.pseudo_article()
