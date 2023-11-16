def order_by(request, default: str = '-created_at'):
    return request.query_params.get('ordering', default)
