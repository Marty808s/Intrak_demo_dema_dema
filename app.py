from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
from datetime import datetime
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

app = Flask(__name__)

# Nastavení tajného klíče
app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(24)

# Slovník pro ukládání studentů s rozšířenými informacemi
students = {
    1: {
        'id': 1,
        'jmeno': 'Jan',
        'prijmeni': 'Novák',
        'datum_narozeni': '2000-05-15',
        'patro': '3A',
        'matka': {'jmeno': 'Jana Nováková', 'telefon': '123456789', 'email': 'jana@example.com'},
        'otec': {'jmeno': 'Petr Novák', 'telefon': '987654321', 'email': 'petr@example.com'},
        'email': 'jan.novak@student.cz',
        'skola': 'Gymnázium Praha',
        'rocnik': 3,
        'obor': 'Všeobecné gymnázium'
    },
    2: {
        'id': 2,
        'jmeno': 'Eva',
        'prijmeni': 'Svobodová',
        'datum_narozeni': '2001-08-20',
        'patro': '5B',
        'matka': {'jmeno': 'Hana Svobodová', 'telefon': '111222333', 'email': 'hana@example.com'},
        'otec': {'jmeno': 'Jiří Svoboda', 'telefon': '444555666', 'email': 'jiri@example.com'},
        'email': 'eva.svobodova@student.cz',
        'skola': 'SPŠ elektrotechnická',
        'rocnik': 2,
        'obor': 'Elektrotechnika'
    },
    3: {
        'id': 3,
        'jmeno': 'Tomáš',
        'prijmeni': 'Dvořák',
        'datum_narozeni': '2002-03-10',
        'patro': '2C',
        'matka': {'jmeno': 'Martina Dvořáková', 'telefon': '777888999', 'email': 'martina@example.com'},
        'otec': {'jmeno': 'Karel Dvořák', 'telefon': '666555444', 'email': 'karel@example.com'},
        'email': 'tomas.dvorak@student.cz',
        'skola': 'Obchodní akademie',
        'rocnik': 1,
        'obor': 'Ekonomika a podnikání'
    },
    4: {
        'id': 4,
        'jmeno': 'Lucie',
        'prijmeni': 'Procházková',
        'datum_narozeni': '2000-11-05',
        'patro': '4A',
        'matka': {'jmeno': 'Petra Procházková', 'telefon': '333222111', 'email': 'petra@example.com'},
        'otec': {'jmeno': 'Michal Procházka', 'telefon': '999888777', 'email': 'michal@example.com'},
        'email': 'lucie.prochazkova@student.cz',
        'skola': 'Střední zdravotnická škola',
        'rocnik': 4,
        'obor': 'Zdravotnický asistent'
    },
    5: {
        'id': 5,
        'jmeno': 'Jakub',
        'prijmeni': 'Černý',
        'datum_narozeni': '2003-07-22',
        'patro': '1B',
        'matka': {'jmeno': 'Lenka Černá', 'telefon': '555444333', 'email': 'lenka@example.com'},
        'otec': {'jmeno': 'Pavel Černý', 'telefon': '222333444', 'email': 'pavel@example.com'},
        'email': 'jakub.cerny@student.cz',
        'skola': 'Střední průmyslová škola',
        'rocnik': 1,
        'obor': 'Strojírenství'
    }
}

# Aktualizace next_id
next_id = max(students.keys()) + 1

# Registrujte font DejaVuSans
# pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
# addMapping('DejaVuSans', 0, 0, 'DejaVuSans')

pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))
addMapping('Arial', 0, 0, 'Arial')
addMapping('Arial', 1, 0, 'Arial-Bold')

@app.route('/')
def index():
    return render_template('index.html', students=students.values())

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    global next_id
    if request.method == 'POST':
        new_student = {
            'id': next_id,
            'jmeno': request.form['jmeno'],
            'prijmeni': request.form['prijmeni'],
            'datum_narozeni': request.form['datum_narozeni'],
            'patro': request.form['patro'],
            'matka': {
                'jmeno': request.form['matka_jmeno'],
                'telefon': request.form['matka_telefon'],
                'email': request.form['matka_email']
            },
            'otec': {
                'jmeno': request.form['otec_jmeno'],
                'telefon': request.form['otec_telefon'],
                'email': request.form['otec_email']
            },
            'email': request.form['email'],
            'skola': request.form['skola'],
            'rocnik': int(request.form['rocnik']),
            'obor': request.form['obor']
        }
        students[next_id] = new_student
        next_id += 1
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/student/<int:id>')
def student_card(id):
    student = students.get(id)
    if student is None:
        return "Student not found", 404
    return render_template('student_card.html', student=student)

