def guardar_datos():
    # Limpiamos los logos eliminando objetos no serializables como bytes o imágenes
    logos_limpios = []
    for l in st.session_state.logos:
        logo_copy = {}
        for k, v in l.items():
            if k in ["imagen_obj", "archivo_bordado_bytes", "archivos_multiples"]:
                # Omitimos o convertimos los campos binarios para evitar errores en JSON
                if k == "archivos_multiples" and isinstance(v, list):
                    # Solo guardamos los nombres de los archivos múltiples, no los bytes
                    logo_copy[k] = [{"nombre": arch.get("nombre")} for arch in v if isinstance(arch, dict)]
                continue
            logo_copy[k] = v
        logos_limpios.append(logo_copy)

    # Limpiamos los recibos de pago para guardar solo metadatos si fuera necesario, o los omitimos del JSON principal
    recibos_limpios = {}
    for cli, rec in st.session_state.get("recibos_pago", {}).items():
        recibos_limpios[cli] = {
            "nombre_archivo": rec.get("nombre_archivo")
            # Los bytes se quedan solo en memoria para evitar corromper el archivo JSON
        }

    datos = {
        "clientes_registrados": st.session_state.clientes_registrados,
        "logos": logos_limpios,
        "recibos_pago_meta": recibos_limpios
    }
    
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
