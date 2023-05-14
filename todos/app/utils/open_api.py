from fastapi_users.openapi import OpenAPIResponseType
from fastapi_users.router.common import ErrorModel


def get_open_api_response(examples_res_details: dict[str, str]) -> OpenAPIResponseType:
    examples = {}
    for example, res_detail in examples_res_details.items():
        examples[example] = {
            'summary': example,
            'value': {'detail': res_detail}
        }
    return {
        'model': ErrorModel,
        'content': {
            'application/json': {
                'examples': examples
            }
        }
    }


def get_open_api_unauthorized_access_response() -> OpenAPIResponseType:
    return get_open_api_response({'Unauthorized access': 'Unauthorized'})
