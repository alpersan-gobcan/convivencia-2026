import json

def get_color_map(data, filter_key):
    unique_keys = []
    for row in data:
        val = row.get(filter_key, "").lower()
        if val and val not in unique_keys:
            unique_keys.append(val)
    
    # Amplia paleta de colores pastel
    colors = [
        '#dcfce7', '#ccfbf1', '#e0e7ff', '#fce7f3', '#fef3c7', '#ffedd5', '#fee2e2', '#f3e8ff',
        '#e0f2fe', '#dbeafe', '#fae8ff', '#fef08a', '#bbf7d0', '#fecaca', '#fde68a', '#d9f99d',
        '#a7f3d0', '#bae6fd', '#c7d2fe', '#e9d5ff', '#fbcfe8', '#fecdd3', '#ccfbf1', '#ffedd5'
    ]
    return {k: colors[i % len(colors)] for i, k in enumerate(unique_keys)}

def create_html(title, description, headers, data, filters_html, filter_js, color_key="filter_1"):
    
    color_map = get_color_map(data, color_key)
    
    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        :root {{
            --primary: #0056b3;
            --text-dark: #1e293b;
            --white: #ffffff;
            --border: #cbd5e1;
            --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; }}
        body {{ background-color: #f8fafc; color: var(--text-dark); padding: 2rem; }}
        h1 {{ text-align: center; color: var(--primary); margin-bottom: 0.5rem; }}
        .subtitle {{ text-align: center; margin-bottom: 2rem; font-weight: 500; color: #475569; }}
        .filter-container {{ display: flex; justify-content: center; align-items: center; gap: 1rem; margin-bottom: 2rem; flex-wrap: wrap; background: var(--white); padding: 1.5rem; border-radius: 12px; box-shadow: var(--shadow); max-width: 1200px; margin-left: auto; margin-right: auto; }}
        .filter-group {{ display: flex; align-items: center; gap: 0.5rem; }}
        select, input {{ padding: 0.6rem; border-radius: 8px; border: 1px solid var(--border); font-size: 1rem; cursor: pointer; min-width: 150px; }}
        .table-container {{ max-width: 1200px; margin: 0 auto; background: var(--white); border-radius: 12px; box-shadow: var(--shadow); overflow-x: auto; margin-bottom: 2rem; }}
        table {{ width: 100%; border-collapse: collapse; min-width: 600px; }}
        th, td {{ padding: 1rem; text-align: left; border-bottom: 1px solid var(--border); vertical-align: top; }}
        th {{ background-color: var(--primary); color: var(--white); }}
        .btn-back {{ display: inline-block; margin-bottom: 1rem; padding: 0.5rem 1rem; background: var(--primary); color: white; text-decoration: none; border-radius: 8px; font-weight: 600; }}
        .btn-back:hover {{ background: #004494; }}
    </style>
</head>
<body>
    <div style="max-width: 1200px; margin: 0 auto;">
        <a href="index.html" class="btn-back">← Volver al inicio</a>
    </div>
    <h1>{title}</h1>
    <div class="subtitle">{description}</div>
    
    <div class="filter-container">
        {filters_html}
    </div>

    <div class="table-container">
        <table id="dataTable">
            <thead>
                <tr>
'''
    for h in headers:
        html += f'                    <th>{h}</th>\n'
    html += '''
                </tr>
            </thead>
            <tbody>
'''
    for row in data:
        bg_color = color_map.get(row.get(color_key, "").lower(), "#ffffff")
        html += f'                <tr style="background-color: {bg_color};" data-filter-1="{row.get("filter_1", "").lower()}" data-filter-2="{row.get("filter_2", "").lower()}" data-filter-3="{row.get("filter_3", "").lower()}">\n'
        for cell in row["cells"]:
            html += f'                    <td>{cell}</td>\n'
        html += '                </tr>\n'
        
    html += f'''
            </tbody>
        </table>
    </div>
'''

    if "docentes_acompanantes" in title.lower() or "centro" in title.lower():
        html += '''
    <div style="max-width: 1200px; margin: 2rem auto; background: var(--white); padding: 1.5rem; border-radius: 12px; box-shadow: var(--shadow); font-size: 0.95rem; line-height: 1.6;">
        <h3 style="color: var(--primary); margin-bottom: 1rem; font-size: 1.2rem;">📌 Información Interna (Profesorado de Guardia)</h3>
        
        <p><strong>PROFESORADO QUE SE QUEDA EN EL CENTRO DE GUARDIA:</strong><br>
        TECENERY, JOSÉ BÁEZ, SONIA, ANTONIO, NAIRA, JULIA, Mª PINO, BRUNO, ANA MEDINA, NIZAMAR, ROSARIO, MAITE, DAVID, MÓNICA S., FERNANDO.</p>
        
        <p style="margin-top: 1rem;"><strong>A LAS 10:40: SE BAJA A PISTA DE ATLETISMO A:</strong><br>
        S (SERGIO, NEREA, DESIREÉ, ELICIA, ELENA)<br>
        N (MONROY, MIGUEL ÁNGEL MORENO, JESÚS, MARIFÉ)<br>
        O (YAIZA, NOEMÍ V, ESTEFANÍA)</p>

        <p style="margin-top: 1rem;"><strong>A LAS 10:55 SE RECOGE EN PISTA DE ATLETISMO A:</strong><br>
        N (ALBERTO, SIXTO, MIGUEL ARTILES, MÓNICA DÍAZ)<br>
        O (RITA, ANTONIA, RUTH)</p>
        
        <p style="margin-top: 1rem;"><strong>A LAS 11:05 SE RECOGE EN PISTA DE ATLETISMO:</strong><br>
        N (JOSÉ MIGUEL)<br>
        O (PEDRO, ANA VÁLIDO, Mª ELENA)</p>
        
        <p style="margin-top: 1rem; color: #dc2626; font-weight: 600;">Nota: Cristian va en coche</p>
    </div>
'''

    html += f'''
    <script>
{filter_js}
    </script>
</body>
</html>
'''
    return html

# Lista maestra de docentes para el desplegable (ordenada alfabéticamente)
teachers_list = [
    'Alberto', 'Alejandro', 'Almudena', 'Ana Mata', 'Ana Medina', 'Ana Teresa', 'Ana Válido', 'Ángeles', 'Antonia', 'Antonio', 'Bosco', 'Bruno', 'Ciro', 'Coralia', 'Cristian', 'David', 'Desireé', 'Diego', 'Elena', 'Elicia', 'Elizabeth', 'Estefanía', 'Fernando', 'Irene', 'Jesús', 'José Báez', 'José Miguel', 'Julia', 'Lidia', 'Loly', 'Mª Elena', 'Mari Pino', 'Maite', 'Marifé', 'Miguel Ángel Moreno', 'Miguel Artiles', 'Migue', 'Mila', 'Mónica Díaz', 'Mónica S.', 'Monroy', 'Naira', 'Nerea', 'Nizamar', 'Noemi V.', 'Orlando H.', 'Orlando R.', 'Paula', 'Pedro', 'Rita', 'Rosalva', 'Rosario', 'Rosi', 'Ruth', 'Sergio', 'Silvia', 'Sixto', 'Sonia', 'Tecenery', 'Vicky', 'Yaiza'
]

teacher_options = '<option value="">Todos los docentes</option>\n'
for t in teachers_list:
    teacher_options += f'        <option value="{t.lower()}">{t}</option>\n'

# ----------------------------------------------------
# 1. GUARDIAS EN EL ESTADIO
# ----------------------------------------------------
estadio_headers = ["Franja horaria", "Zonas", "Docentes", "Observaciones"]
estadio_data = [
    {"filter_1": "9:00 a 10:15", "filter_2": "antonia alberto", "filter_3": "entrada", "cells": ["9:00 a 10:15 H", "Entrada y Salida del Estadio", "Antonia y Alberto", "-Controlar que no salga ningún alumnado del Estadio.<br>-No se permite que ningún tutor legal retire al alumnado del Estadio."]},
    {"filter_1": "9:00 a 10:15", "filter_2": "miguel artiles", "filter_3": "escalinatas", "cells": ["9:00 a 10:15 H", "Zona de Escalinatas", "Miguel Artiles", "-Esta zona no es transitable, el alumnado no puede pasar de esta zona."]},
    {"filter_1": "9:00 a 10:15", "filter_2": "mónica díaz", "filter_3": "área 1", "cells": ["9:00 a 10:15 H", "Área 1", "Mónica Díaz", "-Controlar que las actividades se estén llevando con normalidad...<br>-Controlar que las gradas esté todo en orden<br>-Si un docente-monitor necesita descansar..."]},
    {"filter_1": "9:00 a 10:15", "filter_2": "pedro", "filter_3": "área 2", "cells": ["9:00 a 10:15 H", "Área 2", "Pedro", ""]},
    {"filter_1": "9:00 a 10:15", "filter_2": "rita", "filter_3": "centro", "cells": ["9:00 a 10:15 H", "Zona Centro", "Rita", "- Zona entre áreas, baño y zumba. controlar su tránsito"]},
    {"filter_1": "9:00 a 10:15", "filter_2": "ruth", "filter_3": "baños", "cells": ["9:00 a 10:15 H", "Baños", "Ruth", "-Controlar el acceso al baño y revisar que no lo dejen en mal estado"]},

    {"filter_1": "10:15 a 11:00", "filter_2": "josé miguel", "filter_3": "entrada", "cells": ["10:15 a 11:00 H (Recreo)", "Entrada y Salida del Estadio", "José Miguel", "-Controlar que no salga ningún alumnado del Estadio.<br>-No se permite que ningún tutor legal retire al alumnado del Estadio."]},
    {"filter_1": "10:15 a 11:00", "filter_2": "mila", "filter_3": "escalinatas", "cells": ["10:15 a 11:00 H (Recreo)", "Zona de Escalinatas", "Mila", "-Esta zona no es transitable, el alumnado no puede pasar de esta zona."]},
    {"filter_1": "10:15 a 11:00", "filter_2": "mª elena", "filter_3": "área 1", "cells": ["10:15 a 11:00 H (Recreo)", "Área 1", "Mª Elena", "El alumnado debe de estar en las gradas para desayunar y luego a la zumba hasta el comienzo de las actividades."]},
    {"filter_1": "10:15 a 11:00", "filter_2": "orlando h.", "filter_3": "área 2", "cells": ["10:15 a 11:00 H (Recreo)", "Área 2", "Orlando H.", ""]},
    {"filter_1": "10:15 a 11:00", "filter_2": "irene", "filter_3": "centro", "cells": ["10:15 a 11:00 H (Recreo)", "Zona Centro", "Irene", "- Zona entre áreas, baño y zumba. controlar su tránsito"]},
    {"filter_1": "10:15 a 11:00", "filter_2": "pedro", "filter_3": "baños", "cells": ["10:15 a 11:00 H (Recreo)", "Baños", "Pedro", "-Controlar el acceso al baño y revisar que no lo dejen en mal estado"]},

    {"filter_1": "11:00 a 11:45", "filter_2": "miguel ángel moreno desireé", "filter_3": "entrada", "cells": ["11:00 a 11:45 H", "Entrada y Salida del Estadio", "Miguel Ángel Moreno y Desireé", "-Controlar que no salga ningún alumnado del Estadio.<br>-No se permite que ningún tutor legal retire al alumnado del Estadio."]},
    {"filter_1": "11:00 a 11:45", "filter_2": "jesús", "filter_3": "escalinatas", "cells": ["11:00 a 11:45 H", "Zona de Escalinatas", "Jesús", "-Esta zona no es transitable, el alumnado no puede pasar de esta zona."]},
    {"filter_1": "11:00 a 11:45", "filter_2": "mila", "filter_3": "área 1", "cells": ["11:00 a 11:45 H", "Área 1", "Mila", "-Controlar que las actividades se estén llevando con normalidad...<br>-Controlar que las gradas esté todo en orden<br>-Si un docente-monitor necesita descansar..."]},
    {"filter_1": "11:00 a 11:45", "filter_2": "yaiza", "filter_3": "área 2", "cells": ["11:00 a 11:45 H", "Área 2", "Yaiza", ""]},
    {"filter_1": "11:00 a 11:45", "filter_2": "noemi v.", "filter_3": "centro", "cells": ["11:00 a 11:45 H", "Zona Centro", "Noemi V.", "- Zona entre áreas, baño y zumba. controlar su tránsito"]},
    {"filter_1": "11:00 a 11:45", "filter_2": "nerea", "filter_3": "baños", "cells": ["11:00 a 11:45 H", "Baños", "Nerea", "-Controlar el acceso al baño y revisar que no lo dejen en mal estado"]},

    {"filter_1": "11:45 a 12:30", "filter_2": "orlando h. yaiza", "filter_3": "entrada", "cells": ["11:45 a 12:30 H", "Entrada y Salida del Estadio", "Orlando H. y Yaiza", "-Controlar que no salga ningún alumnado del Estadio.<br>-No se permite que ningún tutor legal retire al alumnado del Estadio."]},
    {"filter_1": "11:45 a 12:30", "filter_2": "jesús", "filter_3": "escalinatas", "cells": ["11:45 a 12:30 H", "Zona de Escalinatas", "Jesús", "-Esta zona no es transitable, el alumnado no puede pasar de esta zona."]},
    {"filter_1": "11:45 a 12:30", "filter_2": "miguel ángel moreno", "filter_3": "área 1", "cells": ["11:45 a 12:30 H", "Área 1", "Miguel Ángel Moreno", "-Controlar que las actividades se estén llevando con normalidad...<br>-Controlar que las gradas esté todo en orden<br>-Si un docente-monitor necesita descansar..."]},
    {"filter_1": "11:45 a 12:30", "filter_2": "noemi v.", "filter_3": "área 2", "cells": ["11:45 a 12:30 H", "Área 2", "Noemi V.", ""]},
    {"filter_1": "11:45 a 12:30", "filter_2": "mila", "filter_3": "centro", "cells": ["11:45 a 12:30 H", "Zona Centro", "Mila", "- Zona entre áreas, baño y zumba. controlar su tránsito"]},
    {"filter_1": "11:45 a 12:30", "filter_2": "desireé", "filter_3": "baños", "cells": ["11:45 a 12:30 H", "Baños", "Desireé", "-Controlar el acceso al baño y revisar que no lo dejen en mal estado"]},
]

estadio_filters_html = f'''
    <div class="filter-group">
        <label for="timeFilter" style="font-weight: bold;">Franja Horaria:</label>
        <select id="timeFilter" onchange="filterTable()">
            <option value="all">Todas las franjas</option>
            <option value="9:00 a 10:15">9:00 a 10:15 H</option>
            <option value="10:15 a 11:00">10:15 a 11:00 H</option>
            <option value="11:00 a 11:45">11:00 a 11:45 H</option>
            <option value="11:45 a 12:30">11:45 a 12:30 H</option>
        </select>
    </div>
    <div class="filter-group">
        <label for="docenteFilter" style="font-weight: bold;">Docente:</label>
        <select id="docenteFilter" onchange="filterTable()">
{teacher_options}
        </select>
    </div>
'''

estadio_filter_js = '''
    function filterTable() {
        const timeF = document.getElementById('timeFilter').value;
        const docF = document.getElementById('docenteFilter').value.toLowerCase();
        const rows = document.querySelectorAll('#dataTable tbody tr');
        rows.forEach(row => {
            const rowTime = row.getAttribute('data-filter-1');
            const rowDoc = row.getAttribute('data-filter-2');
            
            const matchTime = (timeF === 'all' || rowTime.includes(timeF));
            
            let matchDoc = false;
            if (docF === '') {
                matchDoc = true;
            } else {
                matchDoc = rowDoc.includes(docF);
            }
            
            if (matchTime && matchDoc) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }
'''

with open('guardias_estadio.html', 'w', encoding='utf-8') as f:
    f.write(create_html("Guardias en el Estadio", "Estadio Municipal de Vecindario - 09/10/2026", estadio_headers, estadio_data, estadio_filters_html, estadio_filter_js, color_key="filter_3"))

# ----------------------------------------------------
# 2. GUARDIAS EN EL CENTRO
# ----------------------------------------------------
centro_headers = ["Nivel", "1ª H", "2ª H", "3ª H", "Guardia Recreo", "4ª H", "5ª H", "6ª H"]
centro_data = [
    {"filter_1": "1º eso", "filter_2": "sonia mari pino rosario fernando david", "cells": ["1º ESO", "SONIA A 20", "SONIA A20", "MARI PINO A20", "ROSARIO BIBLIOTECA", "FERNANDO A20", "DAVID A20", "ROSARIO A20 O SALÓN ACTOS"]},
    {"filter_1": "2º eso", "filter_2": "rosario mari pino mónica s. julia fernando", "cells": ["2º ESO", "ROSARIO SALÓN ACTOS", "MARI PINO A21", "ROSARIO A21", "MÓNICA S. PASILLO Y JARDÍN INFERIOR", "JULIA A21", "JULIA A21", "FERNANDO A21"]},
    {"filter_1": "3º eso+1º pdc", "filter_2": "antonio sonia fernando antonia bruno naira", "cells": ["3º ESO+1º PDC", "ANTONIO A22", "ANTONIO A22", "SONIA A22 O SALÓN ACTOS", "", "FERNANDO A22", "ANTONIA A22", "BAJAN A JARDÍN CON BRUNO Y NAIRA"]},
    {"filter_1": "4º eso+2º pdc", "filter_2": "mari pino mónica s. david baño david ruth", "cells": ["4º ESO+2º PDC", "MARI PINO A23", "MÓNICA S. A23 O SALON ACTOS", "MÓNICA S. A23", "DAVID BAÑO EXT.", "DAVID A22", "RUTH A23", ""]},
    {"filter_1": "bachill", "filter_2": "josé báez antonio nizamar", "cells": ["BACHILL.", "JOSÉ BÁEZ A24", "JOSÉ BÁEZ A24", "ANTONIO A24", "", "NIZAMAR A24", "NIZAMAR A24 O SALÓN ACTOS", ""]},
    {"filter_1": "cfgb+cfgm", "filter_2": "tecenery ana medina naira bruno", "cells": ["CFGB+CFGM", "TECENERY A26", "ANA MEDINA A26", "NAIRA A26", "GUARDIA JARDÍN NAIRA", "NAIRA A26 O SALÓN A.", "BRUNO A26", ""]},
    {"filter_1": "mesa guardia", "filter_2": "ana medina tecenery elicia julia fernando david lidia mónica s ruth nizamar", "cells": ["MESA GUARDIA", "ANA MEDINA", "TECENERY ELICIA", "JULIA FERNANDO", "FERNANDO", "DAVID LIDIA", "MÓNICA S. RUTH", "NIZAMAR"]}
]

centro_filters_html = f'''
    <div class="filter-group">
        <label for="nivelFilter" style="font-weight: bold;">Nivel/Curso:</label>
        <select id="nivelFilter" onchange="filterTable()">
            <option value="all">Todos los niveles</option>
            <option value="1º eso">1º ESO</option>
            <option value="2º eso">2º ESO</option>
            <option value="3º eso">3º ESO + 1º PDC</option>
            <option value="4º eso">4º ESO + 2º PDC</option>
            <option value="bachill">Bachillerato</option>
            <option value="cfgb">Ciclos (CFGB+CFGM)</option>
            <option value="mesa">Mesa Guardia</option>
        </select>
    </div>
    <div class="filter-group">
        <label for="docenteFilter" style="font-weight: bold;">Docente:</label>
        <select id="docenteFilter" onchange="filterTable()">
{teacher_options}
        </select>
    </div>
'''

centro_filter_js = '''
    function filterTable() {
        const nivelF = document.getElementById('nivelFilter').value;
        const docF = document.getElementById('docenteFilter').value.toLowerCase();
        const rows = document.querySelectorAll('#dataTable tbody tr');
        rows.forEach(row => {
            const rowNivel = row.getAttribute('data-filter-1');
            const rowDoc = row.getAttribute('data-filter-2');
            
            const matchNivel = (nivelF === 'all' || rowNivel.includes(nivelF));
            
            let matchDoc = false;
            if (docF === '') {
                matchDoc = true;
            } else {
                matchDoc = rowDoc.includes(docF);
            }
            
            if (matchNivel && matchDoc) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }
'''

with open('guardias_centro.html', 'w', encoding='utf-8') as f:
    f.write(create_html("Guardias en el Centro", "Docentes que se quedan en el centro de guardia", centro_headers, centro_data, centro_filters_html, centro_filter_js, color_key="filter_1"))


# ----------------------------------------------------
# 3. DOCENTES QUE ACOMPAÑAN
# ----------------------------------------------------
acomp_headers = ["Grupo", "Responsables Salida (8:30 / 8:45)", "Responsables Regreso (13:00 / 13:10)"]
acomp_data = [
    # Grupo A
    {"filter_1": "1º eso a", "filter_2": "rosalva marifé ana teresa", "cells": ["1º ESO A", "ROSALVA", "MARIFÉ / ANA TERESA"]},
    {"filter_1": "1º eso b", "filter_2": "ana teresa ángeles", "cells": ["1º ESO B", "ANA TERESA", "ÁNGELES"]},
    {"filter_1": "1º eso c", "filter_2": "loli diego elena", "cells": ["1º ESO C", "Sust. Loli y Diego", "ELENA"]},
    {"filter_1": "1º eso d", "filter_2": "ciro", "cells": ["1º ESO D", "CIRO", "CIRO"]},
    
    {"filter_1": "3º eso a", "filter_2": "silvia elicia noemi v", "cells": ["3º ESO A", "SILVIA", "ELICIA / Noemi V."]},
    {"filter_1": "3º eso b", "filter_2": "sixto monroy", "cells": ["3º ESO B", "SIXTO", "MONROY"]},
    {"filter_1": "3º eso c", "filter_2": "rita silvia", "cells": ["3º ESO C", "RITA", "SILVIA"]},
    {"filter_1": "3º eso d", "filter_2": "coralia", "cells": ["3º ESO D", "CORALIA", "CORALIA"]},
    
    {"filter_1": "1º pdc", "filter_2": "alberto rosalva", "cells": ["1º PDC", "ALBERTO", "ROSALVA"]},
    {"filter_1": "1º cfgb", "filter_2": "migue orlando h.", "cells": ["1º CFGB", "MIGUE", "ORLANDO H."]},
    {"filter_1": "1º ele", "filter_2": "pedro yaiza", "cells": ["1º ELE", "PEDRO", "YAIZA"]},
    {"filter_1": "1º ite", "filter_2": "mónica díaz miguel ángel moreno", "cells": ["1º ITE", "MÓNICA DÍAZ", "MIGUEL ÁNGEL MORENO"]},
    
    {"filter_1": "1º bach a", "filter_2": "ruth paula", "cells": ["1º BACH A", "RUTH / PAULA", "PAULA"]},
    {"filter_1": "1º bach b", "filter_2": "antonia diego", "cells": ["1º BACH B", "ANTONIA", "DIEGO"]},
    {"filter_1": "1º bach c", "filter_2": "rosi", "cells": ["1º BACH C", "ROSI", "ROSI"]},

    # Grupo B
    {"filter_1": "2º eso a", "filter_2": "miguel artiles elizabeth", "cells": ["2º ESO A", "MIGUEL ARTILES", "Elizabeth"]},
    {"filter_1": "2º eso b", "filter_2": "elizabeth estefanía", "cells": ["2º ESO B", "ELIZABETH", "ESTEFANÍA"]},
    {"filter_1": "2º eso c", "filter_2": "bosco", "cells": ["2º ESO C", "BOSCO", "BOSCO"]},
    {"filter_1": "2º eso d", "filter_2": "ana válido loly nerea", "cells": ["2º ESO D", "ANA VÁLIDO", "SUT LOLY / NEREA"]},
    
    {"filter_1": "4º eso a", "filter_2": "almudena desireé", "cells": ["4º ESO A", "Almudena", "DESIREÉ"]},
    {"filter_1": "4º eso b", "filter_2": "almudena migue", "cells": ["4º ESO B", "Almudena", "Migue"]},
    {"filter_1": "4º eso c", "filter_2": "orlando r.", "cells": ["4º ESO C", "ORLANDO R.", "ORLANDO R."]},
    
    {"filter_1": "2º pdc", "filter_2": "mª elena sergio", "cells": ["2º PDC", "Mª ELENA", "SERGIO"]},
    {"filter_1": "2º cfgb", "filter_2": "orlando h mila", "cells": ["2º CFGB", "ORLANDO H", "Mila"]},
    {"filter_1": "2º iea", "filter_2": "mila", "cells": ["2º IEA", "Mila", "MILA"]},
    {"filter_1": "2º ite", "filter_2": "mila jesús", "cells": ["2º ITE", "MILA", "JESÚS"]},
    
    {"filter_1": "2º bach a", "filter_2": "josé miguel almudena", "cells": ["2º BACH A", "José Miguel", "ALMUDENA"]},
    {"filter_1": "2º bach b", "filter_2": "josé miguel ana mata", "cells": ["2º BACH B", "José Miguel", "ANA MATA"]},
    {"filter_1": "2º bach c", "filter_2": "vicky ana mata almudena", "cells": ["2º BACH C", "Vicky", "Ana Mata / Almudena"]}
]

acomp_filters_html = f'''
    <div class="filter-group">
        <label for="grupoFilter" style="font-weight: bold;">Grupo:</label>
        <select id="grupoFilter" onchange="filterTable()">
            <option value="all">Todos los grupos</option>
            <option value="1º eso">1º ESO</option>
            <option value="2º eso">2º ESO</option>
            <option value="3º eso">3º ESO</option>
            <option value="4º eso">4º ESO</option>
            <option value="bach">Bachillerato</option>
            <option value="pdc">PDC</option>
            <option value="cfgb">CFGB</option>
            <option value="ele">ELE</option>
            <option value="ite">ITE</option>
            <option value="iea">IEA</option>
        </select>
    </div>
    <div class="filter-group">
        <label for="docenteFilter" style="font-weight: bold;">Docente:</label>
        <select id="docenteFilter" onchange="filterTable()">
{teacher_options}
        </select>
    </div>
'''

acomp_filter_js = '''
    function filterTable() {
        const grupoF = document.getElementById('grupoFilter').value;
        const docF = document.getElementById('docenteFilter').value.toLowerCase();
        const rows = document.querySelectorAll('#dataTable tbody tr');
        rows.forEach(row => {
            const rowGrupo = row.getAttribute('data-filter-1');
            const rowDoc = row.getAttribute('data-filter-2');
            
            const matchGrupo = (grupoF === 'all' || rowGrupo.includes(grupoF));
            
            let matchDoc = false;
            if (docF === '') {
                matchDoc = true;
            } else {
                matchDoc = rowDoc.includes(docF);
            }
            
            if (matchGrupo && matchDoc) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }
'''

with open('docentes_acompanantes.html', 'w', encoding='utf-8') as f:
    f.write(create_html("Docentes que Acompañan", "Asignación de docentes para la salida y el regreso", acomp_headers, acomp_data, acomp_filters_html, acomp_filter_js, color_key="filter_1"))
