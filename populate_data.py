"""
Script de población de datos de prueba para la API Biblioteca UNCP.
Ejecutar con: python populate_data.py
Genera: 10 usuarios, 15 autores, 50 libros, 30 préstamos.
"""
import os
import django
import random
from datetime import date, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from biblioteca.models import Usuario, Autor, Libro, Prestamo

# ==========================================
# LIMPIAR BASE DE DATOS (opcional, para reejecutar)
# ==========================================
print("🧹 Limpiando datos anteriores...")
Prestamo.objects.all().delete()
Libro.objects.all().delete()
Autor.objects.all().delete()
Usuario.objects.all().delete()

# ==========================================
# 1. CREAR USUARIOS (RF3) - 10 usuarios
# ==========================================
print("👥 Creando usuarios...")
usuarios_data = [
    # (username, tipo, carrera, telefono)
    ('jsilva',    'estudiante',    'Ingeniería de Sistemas', '987654321'),
    ('mquispe',   'estudiante',    'Agronomía',              '912345678'),
    ('cramirez',  'estudiante',    'Medicina',               '998877665'),
    ('lhuaman',   'estudiante',    'Contabilidad',           '965432109'),
    ('atorres',   'docente',       'Ingeniería Civil',       '934567890'),
    ('rcondori',  'docente',       'Física',                 '923456781'),
    ('pcastillo', 'investigador',  'Biología',               '912345670'),
    ('nflores',   'investigador',  'Química',                '901234567'),
    ('dbiblioteca', 'bibliotecario', 'Ciencias de la Información', '999888777'),
    ('adminuncp',   'admin',         'Administración',       '987654320'),
]

usuarios = []
for username, tipo, carrera, telefono in usuarios_data:
    # get_or_create para que el admin ya existente no falle
    u, created = Usuario.objects.get_or_create(
        username=username,
        defaults={
            'tipo': tipo,
            'carrera': carrera,
            'telefono': telefono,
            'email': f"{username}@uncp.edu.pe",
            'is_staff': tipo in ['bibliotecario', 'admin'],
            'is_superuser': username == 'adminuncp',
        }
    )
    u.set_password('uncp2026')  # Contraseña por defecto para todos
    u.save()
    usuarios.append(u)

print(f"   ✅ {len(usuarios)} usuarios creados")

# ==========================================
# 2. CREAR AUTORES - 15 autores
# ==========================================
print("✍️ Creando autores...")
autores_data = [
    ('Mario Vargas Llosa',   'Peruana',  'Premio Nobel de Literatura 2010.'),
    ('César Vallejo',        'Peruana',  'Poeta vanguardista peruano.'),
    ('José María Arguedas',  'Peruana',  'Escritor y antropólogo.'),
    ('Albert Einstein',      'Alemana',  'Físico teórico, relatividad.'),
    ('Isaac Newton',         'Británica','Matemático y físico.'),
    ('Stephen Hawking',      'Británica','Físico teórico, cosmología.'),
    ('Donald Knuth',         'Estadounidense', 'Padre del análisis de algoritmos.'),
    ('Martin Fowler',        'Británica', 'Experto en arquitectura de software.'),
    ('Robert C. Martin',     'Estadounidense', 'Autor de Clean Code.'),
    ('Gabriel García Márquez','Colombiana','Realismo mágico.'),
    ('Julio Cortázar',       'Argentina', 'Narrador y poeta.'),
    ('Carl Sagan',           'Estadounidense', 'Astrónomo divulgador.'),
    ('Nassim Nicholas Taleb','Libanesa',  'Autor de El Cisne Negro.'),
    ('Daniel Kahneman',      'Israelí',   'Economista conductual.'),
    ('Michael Porter',       'Estadounidense', 'Estrategia competitiva.'),
]

autores = []
for nombre, nac, bio in autores_data:
    a, _ = Autor.objects.get_or_create(nombre=nombre, defaults={'nacionalidad': nac, 'biografia': bio})
    autores.append(a)

print(f"   ✅ {len(autores)} autores creados")

# ==========================================
# 3. CREAR LIBROS - 50 libros
# ==========================================
print("📚 Creando libros...")
categorias = ['Ingeniería', 'Ciencias', 'Literatura', 'Economía', 'Medicina', 'Agronomía', 'Sistemas']
editoriales = ['Penguin', 'McGraw-Hill', 'Pearson', 'Planeta', 'Alfaguara', 'UNCP', 'Cátedra']

