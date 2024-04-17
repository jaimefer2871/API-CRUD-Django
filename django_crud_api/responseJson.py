# Archivo para personalizar respuesta desde el servidor.
from rest_framework.renderers import JSONRenderer
from django.utils.translation import gettext as _


class CustomJSONRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None, **args):
        try:
            # Definimos que la respuesta del código sea mayor a 400 (errores de servidor) para asignar la variable de error a true o caso contrario false
            if renderer_context["response"].status_code >= 400:
                error = True
                mensaje = "Ha ocurrido un error. Por favor consulte al administrador"
                response_data = data
                data = []
                if renderer_context["response"].status_code == 401:
                    error_validation = {
                        "code": renderer_context["response"].status_code,
                        "field": _("Token"),
                        "message": _(str(response_data["detail"])),
                    }
                    data.append(error_validation)
                elif renderer_context["response"].status_code == 404:
                    error_validation = {
                        "code": renderer_context["response"].status_code,
                        "field": (
                            response_data["field"] if response_data != None else ""
                        ),
                        "message": _(str("Not_Found")),
                    }
                    data.append(error_validation)
                elif renderer_context["response"].status_code == 422:
                    error_validation = {
                        "code": renderer_context["response"].status_code,
                        # 'message': _(renderer_context['response'].data[0]['message'])
                        "message": _(str(response_data["message"])),
                    }
                    data.append(error_validation)
                elif renderer_context["response"].status_code == 500:
                    error_validation = {
                        "code": renderer_context["response"].status_code,
                        "message": _(renderer_context["response"].data["message"]),
                        "errors": str(
                            renderer_context["response"].data["errors"]["request"]
                        ),
                    }
                    data.append(error_validation)
                else:
                    for k in response_data:
                        error_validation = {
                            "code": renderer_context["response"].status_code,
                            "field": _(k),
                            "message": _(str(response_data[k][0])),
                            "file": __file__,
                        }
                        data.append(error_validation)
            else:
                error = False
                mensaje = "Operación realizada exitosamente"

            data = {
                "code": renderer_context["response"].status_code,
                "error": error,
                "message": mensaje,
                "data": data,
            }
        except Exception as e:
            data = {
                "code": 500,
                "error": True,
                "message": str(e),
                "data": data,
            }
        return super(CustomJSONRenderer, self).render(
            data, accepted_media_type, renderer_context
        )
