"""
Utilidad para envío de emails.
"""
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
import logging

logger = logging.getLogger('notifications')


def send_email(to, subject, body, from_email=None, html_body=None):
    """
    Envía un email.
    
    Args:
        to: Lista de destinatarios
        subject: Asunto del email
        body: Cuerpo del email (texto plano)
        from_email: Remitente (opcional, usa DEFAULT_FROM_EMAIL si no se especifica)
        html_body: Cuerpo en HTML (opcional)
    
    Returns:
        bool: True si se envió correctamente, False en caso contrario
    """
    try:
        from_email = from_email or settings.DEFAULT_FROM_EMAIL
        
        if html_body:
            # Enviar email con versión HTML
            msg = EmailMessage(
                subject=subject,
                body=body,
                from_email=from_email,
                to=to
            )
            msg.content_subtype = "html"
            msg.send()
        else:
            # Enviar email de texto plano
            send_mail(
                subject=subject,
                message=body,
                from_email=from_email,
                recipient_list=to,
                fail_silently=False
            )
        
        logger.info(f"Email sent successfully to {to}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending email to {to}: {str(e)}")
        return False


def send_template_email(to, subject, template_name, context, from_email=None):
    """
    Envía un email usando una plantilla Django.
    
    Args:
        to: Lista de destinatarios
        subject: Asunto del email
        template_name: Nombre de la plantilla
        context: Contexto para la plantilla
        from_email: Remitente (opcional)
    
    Returns:
        bool: True si se envió correctamente, False en caso contrario
    """
    from django.template.loader import render_to_string
    
    try:
        html_content = render_to_string(template_name, context)
        text_content = render_to_string(
            template_name.replace('.html', '.txt'), 
            context
        ) if template_name.endswith('.html') else html_content
        
        return send_email(
            to=to,
            subject=subject,
            body=text_content,
            html_body=html_content,
            from_email=from_email
        )
        
    except Exception as e:
        logger.error(f"Error sending template email: {str(e)}")
        return False


def format_contact_email(name, email, message):
    """
    Formatea un mensaje de contacto para envío por email.
    
    Args:
        name: Nombre del remitente
        email: Email del remitente
        message: Mensaje
    
    Returns:
        tuple: (subject, body)
    """
    subject = f"[Contacto] Mensaje de {name}"
    
    body = f"""
    ╔══════════════════════════════════════════════════════════╗
    ║          NUEVO MENSAJE DE CONTACTO RECIBIDO             ║
    ╚══════════════════════════════════════════════════════════╝
    
    De: {name}
    Email: {email}
    
    ──────────────────────────────────────────────────────────
    MENSAJE:
    ──────────────────────────────────────────────────────────
    
    {message}
    
    ──────────────────────────────────────────────────────────
    
    Este mensaje fue enviado desde el Email Service.
    Para responder, usa la dirección: {email}
    """
    
    return subject, body