@app.route('/generate_pdf/<int:id>')
def generate_pdf(id):
    student = students.get(id)
    if student is None:
        return "Student not found", 404
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, 
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=1, fontName='Arial'))
    styles['Title'].fontName = 'Arial-Bold'
    styles['Heading2'].fontName = 'Arial-Bold'
    styles['Normal'].fontName = 'Arial'
    
    elements = []
    
    # Nadpis
    elements.append(Paragraph("Karta žáka internátu", styles['Title']))
    elements.append(Spacer(1, 0.5*cm))
    
    # Základní informace
    elements.append(Paragraph("Základní informace:", styles['Heading2']))
    elements.append(Spacer(1, 0.2*cm))
    
    data = [
        ["Jméno:", f"{student['jmeno']} {student['prijmeni']}"],
        ["Datum narození:", student['datum_narozeni']],
        ["Patro:", student['patro']],
        ["Email:", student['email']],
        ["Škola:", student['skola']],
        ["Ročník:", str(student['rocnik'])],
        ["Obor:", student['obor']]
    ]
    
    table = Table(data, colWidths=[4*cm, 10*cm])
    table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Arial'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('TEXTCOLOR', (0,0), (0,-1), colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    elements.append(table)
    
    elements.append(Spacer(1, 0.5*cm))
    
    # Kontakty rodičů
    elements.append(Paragraph("Kontakty rodičů:", styles['Heading2']))
    elements.append(Spacer(1, 0.2*cm))
    
    parent_data = [
        ["Matka:", student['matka']['jmeno']],
        ["Tel:", student['matka']['telefon']],
        ["Email:", student['matka']['email']],
        ["Otec:", student['otec']['jmeno']],
        ["Tel:", student['otec']['telefon']],
        ["Email:", student['otec']['email']]
    ]
    
    parent_table = Table(parent_data, colWidths=[4*cm, 10*cm])
    parent_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Arial'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('TEXTCOLOR', (0,0), (0,-1), colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    elements.append(parent_table)
    
    # Zápatí
    elements.append(Spacer(1, 5*cm))
    elements.append(Paragraph(f"Vytištěno dne: {datetime.now().strftime('%d.%m.%Y')}", styles['Center']))
    doc.build(elements)
    
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"{student['prijmeni']}_{student['jmeno']}_karta.pdf", mimetype='application/pdf')

@app.route('/edit_student/<int:id>', methods=['GET', 'POST', 'DELETE'])
def edit_student(id):
    student = students.get(id)
    if student is None:
        flash('Student nebyl nalezen.', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        if '_method' in request.form and request.form['_method'] == 'DELETE':
            # Odstranění studenta
            del students[id]
            flash('Student byl úspěšně odstraněn.', 'success')
            return redirect(url_for('index'))
        else:
            # Aktualizace studenta
            try:
                student.update({
                    'jmeno': request.form.get('jmeno', student['jmeno']),
                    'prijmeni': request.form.get('prijmeni', student['prijmeni']),
                    'datum_narozeni': request.form.get('datum_narozeni', student['datum_narozeni']),
                    'patro': request.form.get('patro', student['patro']),
                    'matka': {
                        'jmeno': request.form.get('matka_jmeno', student['matka']['jmeno']),
                        'telefon': request.form.get('matka_telefon', student['matka']['telefon']),
                        'email': request.form.get('matka_email', student['matka']['email'])
                    },
                    'otec': {
                        'jmeno': request.form.get('otec_jmeno', student['otec']['jmeno']),
                        'telefon': request.form.get('otec_telefon', student['otec']['telefon']),
                        'email': request.form.get('otec_email', student['otec']['email'])
                    },
                    'email': request.form.get('email', student['email']),
                    'skola': request.form.get('skola', student['skola']),
                    'rocnik': int(request.form.get('rocnik', student['rocnik'])),
                    'obor': request.form.get('obor', student['obor'])
                })
                flash('Údaje studenta byly úspěšně aktualizovány.', 'success')
            except KeyError as e:
                flash(f'Chyba při aktualizaci: Chybí pole {str(e)}', 'error')
            except ValueError as e:
                flash(f'Chyba při aktualizaci: Neplatná hodnota - {str(e)}', 'error')
            return redirect(url_for('student_card', id=id))
    
    return render_template('edit_student.html', student=student)

@app.route('/search', methods=['GET'])
def search_student():
    query = request.args.get('query', '').lower()
    if query:
        results = [
            student for student in students.values()
            if query in student['jmeno'].lower() or query in student['prijmeni'].lower()
        ]
    else:
        results = None
    
    return render_template('search_student.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
