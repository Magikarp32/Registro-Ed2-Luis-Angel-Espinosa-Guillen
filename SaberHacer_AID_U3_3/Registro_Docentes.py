import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
from datetime import datetime

class SistemaDocentes:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 Sistema de Gestión de Docentes - Edificio 2")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Lista para almacenar docentes
        self.docentes = []
        self.simular_errores = False
        
        # Cargar datos existentes
        self.cargar_datos_desde_json()
        
        # Crear interfaz
        self.crear_interfaz()
        
    def cargar_datos_desde_json(self):
        """Carga los datos desde el archivo JSON si existe"""
        try:
            if os.path.exists("docentes.json"):
                with open("docentes.json", 'r', encoding='utf-8') as archivo:
                    self.docentes = json.load(archivo)
                print("✓ Datos cargados desde archivo JSON")
        except Exception as e:
            print(f"✗ Error al cargar datos: {e}")

    def guardar_datos(self):
        """Guarda los datos en todos los formatos"""
        self.generar_archivo_json()
        self.generar_archivo_xml()
        self.generar_archivo_yaml_simple()

    def generar_archivo_json(self):
        try:
            with open("docentes.json", 'w', encoding='utf-8') as archivo:
                json.dump(self.docentes, archivo, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar JSON: {e}")
            return False

    def generar_archivo_xml(self):
        try:
            root = ET.Element("docentes")
            for docente in self.docentes:
                docente_elem = ET.SubElement(root, "docente")
                ET.SubElement(docente_elem, "nombre").text = docente["nombre"]
                ET.SubElement(docente_elem, "especialidad").text = docente["especialidad"]
                ET.SubElement(docente_elem, "numero_empleado").text = str(docente["numero_empleado"])
            
            xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
            with open("docentes.xml", 'w', encoding='utf-8') as archivo:
                archivo.write(xml_str)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar XML: {e}")
            return False

    def generar_archivo_yaml_simple(self):
        try:
            with open("docentes.yaml", 'w', encoding='utf-8') as archivo:
                archivo.write("docentes:\n")
                for docente in self.docentes:
                    archivo.write("  - nombre: " + docente['nombre'] + "\n")
                    archivo.write("    especialidad: " + docente['especialidad'] + "\n")
                    archivo.write("    numero_empleado: " + str(docente['numero_empleado']) + "\n")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar YAML: {e}")
            return False

    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="🎓 Sistema de Gestión de Docentes", 
                          font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Sección de simulación de errores
        errores_frame = ttk.LabelFrame(main_frame, text="🔧 Simulación de Errores HTTP", padding="10")
        errores_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        errores_frame.columnconfigure(0, weight=1)
        
        self.btn_errores = ttk.Button(errores_frame, text="Activar Simulación de Errores: INACTIVO",
                                     command=self.toggle_errores)
        self.btn_errores.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5)
        
        btn_frame = ttk.Frame(errores_frame)
        btn_frame.grid(row=1, column=0, pady=5)
        
        ttk.Button(btn_frame, text="Error 400", 
                  command=lambda: self.simular_error(400)).grid(row=0, column=0, padx=2)
        ttk.Button(btn_frame, text="Error 500", 
                  command=lambda: self.simular_error(500)).grid(row=0, column=1, padx=2)
        ttk.Button(btn_frame, text="Error 502", 
                  command=lambda: self.simular_error(502)).grid(row=0, column=2, padx=2)
        
        # Sección de operaciones CRUD
        crud_frame = ttk.LabelFrame(main_frame, text="📝 Operaciones CRUD", padding="10")
        crud_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Formulario para agregar/actualizar
        form_frame = ttk.Frame(crud_frame)
        form_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.entry_nombre = ttk.Entry(form_frame, width=20)
        self.entry_nombre.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(form_frame, text="Especialidad:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.entry_especialidad = ttk.Entry(form_frame, width=20)
        self.entry_especialidad.grid(row=0, column=3, padx=(0, 10))
        
        ttk.Label(form_frame, text="Número Empleado:").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.entry_numero = ttk.Entry(form_frame, width=15)
        self.entry_numero.grid(row=0, column=5, padx=(0, 10))
        
        # Botones de operaciones
        btn_crud_frame = ttk.Frame(crud_frame)
        btn_crud_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Button(btn_crud_frame, text="➕ Agregar", 
                  command=self.agregar_docente).grid(row=0, column=0, padx=2)
        ttk.Button(btn_crud_frame, text="🔍 Buscar", 
                  command=self.buscar_docente).grid(row=0, column=1, padx=2)
        ttk.Button(btn_crud_frame, text="✏️ Actualizar", 
                  command=self.actualizar_docente).grid(row=0, column=2, padx=2)
        ttk.Button(btn_crud_frame, text="🗑️ Eliminar", 
                  command=self.eliminar_docente).grid(row=0, column=3, padx=2)
        ttk.Button(btn_crud_frame, text="📋 Listar Todos", 
                  command=self.listar_docentes).grid(row=0, column=4, padx=2)
        
        # Búsqueda
        search_frame = ttk.Frame(crud_frame)
        search_frame.grid(row=2, column=0, columnspan=2, pady=5)
        
        ttk.Label(search_frame, text="Buscar por:").grid(row=0, column=0, padx=(0, 5))
        self.combo_busqueda = ttk.Combobox(search_frame, values=["Número", "Nombre", "Especialidad"], width=15)
        self.combo_busqueda.grid(row=0, column=1, padx=(0, 10))
        self.combo_busqueda.set("Número")
        
        self.entry_busqueda = ttk.Entry(search_frame, width=20)
        self.entry_busqueda.grid(row=0, column=2, padx=(0, 10))
        
        ttk.Button(search_frame, text="🔎 Buscar", 
                  command=self.buscar_docente_avanzado).grid(row=0, column=3, padx=2)
        
        # Sección de archivos
        archivos_frame = ttk.LabelFrame(main_frame, text="📁 Generación de Archivos", padding="10")
        archivos_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(archivos_frame, text="🔄 Generar Todos los Archivos", 
                  command=self.generar_archivos).grid(row=0, column=0, padx=5)
        ttk.Button(archivos_frame, text="📊 Estadísticas", 
                  command=self.mostrar_estadisticas).grid(row=0, column=1, padx=5)
        
        # Área de resultados
        resultados_frame = ttk.LabelFrame(main_frame, text="📊 Resultados", padding="10")
        resultados_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        resultados_frame.columnconfigure(0, weight=1)
        resultados_frame.rowconfigure(0, weight=1)
        
        self.text_resultados = scrolledtext.ScrolledText(resultados_frame, width=80, height=15)
        self.text_resultados.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Barra de estado
        self.status_var = tk.StringVar(value="Sistema listo - Total de docentes: 0")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Actualizar estado inicial
        self.actualizar_estado()

    def toggle_errores(self):
        """Activar/desactivar simulación de errores"""
        self.simular_errores = not self.simular_errores
        estado = "ACTIVO" if self.simular_errores else "INACTIVO"
        self.btn_errores.config(text=f"Activar Simulación de Errores: {estado}")
        self.mostrar_resultado(f"Simulación de errores {estado.lower()}")

    def simular_error(self, codigo_error):
        """Simular error HTTP"""
        if codigo_error == 400:
            mensaje = "400 Bad Request - Solicitud incorrecta simulada"
        elif codigo_error == 500:
            mensaje = "500 Internal Server Error - Error interno del servidor simulado"
        elif codigo_error == 502:
            mensaje = "502 Bad Gateway - Gateway incorrecto simulado"
        else:
            mensaje = f"Error {codigo_error} no configurado"
        
        self.mostrar_resultado(f"🔧 ERROR SIMULADO:\n{mensaje}\nCódigo: {codigo_error}")

    def validar_campos(self):
        """Validar que los campos obligatorios estén llenos"""
        if not self.entry_nombre.get().strip():
            messagebox.showwarning("Validación", "El nombre es obligatorio")
            return False
        if not self.entry_especialidad.get().strip():
            messagebox.showwarning("Validación", "La especialidad es obligatoria")
            return False
        if not self.entry_numero.get().strip():
            messagebox.showwarning("Validación", "El número de empleado es obligatorio")
            return False
        try:
            int(self.entry_numero.get())
        except ValueError:
            messagebox.showwarning("Validación", "El número de empleado debe ser un número válido")
            return False
        return True

    def limpiar_campos(self):
        """Limpiar los campos del formulario"""
        self.entry_nombre.delete(0, tk.END)
        self.entry_especialidad.delete(0, tk.END)
        self.entry_numero.delete(0, tk.END)

    def agregar_docente(self):
        """Agregar un nuevo docente"""
        if not self.validar_campos():
            return
        
        if self.simular_errores:
            self.simular_error(400)
            return
        
        numero_empleado = int(self.entry_numero.get())
        
        # Verificar si ya existe
        if any(d['numero_empleado'] == numero_empleado for d in self.docentes):
            messagebox.showerror("Error", "Ya existe un docente con ese número de empleado")
            return
        
        docente = {
            "nombre": self.entry_nombre.get().strip(),
            "especialidad": self.entry_especialidad.get().strip(),
            "numero_empleado": numero_empleado,
            "fecha_registro": datetime.now().isoformat()
        }
        
        self.docentes.append(docente)
        self.guardar_datos()
        self.mostrar_resultado(f"✅ DOCENTE AGREGADO EXITOSAMENTE:\n{json.dumps(docente, indent=2, ensure_ascii=False)}")
        self.limpiar_campos()
        self.actualizar_estado()

    def buscar_docente(self):
        """Buscar docente por número de empleado"""
        if not self.entry_numero.get().strip():
            messagebox.showwarning("Búsqueda", "Ingrese un número de empleado para buscar")
            return
        
        if self.simular_errores:
            self.simular_error(500)
            return
        
        try:
            numero = int(self.entry_numero.get())
            docente = next((d for d in self.docentes if d['numero_empleado'] == numero), None)
            
            if docente:
                self.mostrar_resultado(f"✅ DOCENTE ENCONTRADO:\n{json.dumps(docente, indent=2, ensure_ascii=False)}")
            else:
                self.mostrar_resultado("❌ No se encontró ningún docente con ese número de empleado")
                
        except ValueError:
            messagebox.showerror("Error", "El número de empleado debe ser un número válido")

    def buscar_docente_avanzado(self):
        """Búsqueda avanzada por diferentes criterios"""
        criterio = self.combo_busqueda.get()
        valor = self.entry_busqueda.get().strip()
        
        if not valor:
            messagebox.showwarning("Búsqueda", "Ingrese un valor para buscar")
            return
        
        if self.simular_errores:
            self.simular_error(500)
            return
        
        resultados = []
        if criterio == "Número":
            try:
                numero = int(valor)
                resultados = [d for d in self.docentes if d['numero_empleado'] == numero]
            except ValueError:
                messagebox.showerror("Error", "El número de empleado debe ser un número válido")
                return
        elif criterio == "Nombre":
            resultados = [d for d in self.docentes if valor.lower() in d['nombre'].lower()]
        elif criterio == "Especialidad":
            resultados = [d for d in self.docentes if valor.lower() in d['especialidad'].lower()]
        
        if resultados:
            self.mostrar_resultado(f"✅ {len(resultados)} DOCENTE(S) ENCONTRADO(S):\n{json.dumps(resultados, indent=2, ensure_ascii=False)}")
        else:
            self.mostrar_resultado("❌ No se encontraron docentes con los criterios especificados")

    def actualizar_docente(self):
        """Actualizar un docente existente"""
        if not self.entry_numero.get().strip():
            messagebox.showwarning("Actualización", "Ingrese el número de empleado del docente a actualizar")
            return
        
        if self.simular_errores:
            self.simular_error(400)
            return
        
        try:
            numero = int(self.entry_numero.get())
            docente = next((d for d in self.docentes if d['numero_empleado'] == numero), None)
            
            if not docente:
                messagebox.showerror("Error", "No se encontró un docente con ese número de empleado")
                return
            
            # Actualizar campos si se proporcionaron nuevos valores
            nuevo_nombre = self.entry_nombre.get().strip()
            nueva_especialidad = self.entry_especialidad.get().strip()
            
            if nuevo_nombre:
                docente['nombre'] = nuevo_nombre
            if nueva_especialidad:
                docente['especialidad'] = nueva_especialidad
            
            docente['fecha_actualizacion'] = datetime.now().isoformat()
            self.guardar_datos()
            
            self.mostrar_resultado(f"✅ DOCENTE ACTUALIZADO EXITOSAMENTE:\n{json.dumps(docente, indent=2, ensure_ascii=False)}")
            self.limpiar_campos()
            self.actualizar_estado()
            
        except ValueError:
            messagebox.showerror("Error", "El número de empleado debe ser un número válido")

    def eliminar_docente(self):
        """Eliminar un docente"""
        if not self.entry_numero.get().strip():
            messagebox.showwarning("Eliminación", "Ingrese el número de empleado del docente a eliminar")
            return
        
        if self.simular_errores:
            self.simular_error(500)
            return
        
        try:
            numero = int(self.entry_numero.get())
            docente = next((d for d in self.docentes if d['numero_empleado'] == numero), None)
            
            if not docente:
                messagebox.showerror("Error", "No se encontró un docente con ese número de empleado")
                return
            
            # Confirmar eliminación
            respuesta = messagebox.askyesno(
                "Confirmar Eliminación", 
                f"¿Está seguro de que desea eliminar al docente:\n\n"
                f"Nombre: {docente['nombre']}\n"
                f"Especialidad: {docente['especialidad']}\n"
                f"Número: {docente['numero_empleado']}"
            )
            
            if respuesta:
                self.docentes = [d for d in self.docentes if d['numero_empleado'] != numero]
                self.guardar_datos()
                self.mostrar_resultado(f"✅ DOCENTE ELIMINADO EXITOSAMENTE:\n{json.dumps(docente, indent=2, ensure_ascii=False)}")
                self.limpiar_campos()
                self.actualizar_estado()
                
        except ValueError:
            messagebox.showerror("Error", "El número de empleado debe ser un número válido")

    def listar_docentes(self):
        """Listar todos los docentes"""
        if self.simular_errores:
            self.simular_error(500)
            return
        
        if not self.docentes:
            self.mostrar_resultado("📝 No hay docentes registrados en el sistema")
            return
        
        self.mostrar_resultado(f"📋 LISTA COMPLETA DE DOCENTES ({len(self.docentes)}):\n{json.dumps(self.docentes, indent=2, ensure_ascii=False)}")

    def generar_archivos(self):
        """Generar todos los archivos de exportación"""
        if self.simular_errores:
            self.simular_error(502)
            return
        
        json_ok = self.generar_archivo_json()
        xml_ok = self.generar_archivo_xml()
        yaml_ok = self.generar_archivo_yaml_simple()
        
        mensaje = "📁 ARCHIVOS GENERADOS:\n"
        mensaje += f"✅ JSON: {'docentes.json' if json_ok else 'ERROR'}\n"
        mensaje += f"✅ XML: {'docentes.xml' if xml_ok else 'ERROR'}\n"
        mensaje += f"✅ YAML: {'docentes.yaml' if yaml_ok else 'ERROR'}\n"
        mensaje += f"📊 Total de registros: {len(self.docentes)}"
        
        self.mostrar_resultado(mensaje)

    def mostrar_estadisticas(self):
        """Mostrar estadísticas del sistema"""
        total = len(self.docentes)
        especialidades = {}
        
        for docente in self.docentes:
            esp = docente['especialidad']
            especialidades[esp] = especialidades.get(esp, 0) + 1
        
        mensaje = "📊 ESTADÍSTICAS DEL SISTEMA:\n"
        mensaje += f"📈 Total de docentes: {total}\n"
        mensaje += f"🔧 Simulación de errores: {'ACTIVA' if self.simular_errores else 'INACTIVA'}\n"
        mensaje += "\n📚 Distribución por especialidad:\n"
        
        for esp, cantidad in especialidades.items():
            porcentaje = (cantidad / total) * 100 if total > 0 else 0
            mensaje += f"   • {esp}: {cantidad} ({porcentaje:.1f}%)\n"
        
        self.mostrar_resultado(mensaje)

    def mostrar_resultado(self, mensaje):
        """Mostrar resultado en el área de texto"""
        self.text_resultados.delete(1.0, tk.END)
        self.text_resultados.insert(tk.END, mensaje)
        self.text_resultados.see(tk.END)

    def actualizar_estado(self):
        """Actualizar la barra de estado"""
        total = len(self.docentes)
        estado_errores = "ACTIVA" if self.simular_errores else "inactiva"
        self.status_var.set(f"Sistema listo - Docentes: {total} - Simulación de errores: {estado_errores}")

def main():
    """Función principal"""
    try:
        root = tk.Tk()
        app = SistemaDocentes(root)
        root.mainloop()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")

if __name__ == "__main__":
    main()