
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class comunicado(models.Model):
    _name = 'pruebamjp.comunicado'
    _description = 'Modelo o tabla comunicado'

    nombre = fields.Char(required=True)
    description = fields.Text(required=True)
    fecha = fields.Datetime(required=True)
 # Campos de contenido multimedia
    imagen = fields.Binary(string="Imagen")
    imagen_mimetype = fields.Char(string="Tipo de Imagen")  # mime type para imagen
    video = fields.Binary(string="Video")
    video_mimetype = fields.Char(string="Tipo de Video")  # mime type para video
    audio = fields.Binary(string="Audio")
    audio_mimetype = fields.Char(string="Tipo de Audio")  # mime type para audio





    comunicado_usuario_ids = fields.One2many('pruebamjp.comunicado_usuario', 'comunicado_id', string="Comunicados")
    curso_id = fields.Many2one('pruebamjp.curso', string="Curso")
    ciclo_id = fields.Many2one('pruebamjp.ciclo', string="Ciclo")  

    
    def create_comunicado_for_all_users(self):
        users = self.env['res.users'].search([])
        self._create_comunicado_usuarios(users)



    def _create_comunicado_usuarios(self, users):
        comunicado_usuario_model = self.env['pruebamjp.comunicado_usuario']
        for user in users:
            comunicado_usuario_model.create({
                'visto': 'no',
                'comunicado_id': self.id,
                'usuario_recibe_id': user.id,
            })

     
    def create_comunicado_for_tutors_of_course(self):
        if not self.curso_id:
            raise ValidationError("Por favor, seleccione un curso.")
        max_year = self.env['pruebamjp.gestion'].search([], order='year desc', limit=1).year
        inscripciones = self.env['pruebamjp.inscripcion'].search([
        ('curso', '=', self.curso_id.id),
        ('gestion_id.year', '=', max_year)
        ])
        estudiante_ids = inscripciones.mapped('estudiante.id')
        estudiante_tutores = self.env['pruebamjp.estudiante_tutor'].search([('estudiante', 'in', estudiante_ids)])
        tutor_ids = estudiante_tutores.mapped('tutor.id')
        usuarios = self.env['res.users'].search([('id', 'in', self.env['pruebamjp.tutor'].browse(tutor_ids).mapped('usuario_id.id'))])
        self._create_comunicado_usuarios(usuarios)

    def create_comunicado_for_ciclo(self):
        if not self.ciclo_id:
            raise ValidationError("Por favor, seleccione un ciclo (primaria o secundaria).")
        
        # Obtener el año más reciente de la gestión
        max_year = self.env['pruebamjp.gestion'].search([], order='year desc', limit=1).year
        
        # Buscar inscripciones que coincidan con el ciclo y el año seleccionados
        inscripciones = self.env['pruebamjp.inscripcion'].search([
            ('curso.ciclo_id', '=', self.ciclo_id.id),
            ('gestion_id.year', '=', max_year)
        ])
        
        # Obtener los IDs de los estudiantes en esas inscripciones
        estudiante_ids = inscripciones.mapped('estudiante.id')
        
        # Obtener los tutores de esos estudiantes
        estudiante_tutores = self.env['pruebamjp.estudiante_tutor'].search([('estudiante', 'in', estudiante_ids)])
        tutor_ids = estudiante_tutores.mapped('tutor.id')
        
        # Obtener los usuarios asociados a esos tutores
        usuarios = self.env['res.users'].search([
            ('id', 'in', self.env['pruebamjp.tutor'].browse(tutor_ids).mapped('usuario_id.id'))
        ])
        
        # Crear registros de comunicado para los usuarios filtrados
        self._create_comunicado_usuarios(usuarios)

    @api.model
    def create(self, vals):
        record = super(comunicado, self).create(vals)
        return record    
 

    @api.depends('nombre') 
    def _compute_display_name(self): 
         for rec in self: 
             rec.display_name = f"{rec.nombre}" 
 
       
