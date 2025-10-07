from odoo import models, fields, api
from odoo.exceptions import ValidationError

class GraduacionPaciente(models.Model):
    _name = 'optica.graduacion'
    _description = 'Graduación de Paciente'
    _rec_name = 'paciente_id'
    _order = 'fecha desc, id desc'

    paciente_id = fields.Many2one(
        'res.partner',
        string='Paciente',
        required=True,
        domain=[('is_company', '=', False)],
        ondelete='restrict',
        index=True,
    )
    fecha = fields.Date(string='Fecha de evaluación', default=fields.Date.context_today)
    profesional = fields.Many2one('res.users', string='Optometrista', default=lambda self: self.env.user)

    # ✅ CAMBIADOS DE SELECTION A FLOAT/INTEGER
    ojo_derecho_esfera = fields.Float(string='OD Esfera', digits=(8, 2))
    ojo_derecho_cilindro = fields.Float(string='OD Cilindro', digits=(8, 2))
    ojo_derecho_eje = fields.Integer(string='OD Eje')  # Cambiado a Integer
    ojo_derecho_av = fields.Char(string='OD AV')

    ojo_izquierdo_esfera = fields.Float(string='OI Esfera', digits=(8, 2))
    ojo_izquierdo_cilindro = fields.Float(string='OI Cilindro', digits=(8, 2))
    ojo_izquierdo_eje = fields.Integer(string='OI Eje')  # Cambiado a Integer
    ojo_izquierdo_av = fields.Char(string='OI AV')

    # ✅ ESTOS YA ESTÁN BIEN COMO FLOAT
    adicion = fields.Float(string='Adición', digits=(8, 2))
    distancia_nasopupilar_od = fields.Float(string='Distancia Nasopupilar OD', digits=(8, 2))
    distancia_nasopupilar_oi = fields.Float(string='Distancia Nasopupilar OI', digits=(8, 2))
    distancia_interpupilar = fields.Float(string='Distancia Interpupilar', digits=(8, 2))
    altura_centro_optico = fields.Float(string='Altura CO', digits=(8, 2))
    
    # ✅ ESTOS SELECTION SÍ PUEDEN QUEDARSE (son opciones fijas)
    tipo_lente = fields.Selection([
        ('monofocal', 'Monofocal'),
        ('bifocal', 'Bifocal'),
        ('progresivo', 'Progresivo'),
    ], string='Tipo de Lente')

    diagnostico = fields.Selection([
        ('miopia', 'Miopía'),
        ('hipermetropia', 'Hipermetropía'),
        ('astigmatismo', 'Astigmatismo'),
        ('astigmatismo_miopico', 'Astigmatismo Miópico'),
        ('astigmatismo_hipermetropico', 'Astigmatismo Hipermetrópico'),
        ('astigmatismo_simple', 'Astigmatismo Simple'),
        ('presbicia', 'Presbicia'),
    ], string='Diagnóstico')

    observaciones = fields.Text(string='Observaciones')

    # ✅ ACTUALIZAR LA VALIDACIÓN PARA INTEGER
    @api.constrains('ojo_derecho_eje', 'ojo_izquierdo_eje')
    def _check_valores(self):
        for rec in self:
            if rec.ojo_derecho_eje and not (0 <= rec.ojo_derecho_eje <= 180):
                raise ValidationError('El eje del ojo derecho debe estar entre 0 y 180.')
            if rec.ojo_izquierdo_eje and not (0 <= rec.ojo_izquierdo_eje <= 180):
                raise ValidationError('El eje del ojo izquierdo debe estar entre 0 y 180.')

    def action_imprimir_historia_clinica(self):
        self.ensure_one()
        return self.env.ref('odoo_graduacion_paciente.action_report_graduacion_paciente').report_action(self)

    # ❌ ELIMINAR LOS MÉTODOS DE SELECTION (ya no se necesitan)
    # def _esfera_selection(self):
    #     return [(f"{x:.2f}", f"{x:.2f}") for x in [20.00 - i * 0.25 for i in range(161)]]
    #
    # def _cilindro_selection(self):
    #     return [(f"{x:.2f}", f"{x:.2f}") for x in [-0.25 - i * 0.25 for i in range(24)]]
    #
    # def _eje_selection(self):
    #     return [(str(x), str(x)) for x in range(0, 181, 5)]

class ResPartner(models.Model):
    _inherit = 'res.partner'
    graduacion_ids = fields.One2many('optica.graduacion', 'paciente_id', string='Graduaciones')
