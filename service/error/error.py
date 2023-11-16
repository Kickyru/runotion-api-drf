from rest_framework import status as st
from rest_framework.response import Response


class ErrorHelper:
    BAD_REQUEST = st.HTTP_400_BAD_REQUEST
    NOT_FOUND = st.HTTP_404_NOT_FOUND
    NOT_CONTENT = st.HTTP_204_NO_CONTENT
    FORBIDDEN = st.HTTP_403_FORBIDDEN

    @staticmethod
    def get_error(error: str, status: int):
        return Response(
            {'error': error},
            status=status,
        )

    @staticmethod
    def forbidden():
        return ErrorHelper.get_error(error="У вас нет доступа", status=ErrorHelper.FORBIDDEN)

    @staticmethod
    def is_not_content_form(data=None):
        message = "Переданы не все аргументы"
        if data is not None:
            message = f"{message} ({', '.join(data)})"
        return ErrorHelper.get_error(error=message, status=ErrorHelper.NOT_CONTENT)
