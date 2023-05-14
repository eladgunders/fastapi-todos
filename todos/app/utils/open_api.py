from fastapi_users.openapi import OpenAPIResponseType
from fastapi_users.router.common import ErrorModel


def get_open_api_response(*, example: str, res_detail: str) -> OpenAPIResponseType:
    return {
        'model': ErrorModel,
        'content': {
            'application/json': {
                'examples': {
                    f'{example}': {
                        'summary': f'{example}',
                        'value': {'detail': f'{res_detail}'}
                    }
                }
            }
        }
    }


def get_open_api_unauthorized_access_response() -> OpenAPIResponseType:
    return get_open_api_response(
        example='Unauthorized access',
        res_detail='Unauthorized'
    )
