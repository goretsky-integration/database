from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.exceptions import PermissionDeniedError
from reports.selectors import (
    get_report_routes_by_report_type_id_and_chat_id,
    get_report_routes_by_report_type_id_and_unit_id,
    get_report_type_by_id,
)
from reports.services import create_report_routes, delete_report_routes
from telegram.selectors import get_telegram_chat_with_scope_by_chat_id


class ReportRoutesUnitsListApi(APIView):

    def get(self, request: Request):
        chat_id = int(request.query_params['chat_id'])
        report_type_id = int(request.query_params['report_type_id'])
        limit = int(request.query_params.get('limit', 100))
        offset = int(request.query_params.get('offset', 0))

        report_routes = get_report_routes_by_report_type_id_and_chat_id(
            report_type_id=report_type_id,
            chat_id=chat_id,
            limit=limit,
            offset=offset,
        )
        is_next_page_exists = get_report_routes_by_report_type_id_and_chat_id(
            report_type_id=report_type_id,
            chat_id=chat_id,
            limit=1,
            offset=limit + offset,
        ).exists()

        response_data = {
            'unit_ids': report_routes.values_list('unit_id', flat=True),
            'is_end_of_list_reached': not is_next_page_exists,
        }
        return Response(response_data)


class ReportRoutesChatIdsListApi(APIView):

    def get(self, request: Request):
        unit_id = int(request.query_params['unit_id'])
        report_type_id = int(request.query_params['report_type_id'])
        limit = int(request.query_params.get('limit', 100))
        offset = int(request.query_params.get('offset', 0))

        report_routes = get_report_routes_by_report_type_id_and_unit_id(
            report_type_id=report_type_id,
            unit_id=unit_id,
            limit=limit,
            offset=offset,
        )
        is_next_page_exists = get_report_routes_by_report_type_id_and_unit_id(
            report_type_id=report_type_id,
            unit_id=unit_id,
            limit=1,
            offset=limit + offset,
        ).exists()

        chat_ids = report_routes.values_list(
            'telegram_chat__chat_id',
            flat=True,
        )

        response_data = {
            'chat_ids': chat_ids,
            'is_end_of_list_reached': not is_next_page_exists,
        }
        return Response(response_data)


class ReportRoutesCreateDeleteApi(APIView):

    class InputSerializer(serializers.Serializer):
        report_type_id = serializers.IntegerField()
        chat_id = serializers.IntegerField()
        unit_ids = serializers.ListSerializer(
            child=serializers.IntegerField(),
            allow_empty=False,
        )

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data
        chat_id = serialized_data['chat_id']
        report_type_id = serialized_data['report_type_id']
        requested_unit_ids: set[int] = set(serialized_data['unit_ids'])

        telegram_chat = get_telegram_chat_with_scope_by_chat_id(chat_id)
        if telegram_chat.role is None:
            raise PermissionDeniedError('User has no any role')

        report_type = get_report_type_by_id(report_type_id)

        report_types_with_access = telegram_chat.role.report_types
        units_with_access = telegram_chat.role.units

        has_report_type_access = report_types_with_access.contains(report_type)
        if not has_report_type_access:
            raise PermissionDeniedError('Permission to report type denied')

        unit_ids_with_access: set[int] = set(
            units_with_access.values_list('id', flat=True)
        )
        requested_unit_ids_with_access: set[int] = {
            unit_id for unit_id in requested_unit_ids
            if unit_id in unit_ids_with_access
        }
        permission_denied_units = requested_unit_ids - unit_ids_with_access

        if permission_denied_units:
            raise PermissionDeniedError(
                f'Permission to units {permission_denied_units} denied'
            )

        create_report_routes(
            telegram_chat_id=telegram_chat.id,
            report_type_id=report_type.id,
            unit_ids=requested_unit_ids_with_access,
        )
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request: Request):
        chat_id = request.query_params['chat_id']
        report_type_id = request.query_params['report_type_id']
        unit_ids = tuple(map(int, request.query_params.getlist('unit_ids')))

        delete_report_routes(
            chat_id=chat_id,
            report_type_id=report_type_id,
            unit_ids=unit_ids,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
