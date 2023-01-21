from fastapi import APIRouter, status, Depends
from fastapi_cache.decorator import cache

import models
from routers.dependencies import get_reports_repository
from repositories import ReportRepository

router = APIRouter(prefix='/reports', tags=['Database'])


@router.get(path='/', status_code=status.HTTP_200_OK, response_model=list[models.Report])
@cache(expire=60)
async def get_all(
        limit: int = 100,
        skip: int = 0,
        report_type: str | None = None,
        chat_id: int | None = None,
        reports: ReportRepository = Depends(get_reports_repository),
):
    return await reports.get_all(skip, limit, report_type, chat_id)


@router.post(path='/')
async def add_unit_id(
        report_in: models.Report,
        reports: ReportRepository = Depends(get_reports_repository),
):
    return await reports.upsert_unit_id(report_in.report_type, report_in.chat_id, report_in.unit_ids)


@router.delete(path='/')
async def delete_unit_id(
        report_in: models.Report,
        reports: ReportRepository = Depends(get_reports_repository),
):
    return await reports.delete_unit_id(report_in.report_type, report_in.chat_id, report_in.unit_ids)


@router.get(
    path='/retranslate/{report_type}/',
    response_model=list[models.ReportChatIdAndUnitIds],
)
@cache(expire=60)
async def get_chats_to_retranslate(
        report_type: str,
        reports: ReportRepository = Depends(get_reports_repository),
):
    return await reports.get_chat_ids_and_unit_ids_by_report_type(report_type)
