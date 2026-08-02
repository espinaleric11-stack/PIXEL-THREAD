<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pixel Thread - Control de Pedidos</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-slate-100 font-sans min-h-screen p-6">

    <div class="max-w-4xl mx-auto">
        <!-- Encabezado -->
        <header class="flex justify-between items-center mb-8 border-b border-slate-700 pb-4">
            <div>
                <h1 class="text-2xl font-bold text-indigo-400">Pixel Thread</h1>
                <p class="text-sm text-slate-400">Gestión de Digitalización y Facturación Semanal</p>
            </div>
            <div class="bg-slate-800 px-4 py-2 rounded-lg border border-slate-700 text-right">
                <span class="text-xs text-slate-400 block">Acumulado Actual (Semana)</span>
                <span id="totalAcumulado" class="text-xl font-bold text-emerald-400">$0.00 USD</span>
            </div>
        </header>

        <!-- Contenido Principal -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            <!-- Lista de Trabajos (2 Columnas) -->
            <div class="md:col-span-2 bg-slate-800 rounded-xl p-5 border border-slate-700">
                <h2 class="text-lg font-semibold mb-4 text-slate-200">Trabajos Activos - Cliente: <span class="text-indigo-300">Cliente Ejemplo S.A.</span></h2>
                
                <div id="listaLogos" class="space-y-3">
                    <div class="flex items-center justify-between bg-slate-700/50 p-3 rounded-lg border border-slate-600">
                        <div>
                            <p class="font-medium text-slate-100">Logo León Dorado (Pecho)</p>
                            <span class="text-xs px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-medium estado-txt">En Proceso</span>
                        </div>
                        <div class="flex items-center gap-4">
                            <span class="text-sm font-semibold text-slate-300">$15.00</span>
                            <button onclick="terminarLogo(this, 15, 'Logo León Dorado (Pecho)')" class="bg-indigo-600 hover:bg-indigo-500 text-white text-xs px-3 py-1.5 rounded font-medium transition btn-accion">
                                Terminar ✓
                            </button>
                        </div>
                    </div>

                    <div class="flex items-center justify-between bg-slate-700/50 p-3 rounded-lg border border-slate-600">
                        <div>
                            <p class="font-medium text-slate-100">Logo Cafetería (Manga)</p>
                            <span class="text-xs px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-medium estado-txt">En Proceso</span>
                        </div>
                        <div class="flex items-center gap-4">
                            <span class="text-sm font-semibold text-slate-300">$12.00</span>
                            <button onclick="terminarLogo(this, 12, 'Logo Cafetería (Manga)')" class="bg-indigo-600 hover:bg-indigo-500 text-white text-xs px-3 py-1.5 rounded font-medium transition btn-accion">
                                Terminar ✓
                            </button>
                        </div>
                    </div>

                    <div class="flex items-center justify-between bg-slate-700/50 p-3 rounded-lg border border-slate-600">
                        <div>
                            <p class="font-medium text-slate-100">Escudo Deportivo (Espalda)</p>
                            <span class="text-xs px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-medium estado-txt">En Proceso</span>
                        </div>
                        <div class="flex items-center gap-4">
                            <span class="text-sm font-semibold text-slate-300">$20.00</span>
                            <button onclick="terminarLogo(this, 20, 'Escudo Deportivo (Espalda)')" class="bg-indigo-600 hover:bg-indigo-500 text-white text-xs px-3 py-1.5 rounded font-medium transition btn-accion">
                                Terminar ✓
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Panel de Automatización / Lunes (1 Columna) -->
            <div class="bg-slate-800 rounded-xl p-5 border border-slate-700 flex flex-col justify-between">
                <div>
                    <h2 class="text-lg font-semibold mb-2 text-slate-200">Facturación Automática</h2>
                    <p class="text-xs text-slate-400 mb-4">Simula el proceso programado que se ejecuta cada lunes para enviar el cobro de la semana.</p>
                    
                    <div class="bg-slate-900 p-3 rounded-lg border border-slate-700 mb-4">
                        <span class="text-xs text-slate-400 block">Logos terminados esta semana:</span>
                        <span id="contadorTerminados" class="text-2xl font-bold text-indigo-400">0</span>
                    </div>
                </div>

                <button onclick="simularCorteLunes()" class="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-medium py-2.5 px-4 rounded-lg text-sm transition shadow-lg shadow-emerald-900/20">
                    Simular Corte de Lunes 📄
                </button>
            </div>

        </div>

        <!-- Ventana de Factura Generada -->
        <div id="modalFactura" class="hidden mt-6 bg-slate-800 border border-emerald-500/50 rounded-xl p-6">
            <h3 class="text-lg font-bold text-emerald-400 mb-2">¡Factura Generada y Enviada! (Simulación Lunes)</h3>
            <p class="text-sm text-slate-300 mb-4">Se ha enviado el PDF al cliente con el siguiente desglose:</p>
            <div id="detalleFactura" class="bg-slate-900 p-4 rounded-lg text-sm text-slate-300 space-y-1 font-mono"></div>
        </div>

    </div>

    <script>
        let acumuladoTotal = 0;
        let logosTerminadosCount = 0;
        let itemsTerminadosLista = [];

        function terminarLogo(btn, precio, nombreLogo) {
            const contenedor = btn.closest('div.flex');
            const estadoTxt = contenedor.querySelector('.estado-txt');
            
            estadoTxt.textContent = "Terminado";
            estadoTxt.className = "text-xs px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-medium estado-txt";
            
            btn.textContent = "Completado ✓";
            btn.className = "bg-slate-600 text-slate-300 text-xs px-3 py-1.5 rounded font-medium cursor-not-allowed";
            btn.disabled = true;

            acumuladoTotal += precio;
            logosTerminadosCount += 1;
            itemsTerminadosLista.push({ nombre: nombreLogo, precio: precio });

            document.getElementById('totalAcumulado').textContent = `$${acumuladoTotal.toFixed(2)} USD`;
            document.getElementById('contadorTerminados').textContent = logosTerminadosCount;
        }

        function simularCorteLunes() {
            if (logosTerminadosCount === 0) {
                alert("No hay logos terminados esta semana para facturar.");
                return;
            }

            const modal = document.getElementById('modalFactura');
            const detalle = document.getElementById('detalleFactura');
            
            let htmlDetalle = `<p class="border-b border-slate-700 pb-2 mb-2 font-bold">FACTURA SEMANAL - PIXEL THREAD</p>`;
            itemsTerminadosLista.forEach(item => {
                htmlDetalle += `<div class="flex justify-between"><span>- ${item.nombre}</span> <span>$${item.precio.toFixed(2)}</span></div>`;
            });
            htmlDetalle += `<div class="border-t border-slate-700 pt-2 mt-2 flex justify-between font-bold text-emerald-400"><span>TOTAL A PAGAR:</span> <span>$${acumuladoTotal.toFixed(2)} USD</span></div>`;

            detalle.innerHTML = htmlDetalle;
            modal.classList.remove('hidden');
        }
    </script>
</body>
</html>
