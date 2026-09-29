import json
import io

def create_html(title, area, groups, data, color_map):
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
        select {{ padding: 0.6rem; border-radius: 8px; border: 1px solid var(--border); font-size: 1rem; cursor: pointer; min-width: 150px; }}
        .table-container {{ max-width: 1200px; margin: 0 auto; background: var(--white); border-radius: 12px; box-shadow: var(--shadow); overflow-x: auto; }}
        table {{ width: 100%; border-collapse: collapse; min-width: 800px; }}
        th, td {{ padding: 1rem; text-align: left; border-bottom: 1px solid var(--border); vertical-align: top; }}
        th {{ background-color: var(--primary); color: var(--white); }}
        .btn-back {{ display: inline-block; margin-bottom: 1rem; padding: 0.5rem 1rem; background: var(--primary); color: white; text-decoration: none; border-radius: 8px; font-weight: 600; }}
        .btn-back:hover {{ background: #004494; }}
        .recreo-row {{ background-color: #fed7aa !important; font-weight: bold; text-align: center; }}
        .zumba-row {{ background-color: #fbcfe8 !important; font-weight: bold; text-align: center; }}
'''
    for group, color in color_map.items():
        html += f'        [data-group="{group}"] {{ background-color: {color}; }}\n'
    html += f'''
    </style>
</head>
<body>
    <div style="max-width: 1200px; margin: 0 auto;">
        <a href="index.html" class="btn-back">← Volver al inicio</a>
    </div>
    <h1>{title}</h1>
    <div class="subtitle">{area}</div>
    
    <div class="filter-container">
        <div class="filter-group">
            <label for="courseFilter" style="font-weight: bold;">Curso/Grupo:</label>
            <select id="courseFilter" onchange="filterTable()">
                <option value="all">Todos los grupos</option>
'''
    for g in groups:
        html += f'                <option value="{g.lower()}">{g}</option>\n'
        
    html += '''
            </select>
        </div>
        <div class="filter-group">
            <label for="timeFilter" style="font-weight: bold;">Franja Horaria:</label>
            <select id="timeFilter" onchange="filterTable()">
                <option value="all">Todas las franjas</option>
                <option value="9:30 - 10:15 h">9:30 - 10:15 h</option>
                <option value="11:00 - 11:40 h">11:00 - 11:40 h</option>
                <option value="11:45 - 12:30 h">11:45 - 12:30 h</option>
            </select>
        </div>
    </div>

    <div class="table-container">
        <table id="scheduleTable">
            <thead>
                <tr>
                    <th>Franja horaria</th>
                    <th>Grupo</th>
                    <th>Taller / Actividad</th>
                    <th>Monitor</th>
                    <th>Docente ayudante</th>
                    <th>Observaciones</th>
                </tr>
            </thead>
            <tbody>
'''
    for row in data:
        if row.get('type') == 'recreo':
            html += f'                <tr class="recreo-row" data-group="all" data-time="10:15 - 10:45 h"><td colspan="6">10:15 - 10:45 h - RECREO</td></tr>\n'
        elif row.get('type') == 'zumba':
            html += f'                <tr class="zumba-row" data-group="all" data-time="10:30 - 11:00 h" style="border-bottom: 2px solid var(--primary);"><td colspan="6">10:30 - 11:00 h - ZUMBA</td></tr>\n'
        else:
            style = ' style="border-bottom: 2px solid #64748b;"' if row.get('end_block') else ''
            html += f'                <tr data-group="{row["group"]}" data-time="{row["time"]}"{style}>\n'
            html += f'                    <td>{row["time"]}</td>\n'
            html += f'                    <td><strong>{row["group_display"]}</strong></td>\n'
            html += f'                    <td>{row["activity"]}</td>\n'
            html += f'                    <td>{row.get("monitor", "")}</td>\n'
            html += f'                    <td>{row.get("ayudante", "")}</td>\n'
            html += f'                    <td><small>{row.get("obs", "")}</small></td>\n'
            html += f'                </tr>\n'
            
    html += '''
            </tbody>
        </table>
    </div>

    <script>
        function filterTable() {
            const courseFilter = document.getElementById('courseFilter').value.toLowerCase();
            const timeFilter = document.getElementById('timeFilter').value;
            const rows = document.querySelectorAll('#scheduleTable tbody tr');
            
            rows.forEach(row => {
                const group = row.getAttribute('data-group').toLowerCase();
                const time = row.getAttribute('data-time');
                
                let matchCourse = false;
                if (courseFilter === 'all' || group === 'all') {
                    matchCourse = true;
                } else if (group.includes(courseFilter)) {
                    matchCourse = true;
                } else if (courseFilter.includes('todos') || group.includes('todos')) {
                    const filterNivel = courseFilter.split(' ')[0];
                    if (group.includes(filterNivel) && courseFilter.includes('todos')) {
                        matchCourse = true;
                    } else if (group.includes('todos') && courseFilter.includes(group.split(' ')[0])) {
                        matchCourse = true;
                    }
                }
                
                let matchTime = false;
                if (timeFilter === 'all') {
                    matchTime = true;
                } else if (time === timeFilter) {
                    matchTime = true;
                } else if (group === 'all' && courseFilter === 'all') {
                    matchTime = false;
                }
                
                if (matchCourse && matchTime) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        }
    </script>
</body>
</html>
'''
    return html

color_map_1 = {
    '1ºA ESO': '#dcfce7', '1ºB ESO': '#ccfbf1', '1ºC ESO': '#e0e7ff', '1ºD ESO': '#fce7f3', '1º ESO (Todos)': '#f1f5f9',
    '2ºA ESO Aula Enclave': '#fef3c7', '2ºB ESO': '#ffedd5', '2ºC ESO': '#fee2e2', '2ºD ESO': '#f3e8ff', '2º ESO Aula Enclave (Todos)': '#f1f5f9',
    '3ºA ESO': '#e0f2fe', '3ºB ESO': '#dbeafe', '3ºC ESO': '#fae8ff', '3ºD ESO': '#fef08a', '3ºE ESO': '#bbf7d0', '3º ESO (Todos)': '#f1f5f9'
}

groups_1 = ['1ºA ESO', '1ºB ESO', '1ºC ESO', '1ºD ESO', '1º ESO (Todos)', '2ºA ESO + Aula Enclave', '2ºB ESO', '2ºC ESO', '2ºD ESO', '2º ESO + Aula Enclave (Todos)', '3ºA ESO', '3ºB ESO', '3ºC ESO', '3ºD ESO', '3ºE ESO', '3º ESO (Todos)']

obs_general = '-El monitor controla que esté el grupo que pertenece. Y junto al docente ayudante dinamizamos la actividad. <br><br> -El docente ayudante se coordina con el monitor para hacer turnos de descanso.'

area1_data = [
    {'time': '9:30 - 10:15 h', 'group': '1ºA ESO', 'group_display': '1ºA ESO', 'activity': 'Salto de comba (9:30-9:50) <br><br> El pañuelito (9:50-10:15)', 'monitor': 'Migue (EF) <br><br> CIRO', 'ayudante': '<br><br> ÁNGELES', 'obs': obs_general},
    {'time': '9:30 - 10:15 h', 'group': '1ºB ESO', 'group_display': '1ºB ESO', 'activity': 'Lanzamiento (9:30-9:50) <br><br> Brile (9:50-10:15)', 'monitor': 'UAVA <br><br> Coralia', 'ayudante': 'BOSCO <br><br>', 'end_block': True},
    {'time': '9:30 - 10:15 h', 'group': '1ºC ESO', 'group_display': '1ºC ESO', 'activity': 'Carrera de saco (9:30-9:50) <br><br> Salto Longitud (9:50-10:15)', 'monitor': 'Elena <br><br> UAVA', 'ayudante': '<br><br> CRISTIAN'},
    {'time': '9:30 - 10:15 h', 'group': '1ºD ESO', 'group_display': '1ºD ESO', 'activity': 'Juego de palabras (9:30-9:50) <br><br> Salto de comba (9:50-10:15)', 'monitor': 'SILVIA <br><br> Migue (EF)', 'ayudante': 'ROSALVA <br><br>', 'end_block': True},

    {'time': '9:30 - 10:15 h', 'group': '2ºA ESO Aula Enclave', 'group_display': '2ºA ESO + Aula Enclave', 'activity': 'El pañuelito (9:30-9:50) <br><br> Salto de comba (9:50-10:15)', 'monitor': 'CIRO <br><br> Migue (EF)', 'ayudante': 'ÁNGELES / Samira <br><br> Raúl', 'obs': obs_general},
    {'time': '9:30 - 10:15 h', 'group': '2ºB ESO', 'group_display': '2ºB ESO', 'activity': 'Brile (9:30-9:50) <br><br> Lanzamiento (9:50-10:15)', 'monitor': 'Coralia <br><br> UAVA', 'ayudante': '<br><br> BOSCO', 'end_block': True},
    {'time': '9:30 - 10:15 h', 'group': '2ºC ESO', 'group_display': '2ºC ESO', 'activity': 'Salto Longitud (9:30-9:50) <br><br> Carrera de saco (9:50-10:15)', 'monitor': 'UAVA <br><br> Elena', 'ayudante': 'CRISTIAN <br><br>'},
    {'time': '9:30 - 10:15 h', 'group': '2ºD ESO', 'group_display': '2ºD ESO', 'activity': 'Salto de comba (9:30-9:50) <br><br> Juego de palabras (9:50-10:15)', 'monitor': 'Migue (EF) <br><br> SILVIA', 'ayudante': '<br><br> ROSALVA', 'end_block': True},

    {'time': '9:30 - 10:15 h', 'group': '3º ESO (Todos)', 'group_display': '3º ESO (Todos)', 'activity': 'Hinchables acuáticos', 'monitor': 'DAMASI', 'ayudante': 'SIXTO Y MARIA ELENA', 'obs': 'Ayudar al monitor de DAMASI y mojarte', 'end_block': True},

    {'type': 'recreo'},
    {'type': 'zumba'},

    {'time': '11:00 - 11:40 h', 'group': '1ºA ESO', 'group_display': '1ºA ESO', 'activity': 'Lanzamiento (11:00-11:20) <br><br> Brile (11:20-11:40)', 'monitor': 'UAVA <br><br> Coralia', 'ayudante': 'BOSCO <br><br>', 'obs': obs_general},
    {'time': '11:00 - 11:40 h', 'group': '1ºB ESO', 'group_display': '1ºB ESO', 'activity': 'Carrera de Saco (11:00-11:20) <br><br> Salto Longitud (11:20-11:40)', 'monitor': 'Elena <br><br> UAVA', 'ayudante': '<br><br> CRISTIAN', 'end_block': True},
    {'time': '11:00 - 11:40 h', 'group': '1ºC ESO', 'group_display': '1ºC ESO', 'activity': 'Juego de palabras (11:00-11:20) <br><br> Salto de comba (11:20-11:40)', 'monitor': 'SILVIA <br><br> Migue (EF)', 'ayudante': 'ROSALVA <br><br>'},
    {'time': '11:00 - 11:40 h', 'group': '1ºD ESO', 'group_display': '1ºD ESO', 'activity': 'Pañuelito (11:00-11:20) <br><br> Lanzamiento (11:20-11:40)', 'monitor': 'CIRO <br><br> UAVA', 'ayudante': 'ÁNGELES <br><br>', 'end_block': True},

    {'time': '11:00 - 11:40 h', 'group': '2º ESO Aula Enclave (Todos)', 'group_display': '2º ESO + Aula Enclave (Todos)', 'activity': 'Hinchables Acuáticos', 'monitor': 'Damasi/ Raúl, Samira, Monroy', 'ayudante': 'ESTEFANÍA ELIZABETH', 'obs': 'Ayudar al monitor de DAMASI y mojarte', 'end_block': True},

    {'time': '11:00 - 11:40 h', 'group': '3ºA ESO', 'group_display': '3ºA ESO', 'activity': 'Salto de comba (11:00-11:20) <br><br> El pañuelito (11:20-11:40)', 'monitor': 'Migue (EF) <br><br> CIRO', 'ayudante': '<br><br> ÁNGELES', 'obs': obs_general},
    {'time': '11:00 - 11:40 h', 'group': '3ºB ESO', 'group_display': '3ºB ESO', 'activity': 'Brile (11:00-11:20) <br><br> Lanzamiento (11:20-11:40)', 'monitor': 'Coralia <br><br> UAVA', 'ayudante': '<br><br> BOSCO', 'end_block': True},
    {'time': '11:00 - 11:40 h', 'group': '3ºC ESO', 'group_display': '3ºC ESO', 'activity': 'Carrera de saco (11:00-11:20) <br><br> Salto Longitud (11:20-11:40)', 'monitor': 'Elena <br><br> UAVA', 'ayudante': '<br><br> CRISTIAN'},
    {'time': '11:00 - 11:40 h', 'group': '3ºD ESO', 'group_display': '3ºD ESO', 'activity': 'Salto de comba (11:00-11:20) <br><br> Juego de palabras (11:20-11:40)', 'monitor': 'Migue (EF) <br><br> SILVIA', 'ayudante': '<br><br> ROSALVA', 'end_block': True},
    {'time': '11:00 - 11:40 h', 'group': '3ºE ESO', 'group_display': '3ºE ESO', 'activity': 'Lanzamiento (11:00-11:20) <br><br> El pañuelito (11:20-11:40)', 'monitor': 'UAVA <br><br> CIRO', 'ayudante': 'BOSCO <br><br> ÁNGELES', 'end_block': True},

    {'time': '11:45 - 12:30 h', 'group': '1º ESO (Todos)', 'group_display': '1º ESO (Todos)', 'activity': 'Hinchables Acuáticos', 'monitor': 'Damasi/ MARIFÉ Elicia', 'ayudante': 'ANA TERESA', 'obs': 'Ayudar al monitor de DAMASI y mojarte', 'end_block': True},

    {'time': '11:45 - 12:30 h', 'group': '2ºA ESO Aula Enclave', 'group_display': '2ºA ESO + Aula Enclave', 'activity': 'Lanzamiento (11:45-12:05) <br><br> Braile (12:05-12:30)', 'monitor': 'UAVA <br><br> Coralia', 'ayudante': 'Raúl + BOSCO <br><br>', 'obs': obs_general},
    {'time': '11:45 - 12:30 h', 'group': '2ºB ESO', 'group_display': '2ºB ESO', 'activity': 'Carrera de Saco (11:45-12:05) <br><br> Salto Longitud (12:05-12:30)', 'monitor': 'Elena <br><br> UAVA', 'ayudante': '<br><br> CRISTIAN', 'end_block': True},
    {'time': '11:45 - 12:30 h', 'group': '2ºC ESO', 'group_display': '2ºC ESO', 'activity': 'Juego de palabras (11:45-12:05) <br><br> Salto Comba (12:05-12:30)', 'monitor': 'SILVIA <br><br> Migue (EF)', 'ayudante': 'ROSALVA <br><br>'},
    {'time': '11:45 - 12:30 h', 'group': '2ºD ESO', 'group_display': '2ºD ESO', 'activity': 'El pañuelito (11:45-12:05) <br><br> Lanzamiento (12:05-12:30)', 'monitor': 'CIRO <br><br> UAVA', 'ayudante': 'ÁNGELES <br><br> BOSCO', 'end_block': True},

    {'time': '11:45 - 12:30 h', 'group': '3ºA ESO', 'group_display': '3ºA ESO', 'activity': 'Braile (11:45-12:05) <br><br> Lanzamiento (12:05-12:30)', 'monitor': 'Coralia <br><br> UAVA', 'ayudante': '<br><br> BOSCO', 'obs': obs_general},
    {'time': '11:45 - 12:30 h', 'group': '3ºB ESO', 'group_display': '3ºB ESO', 'activity': 'Salto Longitud (11:45-12:05) <br><br> Carrera de Saco (12:05-12:30)', 'monitor': 'UAVA <br><br> Elena', 'ayudante': 'CRISTIAN <br><br>', 'end_block': True},
    {'time': '11:45 - 12:30 h', 'group': '3ºC ESO', 'group_display': '3ºC ESO', 'activity': 'Salto Comba (11:45-12:05) <br><br> Juego de palabras (12:05-12:30)', 'monitor': 'Migue (EF) <br><br> SILVIA', 'ayudante': '<br><br> ROSALVA'},
    {'time': '11:45 - 12:30 h', 'group': '3ºD ESO', 'group_display': '3ºD ESO', 'activity': 'Lanzamiento (11:45-12:05) <br><br> El pañuelito (12:05-12:30)', 'monitor': 'UAVA <br><br> CIRO', 'ayudante': 'BOSCO <br><br> ÁNGELES', 'end_block': True},
    {'time': '11:45 - 12:30 h', 'group': '3ºE ESO', 'group_display': '3ºE ESO', 'activity': 'Baile (11:45-12:05) <br><br> Carrera de Saco (12:05-12:30)', 'monitor': 'Coralia <br><br> Elena', 'end_block': True}
]

color_map_2 = {
    '1º A BACH': '#dcfce7', '1º B BACH': '#ccfbf1', '1º C BACH': '#e0e7ff', '1º BACH (Todos)': '#f1f5f9',
    '2º A BACH': '#fef3c7', '2º B BACH': '#ffedd5', '2º C BACH': '#fee2e2', '2º BACH + CICLOS': '#f1f5f9',
    'CICLOS': '#f3e8ff', 
    '4ºA ESO': '#e0f2fe', '4ºB ESO': '#dbeafe', '4ºC ESO': '#fae8ff', '4ºD ESO': '#fef08a', '4º ESO (Todos)': '#f1f5f9'
}

groups_2 = ['4ºA ESO', '4ºB ESO', '4ºC ESO', '4ºD ESO', '4º ESO (Todos)', '1º A BACH', '1º B BACH', '1º C BACH', '1º BACH (Todos)', '2º A BACH', '2º B BACH', '2º C BACH', 'CICLOS', '2º BACH + CICLOS']

area2_data = [
    {'time': '9:30 - 10:15 h', 'group': '1º A BACH', 'group_display': '1º A BACH', 'activity': 'Salto de comba (9:30-9:50) <br><br> El pañuelito (9:50-10:15)', 'monitor': 'Almudena <br><br> PAULA', 'ayudante': '<br><br> ROSI', 'obs': obs_general},
    {'time': '9:30 - 10:15 h', 'group': '1º B BACH', 'group_display': '1º B BACH', 'activity': 'Lanzamiento (9:30-9:50) <br><br> Brile (9:50-10:15)', 'monitor': 'UAVA <br><br> DIEGO', 'ayudante': '<br><br> VICKY'},
    {'time': '9:30 - 10:15 h', 'group': '1º C BACH', 'group_display': '1º C BACH', 'activity': 'Carrera de saco (9:30-9:50) <br><br> Salto Longitud (9:50-10:15)', 'monitor': 'Davinia <br><br> UAVA', 'end_block': True},

    {'time': '9:30 - 10:15 h', 'group': '2º A BACH', 'group_display': '2º A BACH', 'activity': 'El pañuelito (9:30-9:50) <br><br> Salto de comba (9:50-10:15)', 'monitor': 'PAULA <br><br> Almudena', 'ayudante': 'ROSI <br><br>', 'obs': obs_general},
    {'time': '9:30 - 10:15 h', 'group': '2º B BACH', 'group_display': '2º B BACH', 'activity': 'Brile (9:30-9:50) <br><br> Lanzamiento (9:50-10:15)', 'monitor': 'DIEGO <br><br> UAVA', 'ayudante': 'VICKY <br><br>'},
    {'time': '9:30 - 10:15 h', 'group': '2º C BACH', 'group_display': '2º C BACH', 'activity': 'Salto Longitud (9:30-9:50) <br><br> Carrera de saco (9:50-10:15)', 'monitor': 'UAVA <br><br> Davinia', 'end_block': True},

    {'time': '9:30 - 10:15 h', 'group': 'CICLOS', 'group_display': 'CICLOS', 'activity': 'Salto de comba (9:30-9:50) <br><br> Juego de palabras (9:50-10:15)', 'monitor': 'Almudena <br><br> ORLANDO R.', 'ayudante': '<br><br> ANA MATA', 'end_block': True},

    {'time': '9:30 - 10:15 h', 'group': '4º ESO (Todos)', 'group_display': '4º ESO (Todos)', 'activity': 'Hinchables acuáticos', 'monitor': 'DAMASI/', 'ayudante': 'Jose Fran Docente .que se quiera mojarse que contacte con Jose Fran ( para cubrir su función )', 'obs': 'Ayudar al monitor de DAMASI y mojarte', 'end_block': True},

    {'type': 'recreo'},
    {'type': 'zumba'},

    {'time': '11:00 - 11:40 h', 'group': '1º A BACH', 'group_display': '1º A BACH', 'activity': 'Lanzamiento (11:00-11:20) <br><br> Brile (11:20-11:40)', 'monitor': 'UAVA <br><br> DIEGO', 'ayudante': '<br><br> VICKY', 'obs': obs_general},
    {'time': '11:00 - 11:40 h', 'group': '1º B BACH', 'group_display': '1º B BACH', 'activity': 'Carrera de Saco (11:00-11:20) <br><br> Salto Longitud (11:20-11:40)', 'monitor': 'Davinia <br><br> UAVA', 'ayudante': 'Jose Fran <br><br>'},
    {'time': '11:00 - 11:40 h', 'group': '1º C BACH', 'group_display': '1º C BACH', 'activity': 'Juego de palabras (11:00-11:20) <br><br> Salto de comba (11:20-11:40)', 'monitor': 'ORLANDO R. <br><br> Almudena', 'ayudante': 'ANA MATA <br><br>', 'end_block': True},

    {'time': '11:00 - 11:40 h', 'group': '2º BACH + CICLOS', 'group_display': '2º BACH + CICLOS', 'activity': 'Hinchables Acuáticos', 'monitor': 'Damasi', 'ayudante': 'Docente que se quiera mojarse que contacte con Jose Fran ( para cubrir su función)', 'obs': 'Ayudar al monitor de DAMASI y mojarte', 'end_block': True},

    {'time': '11:00 - 11:40 h', 'group': '4ºA ESO', 'group_display': '4ºA ESO', 'activity': 'Salto de comba (11:00-11:20) <br><br> El pañuelito (11:20-11:40)', 'monitor': 'Almudena <br><br> PAULA', 'ayudante': '<br><br> ROSI', 'obs': obs_general},
    {'time': '11:00 - 11:40 h', 'group': '4ºB ESO', 'group_display': '4ºB ESO', 'activity': 'Brile (11:00-11:20) <br><br> Lanzamiento (11:20-11:40)', 'monitor': 'DIEGO <br><br> UAVA', 'ayudante': 'VICKY <br><br>', 'end_block': True},
    {'time': '11:00 - 11:40 h', 'group': '4ºC ESO', 'group_display': '4ºC ESO', 'activity': 'Carrera de saco (11:00-11:20) <br><br> Salto Longitud (11:20-11:40)', 'monitor': 'Davinia <br><br> UAVA'},
    {'time': '11:00 - 11:40 h', 'group': '4ºD ESO', 'group_display': '4ºD ESO', 'activity': 'Salto de comba (11:00-11:20) <br><br> Juego de palabras (11:20-11:40)', 'monitor': 'Almudena <br><br> ORLANDO R.', 'ayudante': '<br><br> ANA MATA', 'end_block': True},

    {'time': '11:45 - 12:30 h', 'group': '1º BACH (Todos)', 'group_display': '1º BACH (Todos)', 'activity': 'Hinchables Acuáticos', 'monitor': 'Damasi/ Almudena', 'ayudante': 'Docente que se quiera mojarse que contacte con Jose Fran ( para cubrir su función )', 'obs': 'Ayudar al monitor de DAMASI y mojarte', 'end_block': True},

    {'time': '11:45 - 12:30 h', 'group': '2º A BACH', 'group_display': '2º A BACH', 'activity': 'Lanzamiento (11:45-12:05) <br><br> Braile (12:05-12:30)', 'monitor': 'UAVA <br><br> DIEGO', 'ayudante': '<br><br> VICKY', 'obs': obs_general},
    {'time': '11:45 - 12:30 h', 'group': '2º B BACH', 'group_display': '2º B BACH', 'activity': 'Carrera de Saco (11:45-12:05) <br><br> Salto Longitud (12:05-12:30)', 'monitor': 'Davinia <br><br> UAVA'},
    {'time': '11:45 - 12:30 h', 'group': '2º C BACH', 'group_display': '2º C BACH', 'activity': 'Juego de palabras (11:45-12:05) <br><br> Salto Comba (12:05-12:30)', 'monitor': 'ORLANDO R. <br><br> Almudena', 'ayudante': 'ANA MATA <br><br>', 'end_block': True},

    {'time': '11:45 - 12:30 h', 'group': 'CICLOS', 'group_display': 'CICLOS', 'activity': 'Pañuelito (11:45-12:05) <br><br> Lanzamiento (12:05-12:30)', 'monitor': 'PAULA <br><br> UAVA', 'ayudante': 'ROSI <br><br>', 'end_block': True},

    {'time': '11:45 - 12:30 h', 'group': '4ºA ESO', 'group_display': '4ºA ESO', 'activity': 'Braile (11:45-12:05) <br><br> Lanzamiento (12:05-12:30)', 'monitor': 'DIEGO <br><br> UAVA', 'ayudante': 'VICKY <br><br>', 'obs': obs_general},
    {'time': '11:45 - 12:30 h', 'group': '4ºB ESO', 'group_display': '4ºB ESO', 'activity': 'Salto Longitud (11:45-12:05) <br><br> Carrera de Saco (12:05-12:30)', 'monitor': 'UAVA <br><br> Davinia', 'end_block': True},
    {'time': '11:45 - 12:30 h', 'group': '4ºC ESO', 'group_display': '4ºC ESO', 'activity': 'Salto Comba (11:45-12:05) <br><br> Juego de palabras (12:05-12:30)', 'monitor': 'Almudena <br><br> ORLANDO R.', 'ayudante': '<br><br> ANA MATA'},
    {'time': '11:45 - 12:30 h', 'group': '4ºD ESO', 'group_display': '4ºD ESO', 'activity': 'Lanzamiento (11:45-12:05) <br><br> El pañuelito (12:05-12:30)', 'monitor': 'UAVA <br><br> PAULA', 'ayudante': '<br><br> ROSI', 'end_block': True}
]

with open('area1.html', 'w', encoding='utf-8') as f:
    f.write(create_html('Cuadrante Área 1 - Convivencia Lúdica', '1º, 2º, 3º ESO y Aula Enclave', groups_1, area1_data, color_map_1))

with open('area2.html', 'w', encoding='utf-8') as f:
    f.write(create_html('Cuadrante Área 2 - Convivencia Lúdica', '4º ESO, 1º y 2º BACH y CICLOS', groups_2, area2_data, color_map_2))
