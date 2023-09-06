from odoo import api, fields, models , _
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class studentRegistration(models.Model):
    _name = 'student.registration'
    _description = 'Student Registration'

    name = fields.Char(string='Name',readonly=True)
    student_id = fields.Many2one(comodel_name='res.partner',string='Student',domain=[('is_student','=',True)],required=True,context="{'default_is_student':True}" )
    phone = fields.Char(string='Phone',related='student_id.phone',store=True)
    age = fields.Integer(string='Age')
    date = fields.Date(string='Date')
    currency_id = fields.Many2one(comodel_name='res.currency',string='Curreny',readonly=True,  default=lambda self:self.env.user.company_id.currency_id.id)
    amount = fields.Float('Registration fees',required=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirmed'),
                              ('invoiced', 'Invoiced'),
                              ('canceled', 'Canceled')], string='state',default='draft')
    is_invoiced = fields.Boolean('is_invoiced',default=False) 
    
    
    
    def confirm(self):
        self.state = 'confirm'
    
    def cancel(self):
        self.state = 'canceled'
    
    def create_invoice(self):
        entry = self.env['account.move']
        emn= entry.create({
            'move_type': 'entry',
            'state': 'draft',
            'partner_id': self.student_id.id,
            'date': self.date,
            'journal_id': 1,
            'registration_id': self.id,
            
        })
        self.is_invoiced = True
    
    def invoice_action(self):
        return {
            'name': _('New Entry'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'domain': [('registration_id', '=', self.id)]
        }
    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('rsr.sequence') or _('New')
            
        result = super(studentRegistration, self).create(vals)
        return result