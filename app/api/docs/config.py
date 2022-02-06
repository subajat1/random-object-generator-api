template = {
    "swagger": "2.0",
    "info": {
        "title": "Random-object Generator API",
        "description": "API docs for Random-object Generator",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "bayumunajat",
            "email": "bayumunajat@gmail.com",
            "url": "https://github.com/subajat1",
        },
        "termsOfService": "",
        "version": "0.1.1"
    },
    "basePath": "",
    "schemes": [
        "http"
    ],
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}
