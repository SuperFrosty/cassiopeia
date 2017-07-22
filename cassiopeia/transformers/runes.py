from typing import Type, TypeVar
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.runepage import RunePageData, RunePagesData, RunePage, RunePages

from ..dto.runepage import RunePageDto, RunePagesDto

T = TypeVar("T")
F = TypeVar("F")


class RunesTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    # Data

    @transform.register(RunePageDto, RunePageData)
    def rune_page_dto_to_data(self, value: RunePageDto, context: PipelineContext = None) -> RunePageData:
        data = deepcopy(value)
        return RunePageData(data)

    @transform.register(RunePagesDto, RunePagesData)
    def rune_pages_dto_to_data(self, value: RunePagesDto, context: PipelineContext = None) -> RunePagesData:
        data = deepcopy(value)
        for page in data["pages"]:
            page["region"] = data["region"]
            page["summonerId"] = data["summonerId"]
        data = [self.rune_page_dto_to_data(page) for page in data["pages"]]
        return RunePagesData(data)

    # Core

    @transform.register(RunePageData, RunePage)
    def rune_page_data_to_core(self, value: RunePageData, context: PipelineContext = None) -> RunePage:
        data = deepcopy(value)
        return RunePage(data)

    @transform.register(RunePagesData, RunePages)
    def rune_pages_data_to_core(self, value: RunePagesData, context: PipelineContext = None) -> RunePages:
        return RunePages([self.rune_page_data_to_core(page) for page in value])
