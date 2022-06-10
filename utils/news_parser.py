from abc import ABCMeta, abstractmethod

import xmltodict

from const.const import SourceTypeEnum
from schemas.news import RSSArticleSchema, HTTPQuerySchema


class NewsParserAbstract(metaclass=ABCMeta):
    """Абстрактный парсер новостного блока"""
    source_type = ''

    def __init__(self, news_models, http_query: HTTPQuerySchema):
        self._news_models = news_models
        self._raw_news = [xmltodict.parse(row[0].data) for row in self._news_models]
        self._http_query = http_query

    @abstractmethod
    def parse(self):
        raise NotImplementedError


class RSSParser(NewsParserAbstract):
    """Парсер RSS"""
    source_type = SourceTypeEnum.rss.value

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def parse(self):
        items = [n['rss']['channel']['item'] for n in self._raw_news]

        # Формирование уникального множества статей
        uniq_articles = set()
        for articles in items:
            for article in articles:
                uniq_articles.add(RSSArticleSchema(**article))

        # Сортировка статей по дате выхода от новых к старым
        sorted_articles = sorted(uniq_articles, key=lambda art: art.pub_date, reverse=True)
        converted_articles = [art.dict() for art in sorted_articles]

        # Пагинация
        from_slice = (self._http_query.page - 1) * self._http_query.page_size
        to_slice = from_slice + self._http_query.page_size
        sliced_articles = converted_articles[from_slice:to_slice]
        return sliced_articles


class ParserFabric:
    """Фабричный метод"""
    def __init__(self):
        pass

    def get_parser(self, source_type: str):
        """Выбрать нужный парсер"""
        parser_cls = None
        for parser_cls in NewsParserAbstract.__subclasses__():
            if parser_cls.source_type in source_type:
                break
        return parser_cls