titulos = [
    'Cien Años de Soledad', 'Conversación en La Catedral', 'Los Ríos Profundos',
    'Trilce', 'Relatividad: Teoría Especial y General', 'Principia Mathematica',
    'Breve Historia del Tiempo', 'El Arte de Programar', 'Refactoring',
    'Clean Code', 'El Cisne Negro', 'Pensar Rápido, Pensar Despacio',
    'Estrategia Competitiva', 'Cosmos', 'La Ciudad y los Perros',
    'Algoritmos: Teoría y Práctica', 'Introducción a la Bases de Datos',
    'Sistemas Operativos Modernos', 'Redes de Computadoras', 'Ingeniería de Software',
    'Física Universitaria', 'Cálculo de una Variable', 'Ecuaciones Diferenciales',
    'Química General', 'Biología Celular', 'Genética Molecular',
    'Microbiología Médica', 'Anatomía Humana', 'Fisiología',
    'Botánica Económica', 'Suelos y Fertilidad', 'Zootecnia',
    'Contabilidad Básica', 'Matemáticas Financieras', 'Microeconomía',
    'Macroeconomía', 'Marketing Digital', 'Estadística Aplicada',
    'Investigación Operativa', 'Inteligencia Artificial', 'Machine Learning',
    'Big Data', 'Seguridad Informática', 'Desarrollo Web Fullstack',
    'Python para Ciencia de Datos', 'Django en Acción', 'REST APIs con DRF',
    'Arquitectura de Microservicios', 'DevOps en la Práctica', 'Cloud Computing',
]

libros = []
for i, titulo in enumerate(titulos):
    autor = random.choice(autores)
    isbn = f"978-{random.randint(1000000000, 9999999999)}"
    libro, _ = Libro.objects.get_or_create(
        isbn=isbn,
        defaults={
            'titulo': titulo,
            'autor': autor,
            'editorial': random.choice(editoriales),
            'anio': random.randint(1990, 2025),
            'categoria': random.choice(categorias),
            'stock': random.randint(0, 10),
            'ubicacion': f"Estante {random.randint(1, 8)}, Piso {random.randint(1, 3)}",
        }
    )
    libros.append(libro)

print(f"   ✅ {len(libros)} libros creados")

# ==========================================
# 4. CREAR PRÉSTAMOS - 30 préstamos
# ==========================================
print("🔄 Creando préstamos...")
hoy = date.today()
prestamos = []

for i in range(30):
    usuario = random.choice([u for u in usuarios if u.tipo in ['estudiante', 'docente', 'investigador']])
    libro = random.choice(libros)
    
    # Generar fecha de préstamo (entre 40 días atrás y hoy)
    dias_atras = random.randint(1, 40)
    fecha_prestamo = hoy - timedelta(days=dias_atras)
    fecha_devolucion = fecha_prestamo + timedelta(days=14)  # 14 días de plazo
    
    # Determinar estado según fechas
    if fecha_devolucion < hoy:
        # Ya venció: 50% devuelto, 50% vencido
        estado = random.choice(['devuelto', 'vencido'])
    else:
        estado = 'activo'
    
    p = Prestamo.objects.create(
        usuario=usuario,
        libro=libro,
        fecha_devolucion=fecha_devolucion,
        estado=estado,
    )
    # Ajustar la fecha_prestamo (auto_now_add la pone en hoy)
    p.fecha_prestamo = fecha_prestamo
    p.save()
    prestamos.append(p)

print(f"   ✅ {len(prestamos)} préstamos creados")

# ==========================================
# RESUMEN FINAL
# ==========================================
print("\n" + "="*50)
print("📊 RESUMEN DE DATOS GENERADOS")
print("="*50)
print(f"   👥 Usuarios:       {Usuario.objects.count()}")
print(f"   ✍️  Autores:        {Autor.objects.count()}")
print(f"   📚 Libros:         {Libro.objects.count()}")
print(f"   🔄 Préstamos:      {Prestamo.objects.count()}")
print(f"      • Activos:      {Prestamo.objects.filter(estado='activo').count()}")
print(f"      • Vencidos:     {Prestamo.objects.filter(estado='vencido').count()}")
print(f"      • Devueltos:    {Prestamo.objects.filter(estado='devuelto').count()}")
print("="*50)
print("🎉 ¡Población de datos completada!")
print("   Contraseña de todos los usuarios: uncp2026")