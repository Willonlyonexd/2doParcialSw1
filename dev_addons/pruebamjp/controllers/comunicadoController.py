from odoo import http
from odoo.http import request
import json
import base64

class ComunicadoController(http.Controller):

    @http.route('/api/comunicados/general', auth='user', type='http', methods=['GET'], csrf=False)
    def get_comunicados_general(self, **kwargs):
        comunicados = request.env['pruebamjp.comunicado_usuario'].search([('usuario_recibe_id', 'in', request.env['res.users'].search([]).ids)])
        data = []
        for com in comunicados:
            comunicado = com.comunicado_id
            multimedia = {
                'imagen': base64.b64encode(comunicado.imagen).decode('utf-8') if comunicado.imagen else None,
                'imagen_mimetype': comunicado.imagen_mimetype,
                'video': base64.b64en                            comunicado.video).decode('utf-8') if comunicado.video else None,
                'video_mimetype': comunicado.video_mimetype,
                'audio': base64.b64encode(comunicado.audio).decode('utf-8') if comunicado.audio else None,
                'audio_mimetype': comunicado.audio_mimetype,
            }
            data.append({
                'nombre': comunicado.nombre,
                'descripcion': comunicado.description,
                'fecha': comunicado.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                'visto': com.visto,
                'multimedia': multimedia
            })
        
        return request.make_response(json.dumps(data), headers=[('Content-Type', 'application/json')])

    @http.route('/api/comunicados/visto/<int:comunicado_usuario_id>', auth='user', type='http', methods=['POST'], csrf=False)
    def marcar_como_visto(self, comunicado_usuario_id, **kwargs):
        comunicado_usuario = request.env['pruebamjp.comunicado_usuario'].browse(comunicado_usuario_id)
        if not comunicado_usuario.exists():
            return request.make_response(json.dumps({'error': 'Comunicado no encontrado'}), status=404)

        comunicado_usuario.write({'visto': True})
        return request.make_response(json.dumps({'success': 'Comunicado marcado como visto'}), headers=[('Content-Type', 'application/json')])
