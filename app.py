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
    # ... existing students ...
    6: {
        'id': 6,
        'jmeno': 'Karolína',
        'prijmeni': 'Veselá',
        'datum_narozeni': '2002-09-18',
        'patro': 4,
        'pokoj': '4B',
        'matka': {'jmeno': 'Monika Veselá', 'telefon': '777111222', 'email': 'monika@example.com'},
        'otec': {'jmeno': 'Radek Veselý', 'telefon': '777333444', 'email': 'radek@example.com'},
        'email': 'karolina.vesela@student.cz',
        'skola': 'Gymnázium Praha',
        'rocnik': 3,
        'obor': 'Všeobecné gymnázium'
    },
    7: {
        'id': 7,
        'jmeno': 'Martin',
        'prijmeni': 'Kučera',
        'datum_narozeni': '2001-04-30',
        'patro': 2,
        'pokoj': '2A',
        'matka': {'jmeno': 'Jitka Kučerová', 'telefon': '608123456', 'email': 'jitka@example.com'},
        'otec': {'jmeno': 'Tomáš Kučera', 'telefon': '608654321', 'email': 'tomas@example.com'},
        'email': 'martin.kucera@student.cz',
        'skola': 'SPŠ elektrotechnická',
        'rocnik': 4,
        'obor': 'Informační technologie'
    },
    8: {
        'id': 8,
        'jmeno': 'Tereza',
        'prijmeni': 'Marková',
        'datum_narozeni': '2003-12-05',
        'patro': 3,
        'pokoj': '3C',
        'matka': {'jmeno': 'Alena Marková', 'telefon': '602111222', 'email': 'alena@example.com'},
        'otec': {'jmeno': 'Petr Marek', 'telefon': '602333444', 'email': 'petr.m@example.com'},
        'email': 'tereza.markova@student.cz',
        'skola': 'Obchodní akademie',
        'rocnik': 2,
        'obor': 'Ekonomika a podnikání'
    },
    9: {
        'id': 9,
        'jmeno': 'David',
        'prijmeni': 'Novotný',
        'datum_narozeni': '2000-08-12',
        'patro': 1,
        'pokoj': '1A',
        'matka': {'jmeno': 'Ivana Novotná', 'telefon': '773999888', 'email': 'ivana@example.com'},
        'otec': {'jmeno': 'Marek Novotný', 'telefon': '773888999', 'email': 'marek@example.com'},
        'email': 'david.novotny@student.cz',
        'skola': 'Střední průmyslová škola',
        'rocnik': 4,
        'obor': 'Strojírenství'
    },
    10: {
        'id': 10,
        'jmeno': 'Nikola',
        'prijmeni': 'Králová',
        'datum_narozeni': '2002-06-25',
        'patro': 5,
        'pokoj': '5A',
        'matka': {'jmeno': 'Zuzana Králová', 'telefon': '606777888', 'email': 'zuzana@example.com'},
        'otec': {'jmeno': 'Lukáš Král', 'telefon': '606888999', 'email': 'lukas@example.com'},
        'email': 'nikola.kralova@student.cz',
        'skola': 'Střední zdravotnická škola',
        'rocnik': 3,
        'obor': 'Praktická sestra'
    },
    11: {
        'id': 11,
        'jmeno': 'Filip',
        'prijmeni': 'Horák',
        'datum_narozeni': '2001-11-08',
        'patro': 2,
        'pokoj': '2B',
        'matka': {'jmeno': 'Markéta Horáková', 'telefon': '775123456', 'email': 'marketa@example.com'},
        'otec': {'jmeno': 'Ondřej Horák', 'telefon': '775654321', 'email': 'ondrej@example.com'},
        'email': 'filip.horak@student.cz',
        'skola': 'Gymnázium Praha',
        'rocnik': 4,
        'obor': 'Všeobecné gymnázium'
    },
    12: {
        'id': 12,
        'jmeno': 'Adéla',
        'prijmeni': 'Sedláčková',
        'datum_narozeni': '2003-02-14',
        'patro': 4,
        'pokoj': '4C',
        'matka': {'jmeno': 'Lucie Sedláčková', 'telefon': '604111222', 'email': 'lucie@example.com'},
        'otec': {'jmeno': 'Jan Sedláček', 'telefon': '604333444', 'email': 'jan.s@example.com'},
        'email': 'adela.sedlackova@student.cz',
        'skola': 'SPŠ elektrotechnická',
        'rocnik': 2,
        'obor': 'Elektrotechnika'
    },
    13: {
        'id': 13,
        'jmeno': 'Vojtěch',
        'prijmeni': 'Malý',
        'datum_narozeni': '2000-10-03',
        'patro': 3,
        'pokoj': '3B',
        'matka': {'jmeno': 'Kateřina Malá', 'telefon': '777555666', 'email': 'katerina@example.com'},
        'otec': {'jmeno': 'Martin Malý', 'telefon': '777666555', 'email': 'martin.m@example.com'},
        'email': 'vojtech.maly@student.cz',
        'skola': 'Střední průmyslová škola',
        'rocnik': 4,
        'obor': 'Informační technologie'
    },
    14: {
        'id': 14,
        'jmeno': 'Barbora',
        'prijmeni': 'Kolářová',
        'datum_narozeni': '2002-07-19',
        'patro': 5,
        'pokoj': '5C',
        'matka': {'jmeno': 'Simona Kolářová', 'telefon': '608987654', 'email': 'simona@example.com'},
        'otec': {'jmeno': 'Jakub Kolář', 'telefon': '608456789', 'email': 'jakub.k@example.com'},
        'email': 'barbora.kolarova@student.cz',
        'skola': 'Obchodní akademie',
        'rocnik': 3,
        'obor': 'Ekonomické lyceum'
    },
    15: {
        'id': 15,
        'jmeno': 'Matěj',
        'prijmeni': 'Pospíšil',
        'datum_narozeni': '2001-01-27',
        'patro': 1,
        'pokoj': '1C',
        'matka': {'jmeno': 'Veronika Pospíšilová', 'telefon': '773222111', 'email': 'veronika@example.com'},
        'otec': {'jmeno': 'David Pospíšil', 'telefon': '773111222', 'email': 'david.p@example.com'},
        'email': 'matej.pospisil@student.cz',
        'skola': 'Střední zdravotnická škola',
        'rocnik': 4,
        'obor': 'Zdravotnický asistent'
    },
    1: {
        'id': 1,
        'jmeno': 'Jan',
        'prijmeni': 'Novák',
        'datum_narozeni': '2000-05-15',
        'patro': 3,
        'pokoj': '3A',
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
        'patro': 5,
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
        'patro': 2,
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
        'patro': 4,
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
        'patro': 1,
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
    obor = request.args.get('obor', '').lower()
    skola = request.args.get('skola', '').lower()
    patro = request.args.get('patro', '')
    pokoj = request.args.get('pokoj', '').lower()

    # Debug: Print the type and content of students
    print(f"Type of students: {type(students)}")
    print(f"Content of students: {students}")

    # Ensure students is a dictionary
    if isinstance(students, dict):
        student_list = list(students.values())
    else:
        student_list = students  # Assuming it's already a list

    # Debug: Print a sample student
    if student_list:
        print(f"Sample student: {student_list[0]}")

    # Safely get the 'skola' field
    skoly = sorted(set(student.get('skola', '') for student in student_list if isinstance(student, dict)))

    results = student_list

    if query:
        results = [s for s in results if isinstance(s, dict) and (query in s.get('jmeno', '').lower() or query in s.get('prijmeni', '').lower())]
    if obor:
        results = [s for s in results if isinstance(s, dict) and obor in s.get('obor', '').lower()]
    if skola:
        results = [s for s in results if isinstance(s, dict) and skola in s.get('skola', '').lower()]
    if patro:
        results = [s for s in results if isinstance(s, dict) and str(s.get('patro', '')) == patro]
    if pokoj:
        results = [s for s in results if isinstance(s, dict) and pokoj in str(s.get('pokoj', '')).lower()]

    return render_template('search_student.html', results=results, skoly=skoly)

if __name__ == '__main__':
    app.run(debug=True)
